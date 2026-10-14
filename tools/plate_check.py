"""Sanity-check flat plates (CF, metal) and compare them hole-by-hole with a reference variant.

Run with FreeCAD's freecadcmd (see plate-check.ps1). Settings come from env vars, because
freecadcmd doesn't pass script arguments through reliably:
  PLATE_VARIANT   variant folder to check, e.g. "Metal Version"
  PLATE_REF       optional reference variant to compare against, e.g. "CF Version"
  PLATE_ONLY      optional: only plates whose name contains this text
  PLATE_OUT       folder for marked-up drawings of plates with findings
  PLATE_MIN_WALL  thinnest allowed material between features (mm, default 1.5)

Per plate it checks:
  - thickness = the number before "mm" at the end of the file name (e.g. Metal5mm -> 5)
  - position: the plate should sit on 0,0,0
  - holes by role: tap drill (M2 1.6, M3 2.5), close-fit clearance (3.2/4.3/5.3), 5.00 locating
    fit, and NEAR-MISS sizes that are probably un-updated holes. Inside corner radii of the
    outline are ignored; partial circles (slots, keyholes) are reported as arcs.
  - metal only: every plate except spacers has at least one tapped hole
  - minimum wall: the thinnest strip of material between two features, or a feature and the
    edge, on every flat level of the plate (catches webs too thin to cut)
  - with a reference: each hole matched by position to the reference plate, reporting changes
    in diameter, depth/steps, or holes that exist on only one side
"""
import glob
import math
import os
import re
import sys

import Part

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
VARIANT = os.environ["PLATE_VARIANT"]
REF = os.environ.get("PLATE_REF") or None
ONLY = os.environ.get("PLATE_ONLY") or ""
OUT = os.environ.get("PLATE_OUT") or ""
MIN_WALL = float(os.environ.get("PLATE_MIN_WALL") or 1.5)
TOL = 0.02
TAP = {1.6: "M2 tap", 2.5: "M3 tap"}
CLEAR = {3.2: "M3 clr", 4.3: "M4 clr", 5.3: "M5 clr"}
FIT = {5.0: "5.00 fit"}
NEAR = [(1.5, 1.8), (2.3, 2.7), (2.9, 3.8), (4.0, 4.9), (5.05, 5.9)]
IS_METAL = "metal" in VARIANT.lower()
VERBOSE = bool(os.environ.get("PLATE_VERBOSE"))
# Reference sizes that are precision fits and must survive into the checked variant:
# 5.00 D5 shoulder-bolt shoulders, 13.00 F695 bearing bores, 22.00 NEMA 17 boss.
PRESERVE = (5.0, 13.0, 22.0)
NO_TAP_NEEDED = ("Spacer", "Lever")


def role(d):
    for table in (TAP, CLEAR, FIT):
        for size, name in table.items():
            if abs(d - size) <= TOL:
                return name
    for lo, hi in NEAR:
        if lo <= d <= hi:
            return "NEAR-MISS"
    return ""


def load_accepted():
    p = os.path.join(os.path.dirname(os.path.abspath(__file__)), "plate_accepted.json")
    if not os.path.exists(p):
        return []
    import json
    with open(p, encoding="utf-8") as f:
        return json.load(f).get("accepted", [])


ACCEPTED = load_accepted()


def is_accepted(plate, kind, x, y, value):
    """An accepted entry matches the same plate and kind, within 1 mm of its location and
    0.05 mm of its recorded value. If the geometry changes, the finding comes back."""
    for a in ACCEPTED:
        if a["plate"] == plate and a["kind"] == kind and math.hypot(a["x"] - x, a["y"] - y) <= 1.0 \
                and abs(a["value"] - value) <= 0.05:
            return a.get("note", "accepted")
    return None


def expected_thickness(name):
    m = re.findall(r"(\d+(?:\.\d+)?)\s*mm", name)
    return float(m[-1]) if m else None


