"""Wall sweep for flat parts, measured directly on the solid (complements plate_check.py).

Run with FreeCAD's freecadcmd (plate-check.ps1 runs it after plate_check.py). Settings come from
env vars, because freecadcmd doesn't pass script arguments through reliably:
  PLATE_VARIANT        variant folder, e.g. "Metal Version" (or "Shared Components")
  PLATE_FOLDER         subfolder with the parts (default "Base Components"),
                       e.g. "Base Components\\Print Ready" or "Print Ready"
  PLATE_ONLY           optional: only parts whose name contains this text
  PLATE_MIN_WALL       thinnest allowed material (mm, default 1.5)
  PLATE_WALL_MULTIPLE  optional, for printed parts: every wall up to PLATE_WALL_MAX must be an
                       exact multiple of this (your line width, e.g. 0.4 or 0.45)
  PLATE_WALL_MAX       widest wall the multiple rule applies to (mm, default 4.0); wider walls are
                       mostly infill
  PLATE_LAYER_HEIGHT   optional, for printed parts: the thickness and every flat level (floors,
                       steps) must be a multiple of this (e.g. 0.2 or 0.15), measured from the bed

plate_check.py measures walls between separate features. This sweep also catches material between
pockets that merge into one opening (for example a bearing step overlapping a motor-boss recess),
where knife-edge tips and thin tongues form. For every part:
  - in-plane walls: the part is sectioned at every distinct level (midway between horizontal
    faces) and every 0.1 mm through sloped faces (countersinks, chamfers). In each section, any
    two boundary edges that are not neighbours count as a wall if the gap between their closest
    points is material and meets at least one edge squarely. Walls under the minimum are THIN
    WALLs; with a wall multiple, walls off that grid are OFF-GRID WALLs.
  - floors: each pocket floor or ceiling vs the nearest opposite face over the same area.
  - with a layer height: flat levels that aren't on a layer boundary are OFF-LAYER HEIGHTs.
Findings within 1.5 mm of each other (and of the same width) are one wall, reported at its
thinnest point. Parts are laid flat on their largest face, except with a layer height, where the
file's own Z is the build direction (print-ready files are already oriented for printing).
Accepted findings are listed in plate_accepted.json (kinds "wall", "floor", "grid", "layer"),
shared with plate_check.py.
"""
import glob
import math
import os
import sys

import FreeCAD
import Part

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
VARIANT = os.environ["PLATE_VARIANT"]
FOLDER = os.environ.get("PLATE_FOLDER") or "Base Components"
ONLY = os.environ.get("PLATE_ONLY") or ""
MIN = float(os.environ.get("PLATE_MIN_WALL") or 1.5)
GRID = float(os.environ.get("PLATE_WALL_MULTIPLE") or 0) or None
GRID_MAX = float(os.environ.get("PLATE_WALL_MAX") or 4.0)
LAYER = float(os.environ.get("PLATE_LAYER_HEIGHT") or 0) or None
TOL = 0.005  # how far off a multiple still counts as on it (CAD rounding)
SLOPE_STEP = 0.1
MERGE = 1.5
V = FreeCAD.Vector

os.environ["PLATE_NO_MAIN"] = "1"  # reuse plate_check's accepted-list matching without running it
sys.path.insert(0, HERE)
from plate_check import is_accepted  # noqa: E402


def off_grid(value, step):
    """Distance from value to the nearest multiple of step (0 when it's on the grid)."""
    k = round(value / step)
    return abs(value - k * step) if k > 0 else value


def neighbours(value, step):
    lo = math.floor(value / step + 1e-9) * step
    return lo, lo + step


def orient(shape):
    """Copy of the part lying flat on XY, plus the matrix back to file coordinates."""
    if LAYER:
        return shape.copy(), FreeCAD.Matrix()  # print-ready: keep the build direction
    planes = [f for f in shape.Faces if isinstance(f.Surface, Part.Plane)]
    n = max(planes, key=lambda f: f.Area).normalAt(0, 0)
    rot = FreeCAD.Rotation(n, V(0, 0, 1))
    m = FreeCAD.Placement(V(), rot).toMatrix()
    s = shape.copy()
    if abs(rot.Angle) > 1e-9:
        s.transformShape(m)  # rigid move; keeps planes as planes (transformGeometry can turn them into B-splines)
    return s, m.inverse()