class Plate:
    def __init__(self, path):
        self.path = path
        self.name = os.path.splitext(os.path.basename(path))[0]
        s = Part.Shape()
        s.read(path)
        self.shape = s
        planes = [f for f in s.Faces if isinstance(f.Surface, Part.Plane)]
        self.n = n = max(planes, key=lambda f: f.Area).normalAt(0, 0)
        self.levels = [f for f in planes if abs(abs(f.normalAt(0, 0).dot(n)) - 1) < 1e-6]
        offs = [f.CenterOfMass.dot(n) for f in self.levels]
        self.thickness = max(offs) - min(offs)
        outer_faces = [f for f in self.levels if min(abs(f.CenterOfMass.dot(n) - o) for o in (max(offs), min(offs))) < 1e-6]
        self.outline = [e for f in outer_faces for e in f.OuterWire.Edges]
        outline_pts = [e.CenterOfMass for e in self.outline]
        self.holes = {}  # (x, y) -> {diameter: [zlo, zhi, sweep]}
        for f in s.Faces:
            if not isinstance(f.Surface, Part.Cylinder) or abs(abs(f.Surface.Axis.dot(n)) - 1) > 1e-6 or f.Area < 1e-6:
                continue
            if any(e.CenterOfMass.distanceToPoint(q) < 1e-3 for e in f.Edges for q in outline_pts):
                continue  # inside corner radius of the outline
            c = f.Surface.Center
            u0, u1, v0, v1 = f.ParameterRange
            mid = f.valueAt((u0 + u1) / 2, (v0 + v1) / 2)
            t = c - mid
            t = t - n * t.dot(n)
            if f.normalAt((u0 + u1) / 2, (v0 + v1) / 2).dot(t) <= 0:
                continue  # convex surface, not a hole
            zs = [v.Point.dot(n) for v in f.Vertexes] or [0.0]
            key = self._key(c)
            d = round(2 * f.Surface.Radius, 3)
            seg = self.holes.setdefault(key, {}).setdefault(d, [min(zs), max(zs), 0.0])
            seg[0], seg[1], seg[2] = min(seg[0], min(zs)), max(seg[1], max(zs)), seg[2] + math.degrees(u1 - u0)
        self.zmin = min(offs)

    def _key(self, c):
        # Snap to an existing key within 0.05 mm so split faces merge.
        for k in getattr(self, "holes", {}):
            if abs(k[0] - c.x) < 0.05 and abs(k[1] - c.y) < 0.05:
                return k
        return (round(c.x, 2), round(c.y, 2))

    def describe(self, key):
        segs = sorted(self.holes[key].items(), key=lambda kv: -kv[1][1])  # from the top face down
        out = []
        for d, (lo, hi, sweep) in segs:
            label = role(d)
            arc = "" if sweep >= 300 else " arc"
            out.append(f"Ø{d:.2f}x{hi - lo:.1f}{arc}" + (f" [{label}]" if label else ""))
        return " + ".join(out)

    def min_walls(self):
        """Thinnest material between distinct boundaries on each flat level.
        Returns sorted (gap, p1, p2, kind): kind 'through' if the same wall shows on both outer
        faces (full plate depth), else 'lip N.N mm' with the depth of the level it was found on."""
        if hasattr(self, "_walls"):
            return self._walls
        offs = [f.CenterOfMass.dot(self.n) for f in self.levels]
        top, bottom = max(offs), min(offs)
        found = []
        for f in self.levels:
            lvl = f.CenterOfMass.dot(self.n)
            wires = f.Wires
            for i in range(len(wires)):
                for j in range(i + 1, len(wires)):
                    a, b = wires[i], wires[j]
                    if (a.BoundBox.Center - b.BoundBox.Center).Length < 0.05 and \
                            abs(a.BoundBox.DiagonalLength - b.BoundBox.DiagonalLength) > 0.1:
                        continue  # concentric rings of one stepped hole: a ledge, not a wall
                    dist, pts, _ = a.distToShape(b)
                    if dist < MIN_WALL - 0.005:
                        found.append((dist, pts[0][0], pts[0][1], lvl))
        found.sort(key=lambda t: t[0])
        walls = []
        for dist, p1, p2, lvl in found:
            mid = (p1 + p2) * 0.5
            same = [w for w in walls if math.hypot(w[4].x - mid.x, w[4].y - mid.y) < 1.0]
            if same:
                same[0][5].add(round(lvl, 3))
                continue
            walls.append([dist, p1, p2, None, mid, {round(lvl, 3)}])
        out = []
        for dist, p1, p2, _, mid, lvls in walls:
            if round(top, 3) in lvls and round(bottom, 3) in lvls:
                kind = "through"
            else:
                # Only on one level: a rim around a pocket/counterbore rather than a full-depth web.
                depth = max(top - lvl for lvl in lvls)
                kind = "lip at top face" if depth < 1e-3 else (
                    "lip at bottom face" if abs(depth - (top - bottom)) < 1e-3 else f"lip {depth:.1f} mm below top")
            out.append((dist, p1, p2, kind))
        self._walls = out
        return out


# Plate files can be stored in any orientation (a plate can be flipped or turned before cutting),
# so holes are matched under whichever of these maps lines up the most of them.
ORIENTATIONS = {"as stored": (1, 1), "mirrored X": (-1, 1), "mirrored Y": (1, -1), "rotated 180": (-1, -1)}