def flat_levels(s):
    """Distinct heights of horizontal faces above the part's bottom, with one face centre each."""
    z0 = s.BoundBox.ZMin
    out = {}
    for f in s.Faces:
        if isinstance(f.Surface, Part.Plane) and f.BoundBox.ZLength < 1e-6:
            h = round(f.BoundBox.ZMin - z0, 4)
            if h > 1e-6:
                out.setdefault(h, f.CenterOfMass)
    return out


def section_levels(s):
    b = s.BoundBox
    zs = {round(b.ZMin, 4), round(b.ZMax, 4)}
    sloped = []
    for f in s.Faces:
        fb = f.BoundBox
        zs.update((round(fb.ZMin, 4), round(fb.ZMax, 4)))
        if fb.ZLength < 1e-6 or isinstance(f.Surface, Part.Cylinder):
            continue  # horizontal faces and vertical walls don't change the section
        if isinstance(f.Surface, Part.Plane) and abs(f.normalAt(0, 0).z) < 1e-6:
            continue
        sloped.append((fb.ZMin, fb.ZMax))
    zs = sorted(zs)
    out = [(a + c) / 2 for a, c in zip(zs, zs[1:]) if c - a > 1e-3]
    for lo, hi in sloped:
        z = lo + SLOPE_STEP / 2
        while z < hi:
            out.append(z)
            z += SLOPE_STEP
    return sorted(set(round(z, 4) for z in out))


def squarely(e, p, d):
    """True if direction d leaves edge e at p roughly at right angles (a wall, not a corner)."""
    if any(v.Point.distanceToPoint(p) < 1e-4 for v in e.Vertexes):
        return False
    try:
        t = e.tangentAt(e.Curve.parameter(p))
    except Exception:
        return False
    return t.Length > 1e-9 and abs(t.normalize().dot(d)) < 0.15


def section_walls(s, z, limit):
    wires = s.slice(V(0, 0, 1), z)
    if not wires:
        return []
    face = Part.makeFace(wires, "Part::FaceMakerBullseye")
    edges = face.Edges
    boxes = [e.BoundBox for e in edges]
    out = []
    for i in range(len(edges)):
        for j in range(i + 1, len(edges)):
            bi, bj = boxes[i], boxes[j]
            if bi.XMin - bj.XMax > limit or bj.XMin - bi.XMax > limit or bi.YMin - bj.YMax > limit or bj.YMin - bi.YMax > limit:
                continue
            a, b = edges[i], edges[j]
            if any(va.Point.distanceToPoint(vb.Point) < 1e-6 for va in a.Vertexes for vb in b.Vertexes):
                continue  # neighbours
            d, pts, _ = a.distToShape(b)
            if d < 1e-4 or d >= limit:
                continue
            p, q = pts[0]
            mid = (p + q) * 0.5
            if not face.isInside(mid, 1e-4, False):
                continue  # a gap, not material
            dirv = (q - p).normalize()
            if squarely(a, p, dirv) or squarely(b, q, dirv):
                out.append((d, mid))
    return out


def walls(s, inv):
    """Merged walls narrower than the minimum, or (with a wall multiple) up to the multiple's limit."""
    limit = max(MIN - 1e-3, GRID_MAX + TOL if GRID else 0)
    hits = []
    for z in section_levels(s):
        for d, mid in section_walls(s, z, limit):
            if d >= MIN - 1e-3 and not (GRID and off_grid(d, GRID) > TOL):
                continue  # thick enough and on the grid
            p = inv.multVec(V(mid.x, mid.y, mid.z))
            hits.append((d, p.x, p.y, z - s.BoundBox.ZMin))
    merged = []  # thinnest first, so each wall is reported at its thinnest point
    for d, x, y, z in sorted(hits):
        for w in merged:
            same_width = d < MIN - 1e-3 if w["d"] < MIN - 1e-3 else abs(w["d"] - d) < 0.01
            if same_width and math.hypot(w["x"] - x, w["y"] - y) < MERGE:
                w["lo"], w["hi"] = min(w["lo"], z), max(w["hi"], z)
                break
        else:
            merged.append({"d": d, "x": x, "y": y, "lo": z, "hi": z})
    return merged