def match(plate, ref):
    best = None
    for label, (sx, sy) in ORIENTATIONS.items():
        pairs, used = [], set()
        for k in plate.holes:
            t = (k[0] * sx, k[1] * sy)
            r = min(ref.holes, key=lambda h: (h[0] - t[0]) ** 2 + (h[1] - t[1]) ** 2, default=None)
            if r is not None and math.hypot(r[0] - t[0], r[1] - t[1]) < 0.1 and r not in used:
                used.add(r)
                pairs.append((k, r))
            else:
                pairs.append((k, None))
        pairs += [(None, r) for r in ref.holes if r not in used]
        score = len(used)
        if best is None or score > best[0]:
            best = (score, label, pairs)
    return best[1], best[2]


def ref_path_for(name):
    if not REF:
        return None
    stem = re.sub(r"(Metal|CF|Printed)\s*\d+(\.\d+)?mm$", "", name).strip()
    for p in glob.glob(os.path.join(ROOT, REF, "Base Components", "*.step")):
        if re.sub(r"(Metal|CF|Printed)\s*\d+(\.\d+)?mm$", "", os.path.splitext(os.path.basename(p))[0]).strip() == stem:
            return p
    return None


def draw(plate, marks, dst):
    from PySide2 import QtCore, QtGui
    QtGui.QGuiApplication.instance() or QtGui.QGuiApplication(sys.argv[:1])
    bb = plate.shape.BoundBox
    W, PAD = 1800, 90
    scale = (W - 2 * PAD) / max(bb.XLength, 1e-6)
    H = int(bb.YLength * scale + 2 * PAD)
    px = lambda x, y: QtCore.QPointF(PAD + (x - bb.XMin) * scale, H - PAD - (y - bb.YMin) * scale)
    img = QtGui.QImage(W, H, QtGui.QImage.Format_RGB32)
    img.fill(QtCore.Qt.white)
    p = QtGui.QPainter(img)
    p.setRenderHint(QtGui.QPainter.Antialiasing)
    p.setPen(QtGui.QPen(QtGui.QColor("#222"), 3))
    top = max(plate.levels, key=lambda f: (round(f.CenterOfMass.dot(plate.n), 3), f.Area))
    for f in plate.levels:  # draw every level so steps show
        pen = QtGui.QPen(QtGui.QColor("#222" if f.isSame(top) else "#999"), 3 if f.isSame(top) else 2)
        p.setPen(pen)
        for e in f.Edges:
            pts = [px(v.x, v.y) for v in e.discretize(Deflection=0.02)]
            for a, b in zip(pts, pts[1:]):
                p.drawLine(a, b)
    font = p.font()
    font.setPointSize(18)
    font.setBold(True)
    p.setFont(font)
    for i, (x, y, label) in enumerate(marks, start=1):
        c = px(x, y)
        p.setPen(QtGui.QPen(QtGui.QColor("#e0115f"), 5))
        p.drawEllipse(c, 30, 30)
        p.drawText(c + QtCore.QPointF(34, -12), f"{i}: {label}")
    p.end()
    img.save(dst)


def check(path):
    plate = Plate(path)
    findings, marks, print_notes = [], [], []
    exp = expected_thickness(plate.name)
    sizes = [float(m) for m in re.findall(r"(\d+(?:\.\d+)?)\s*mm", plate.name)[:-1]]
    if exp is not None and abs(plate.thickness - exp) > 0.01:
        if any(abs(plate.thickness - s) <= 0.01 for s in sizes):
            # e.g. "XY Live Idler Spacer 5mm CF6mm": machined to 5 mm from 6 mm stock
            print_notes.append(f"machined to {plate.thickness:g} mm from {exp:g} mm stock (per the name)")
        else:
            findings.append(f"thickness {plate.thickness:.2f} mm, name says {exp:g}")
    bb = plate.shape.BoundBox
    if not all(lo - 1 <= 0 <= hi + 1 for lo, hi in ((bb.XMin, bb.XMax), (bb.YMin, bb.YMax), (bb.ZMin, bb.ZMax))):
        findings.append(f"not at 0,0,0 (X {bb.XMin:.1f}..{bb.XMax:.1f} Y {bb.YMin:.1f}..{bb.YMax:.1f} Z {bb.ZMin:.1f}..{bb.ZMax:.1f})")
    if "CF" in plate.name and "metal" in VARIANT.lower() or "6mm" in plate.name and "metal" in VARIANT.lower():
        findings.append("leftover CF/6mm in the name")

    roles = [role(d) for segs in plate.holes.values() for d in segs]
    taps = sum(r.endswith("tap") for r in roles)
    exempt = any(x in plate.name for x in NO_TAP_NEEDED)
    if IS_METAL and not exempt and not taps:
        findings.append("no tapped holes")
    if IS_METAL and exempt and taps:
        findings.append("has tapped holes but is a spacer")
    accepted = []

    def flag(kind, x, y, value, text, mark):
        note = is_accepted(plate.name, kind, x, y, value)
        if note is not None:
            accepted.append(f"{text}  -- {note}")
        else:
            findings.append(text)
            marks.append((x, y, mark))

    for k in plate.holes:
        for d in plate.holes[k]:
            if role(d) == "NEAR-MISS":
                flag("near-miss", k[0], k[1], d, f"near-miss Ø{d:.2f} at ({k[0]:.2f}, {k[1]:.2f})", f"Ø{d:.2f}")

    for gap, a, b, kind in plate.min_walls():
        mid = (a + b) * 0.5
        flag("wall", mid.x, mid.y, gap, f"THIN WALL {gap:.2f} mm ({kind}) near ({mid.x:.2f}, {mid.y:.2f})",
             f"{gap:.2f} {'thru' if kind == 'through' else 'lip'}")

    changes, other_changes = [], 0
    rp = ref_path_for(plate.name)
    if REF and not rp:
        findings.append(f"no matching plate in {REF}")
    elif rp:
        ref = Plate(rp)
        orientation, pairs = match(plate, ref)
        if orientation != "as stored":
            print_notes.append(f"stored {orientation} relative to the {REF} plate (compared in that orientation)")
        for k, r in pairs:
            kk = k or r
            where = f"({kk[0]:.2f}, {kk[1]:.2f})"
            if not k or not r:
                side = "only on this plate" if k else f"only on the {REF} plate"
                findings.append(f"hole {side} at {where}: {plate.describe(k) if k else ref.describe(r)}")
                marks.append((kk[0], kk[1], "only here" if k else "missing"))
                continue
            mine, theirs = plate.holes[k], ref.holes[r]
            if sorted(round(d, 2) for d in mine) == sorted(round(d, 2) for d in theirs):
                continue
            # Precision fits in the reference (full circles) must keep their size.
            lost = [d for d, (_, _, sw) in theirs.items() if sw >= 300 and any(abs(d - f) <= TOL for f in PRESERVE)
                    and not any(abs(d - m) <= TOL for m in mine)]
            if lost:
                flag("fit", kk[0], kk[1], lost[0], f"precision fit changed at {where}: {plate.describe(k)}  (was {ref.describe(r)})",
                     f"was Ø{lost[0]:.2f}")
            else:
                other_changes += 1
                changes.append(f"{where}  {plate.describe(k)}   <- {ref.describe(r)}")

    status = "OK" if not findings else f"{len(findings)} finding(s)"
    print(f"\n== {plate.name}   [{status}]")
    print(f"   thickness {plate.thickness:.2f} mm | {len(plate.holes)} holes | taps {taps} | "
          f"walls under {MIN_WALL:g} mm: {len(plate.min_walls())}")
    for note in print_notes:
        print(f"   i {note}")
    for f in findings:
        print(f"   ! {f}")
    for a in accepted:
        print(f"   ~ accepted: {a}")
    if other_changes:
        print(f"   {other_changes} other hole(s) differ from {REF} without touching a precision fit"
              f" (e.g. PEM->tap, clearance updates){': ' if VERBOSE else ''}")
        for c in changes if VERBOSE else []:
            print(f"     {c}")
    if marks and OUT:
        os.makedirs(OUT, exist_ok=True)
        dst = os.path.join(OUT, plate.name + ".png")
        draw(plate, marks, dst)
        print(f"   drawing: {dst}")
    return not findings


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    plates = sorted(glob.glob(os.path.join(ROOT, VARIANT, "Base Components", "*.step")))
    plates = [p for p in plates if ONLY.lower() in os.path.basename(p).lower()]
    print(f"Checking {len(plates)} plate(s) in {VARIANT}" + (f" against {REF}" if REF else ""))
    if REF and not ONLY:
        mine = {re.sub(r"(Metal|CF|Printed)\s*\d+(\.\d+)?mm$", "", os.path.splitext(os.path.basename(p))[0]).strip() for p in plates}
        theirs = {re.sub(r"(Metal|CF|Printed)\s*\d+(\.\d+)?mm$", "", os.path.splitext(os.path.basename(p))[0]).strip()
                  for p in glob.glob(os.path.join(ROOT, REF, "Base Components", "*.step"))}
        for missing in sorted(theirs - mine):
            print(f"! missing plate (exists in {REF}): {missing}")
    ok = sum(check(p) for p in plates)
    print(f"\nPLATE CHECK: {ok}/{len(plates)} plates with no findings")


if not os.environ.get("PLATE_NO_MAIN"):  # set when another script imports this one's helpers
    main()