def floors(s, inv):
    """Material thickness along Z under every upward-facing flat face (and so over every
    downward-facing one): sample points on the face and find the nearest downward-facing flat
    face directly below each. Sampling avoids booleans between faces, which fail silently on
    some merged pocket floors."""
    up, down = [], []
    for f in s.Faces:
        if isinstance(f.Surface, Part.Plane) and f.BoundBox.ZLength < 1e-6:
            (up if f.normalAt(0, 0).z > 0 else down).append(f)
    out = []
    for fu in up:
        zu = fu.BoundBox.ZMin
        below = [fd for fd in down if fd.BoundBox.ZMin < zu - 1e-6]
        pts, tris = fu.tessellate(0.2)
        samples = [(pts[a] + pts[b] + pts[c]) * (1 / 3) for a, b, c in tris] + list(pts)
        thin = []
        for p in samples:
            depth = None
            for fd in below:
                zd = fd.BoundBox.ZMin
                if depth is not None and zu - zd >= depth:
                    continue
                if fd.isInside(V(p.x, p.y, zd), 1e-4, True):
                    depth = zu - zd
            if depth is not None and depth < MIN - 1e-3:
                thin.append((depth, p))
        if thin:
            d = min(t for t, _ in thin)
            cx = sum(p.x for _, p in thin) / len(thin)
            cy = sum(p.y for _, p in thin) / len(thin)
            q = inv.multVec(V(cx, cy, zu))
            out.append({"d": d, "x": q.x, "y": q.y, "area": fu.Area})
    return out


def check(path):
    name = os.path.splitext(os.path.basename(path))[0]
    shape = Part.Shape()
    shape.read(path)
    s, inv = orient(shape)
    t = s.BoundBox.ZLength
    findings, accepted = [], []

    def report(kind, x, y, value, text):
        note = is_accepted(name, kind, x, y, round(value, 2))
        (accepted if note else findings).append(f"{text}  -- {note}" if note else text)

    for w in walls(s, inv):
        depth = f"{w['lo']:.2f} mm up" if abs(w["hi"] - w["lo"]) < 1e-6 else f"{w['lo']:.2f} to {w['hi']:.2f} mm up"
        where = f"near ({w['x']:.2f}, {w['y']:.2f}), section at {depth} of {t:.2f}"
        if w["d"] < MIN - 1e-3:
            report("wall", w["x"], w["y"], w["d"], f"THIN WALL {w['d']:.2f} mm {where}")
        else:
            lo, hi = neighbours(w["d"], GRID)
            report("grid", w["x"], w["y"], w["d"],
                   f"OFF-GRID WALL {w['d']:.2f} mm {where} (multiples of {GRID:g}: {lo:.2f} / {hi:.2f})")
    for w in floors(s, inv):
        report("floor", w["x"], w["y"], w["d"], f"THIN FLOOR {w['d']:.2f} mm near ({w['x']:.2f}, {w['y']:.2f}) (on a {w['area']:.1f} mm2 face)")
    if LAYER:
        for h, c in sorted(flat_levels(s).items()):
            if off_grid(h, LAYER) > TOL:
                lo, hi = neighbours(h, LAYER)
                what = "thickness" if abs(h - t) < 1e-4 else "flat level"
                report("layer", c.x, c.y, h, f"OFF-LAYER HEIGHT {h:.2f} mm ({what}, face near ({c.x:.2f}, {c.y:.2f})); "
                                             f"layers of {LAYER:g}: {lo:.2f} / {hi:.2f}")
    print(f"\n== {name}   [{'OK' if not findings else 'CHECK'}]")
    for f in findings:
        print(f"   ! {f}")
    for a in accepted:
        print(f"   ~ accepted: {a}")
    return not findings


def main():
    folder = os.path.join(ROOT, VARIANT, FOLDER)
    parts = sorted(glob.glob(os.path.join(folder, "*.step")) + glob.glob(os.path.join(folder, "*.stp")))
    parts = [p for p in parts if ONLY.lower() in os.path.basename(p).lower()]
    rules = [f"minimum {MIN:g} mm"]
    if GRID:
        rules.append(f"walls up to {GRID_MAX:g} mm in multiples of {GRID:g}")
    if LAYER:
        rules.append(f"heights in layers of {LAYER:g}")
    print(f"Wall sweep of {len(parts)} part(s) in {os.path.join(VARIANT, FOLDER)} ({', '.join(rules)})")
    ok = sum(check(p) for p in parts)
    print(f"\nWALL CHECK: {ok}/{len(parts)} parts with no findings")


main()
