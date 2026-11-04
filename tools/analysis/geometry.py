"""Step 1 of the mechanical analysis: pull everything the analysis needs out of the assembly STEPs (the three
versions, plus the 9mm belt mod, which is built on the CF plates).

Run with FreeCAD's freecadcmd (see analysis.ps1). Writes into SV08_ANALYSIS_DIR:
  parts_<Variant>.json   every solid: label, parent assemblies, volume, bounding box (assembly coordinates)
  idlers.json            every belt wrap: idler position, belt height, wrap angle, load vector at 8 lb
  idlers_CF9.json        the same for the 9mm belt mod (its belts run at different heights)
  plates.json + *.brep   the left-side plates of each version, in assembly coordinates
  corners.json + *.brep  front-left and back-left corner sandwiches (plates + printed spacers + 2020 stub),
                         fused so their shared faces mesh conformally
  xyjoints.json + *.brep the left XY joint (plates + spacers + 200 mm X-beam stub), as on a bench test
"""
import glob
import json
import math
import os

import FreeCAD as App
import Import  # noqa: F401  (registers the STEP importer)
import Part

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
WORK = os.environ["SV08_ANALYSIS_DIR"]
VARIANTS = {"Printed": "Printed Version", "CF": "CF Version", "Metal": "Metal Version", "CF9": "CF Version/9mm Belt Mod"}
T_BELT = 35.6  # N, 8 lb
PLATES = ["Front Left Bottom", "Front Left Top", "Back Left Bottom Plate", "Back Left Top Plate",
          "XY Live Idler Left Bottom Plate", "XY Live Idler Left Top Plate"]
PLATE_TAGS = ("Printed6mm", "CF6mm", "Metal5mm")
# The 2020 stub runs from the spacer plate to 40 mm past the plates, at the Y extrusion's height.
CORNERS = {
    "Front": dict(asm="Front Left Motor Assembly", stub_dir=+1),
    "Back": dict(asm="Back Left Motor Assembly", stub_dir=-1),
}


def placed(o):
    s = o.Shape.copy()
    s.Placement = o.getGlobalPlacement()
    return s


def box(s):
    b = s.BoundBox
    return [b.XMin, b.YMin, b.ZMin, b.XMax, b.YMax, b.ZMax]


def parents(o):
    return [p.Label for p in o.InListRecursive if p.TypeId == "App::Part"]


def belt_wraps(doc):
    """Slice each belt at its mid height; every arc is a wrap around an idler or pulley."""
    arcs = {}
    for o in doc.Objects:
        if o.TypeId != "Part::Feature" or "Belt" not in o.Label:
            continue
        s = placed(o)
        z = (s.BoundBox.ZMin + s.BoundBox.ZMax) / 2
        for w in s.slice(App.Vector(0, 0, 1), z):
            for e in w.Edges:
                c = e.Curve
                if not isinstance(c, Part.Circle) or not 4 < c.Radius < 15:
                    continue  # small arcs are the belt clamps at the toolhead
                key = (o.Label[:3], round(c.Center.x), round(c.Center.y))
                if key in arcs and arcs[key]["r"] >= c.Radius:
                    continue  # keep the outer face of the belt
                m = e.valueAt((e.FirstParameter + e.LastParameter) / 2)
                arcs[key] = dict(belt=o.Label, z=z, r=c.Radius, x=c.Center.x, y=c.Center.y,
                                 ang=math.degrees(e.LastParameter - e.FirstParameter), mx=m.x, my=m.y)
    out = []
    for a in arcs.values():
        dx, dy = a["x"] - a["mx"], a["y"] - a["my"]  # the belt pulls the idler away from its wrap
        n = math.hypot(dx, dy)
        F = 2 * T_BELT * math.sin(math.radians(a["ang"]) / 2)
        asm = ("Front" if a["y"] < -100 else "Back" if a["y"] > 150 else "XYjoint") + (" L" if a["x"] < 0 else " R")
        out.append(dict(asm=asm, belt=a["belt"], x=a["x"], y=a["y"], z=a["z"], ang=a["ang"], F=F,
                        fx=F * dx / n, fy=F * dy / n))
    return sorted(out, key=lambda i: (i["y"], i["x"]))


GAP, PATCH_R = 1.0, 4.6  # clamp-patch model: gap between extrusion and plates, radius of each bolt's clamped patch


def add_stub(solids, roles, stub, bolt_xy, patch):
    """The extrusion stub. Bonded: it fills the space between the plates (a perfect clamp, the best a through-bolt can
    do). Patch: it stops GAP short of each plate and touches it only through a disc at each bolt, roughly a
    joint clamped at its bolts and free everywhere else (what a loose T-nut joint tends toward)."""
    x, y, z, dx, dy, dz = stub
    if not patch:
        solids.append(Part.makeBox(dx, dy, dz, App.Vector(x, y, z))); roles.append(("stub", "2020 stub"))
        return stub
    for bx, by in bolt_xy:
        for zz in (z, z + dz - GAP):
            solids.append(Part.makeCylinder(PATCH_R, GAP, App.Vector(bx, by, zz))); roles.append(("clamp", "clamp patch"))
    s = (x, y, z + GAP, dx, dy, dz - 2 * GAP)
    solids.append(Part.makeBox(s[3], s[4], s[5], App.Vector(*s[:3]))); roles.append(("stub", "2020 stub"))
    return s


def bolt_positions(doc, asm, labels, near_x=None):
    out = set()
    for o in doc.Objects:
        if o.TypeId == "Part::Feature" and o.Label.startswith(labels) and any(p.Label.startswith(asm) for p in o.InListRecursive):
            b = placed(o).BoundBox
            x, y = round((b.XMin + b.XMax) / 2, 2), round((b.YMin + b.YMax) / 2, 2)
            if near_x is None or abs(x - near_x) < 2:
                out.add((x, y))
    return sorted(out)


def corner_sandwich(doc, c, patch=False):
    solids, roles = [], []
    for o in doc.Objects:
        if o.TypeId != "Part::Feature" or not any(p.Label.startswith(c["asm"]) for p in o.InListRecursive):
            continue
        L = o.Label
        if (any(t in L for t in PLATE_TAGS) and "Lever" not in L) or "5mm Spacer for" in L:
            role = "plate"  # 9mm belt mod: the 5 mm risers either side of the extrusion are cut from the plate stock
        elif "Spacer Plate" in L or "Z Carriage Spacer" in L:
            role = "spacer"
        else:
            continue
        q = placed(o).Solids[0].copy()
        q.fix(1e-4, 1e-5, 1e-3)
        q = q.removeSplitter()
        solids.append(q.Solids[0]); roles.append((role, L))
    # 9mm belt mod: merge each riser into the plate it sits on (same stock, clamped together); their shared faces
    # otherwise leave unbonded slivers
    main = [i for i, r in enumerate(roles) if r[0] == "plate" and "5mm Spacer for" not in r[1]]
    merged = []
    for i in [i for i, r in enumerate(roles) if "5mm Spacer for" in r[1]]:
        z = solids[i].BoundBox
        k = min(main, key=lambda m: min(abs(solids[m].BoundBox.ZMax - z.ZMin), abs(solids[m].BoundBox.ZMin - z.ZMax)))
        f = solids[k].fuse([solids[i]], 0.05).removeSplitter().Solids
        if len(f) == 1:
            solids[k] = f[0]; merged.append(i)
    keep = [i for i in range(len(roles)) if i not in merged]
    solids, roles = [solids[i] for i in keep], [roles[i] for i in keep]
    # fit the stub to the Y extrusion, snapped onto the faces it touches, and against the spacer plate, whose outer
    # side is flush with the extrusion (a stub even 0.01 mm off leaves a sliver face the mesher can't handle)
    ext = next(placed(o).BoundBox for o in doc.Objects if o.TypeId == "Part::Feature"
               and o.Label.startswith("Gantry Y-Axis") and placed(o).BoundBox.XMin < 0)
    pl = [s for s, r in zip(solids, roles) if r[0] == "plate"]
    sp = next(s for s, r in zip(solids, roles) if "Spacer Plate" in r[1])
    x, dx = sp.BoundBox.XMin, 20.0

    def snap(v, faces):
        f = min(faces, key=lambda f: abs(f - v))
        return f if abs(f - v) < 0.1 else v
    z0 = snap(ext.ZMin, [q.BoundBox.ZMax for q in solids])
    z1 = snap(ext.ZMax, [q.BoundBox.ZMin for q in solids])
    if c["stub_dir"] > 0:
        y0, y1 = sp.BoundBox.YMax, max(q.BoundBox.YMax for q in pl) + 40
    else:
        y0, y1 = min(q.BoundBox.YMin for q in pl) - 40, sp.BoundBox.YMin
    bolts = bolt_positions(doc, c["asm"], ("M4x10mm BHCS", "M4x16mm BHCS"), near_x=x + dx / 2)  # M4s into the Y extrusion
    zbolts = bolt_positions(doc, c["asm"], ("M4x45mm BHCS", "M4x55 BHCS", "M4x55mm BHCS"))  # M4s into the Z carriage
    stub = add_stub(solids, roles, (x, y0, z0, dx, y1 - y0, z1 - z0), bolts, patch)
    # remove overlaps (plates win, then spacers, then the stub) so every region belongs to one part
    for i in range(1, len(solids)):
        cut = solids[i].cut(Part.makeCompound(solids[:i])).Solids
        solids[i] = max(cut, key=lambda q: q.Volume)
    fused = solids[0].generalFuse(solids[1:])[0]
    parts = []
    for s in fused.Solids:
        hit = next((roles[j] for j, src in enumerate(solids) if all(abs(a - b) < 0.05 for a, b in zip(box(s), box(src)))),
                   None)
        if hit is None:
            hits = [roles[j] for j, src in enumerate(solids) if src.common(s).Volume > 0.5 * s.Volume]
            hit = (hits[0][0], hits[0][1] + " (overlap)") if hits else ("?", "?")
        parts.append(dict(role=hit[0], label=hit[1], bb=box(s), vol=s.Volume))
    return Part.Compound(fused.Solids), parts, stub, zbolts


def xy_joint_sandwich(doc, patch=False, shaft_d=15.4):
    """Left XY joint as on a bench: both plates, the spacers between them, the steel shafts and standoffs that tie
    the plates together, and a 200 mm stub of the X beam.

    The shafts sit in bearing seats or loose holes, so each is modelled as a post of a larger diameter whose ends
    land on solid plate (bonded), with its modulus scaled to keep the real part's bending stiffness."""
    solids, roles, carriage, bolts, ext, posts = [], [], None, [], None, {}
    for o in doc.Objects:
        if o.TypeId != "Part::Feature":
            continue
        L = o.Label
        if L.startswith("Toolhead X-Axis 2020"):
            ext = placed(o).BoundBox
        if not any(p.Label.startswith("XY Joint Left") for p in o.InListRecursive):
            continue
        s = placed(o)
        if "MGN9H" in L:
            carriage = box(s)
        elif L.startswith("M3x10mm BHCS"):
            bolts.append(((s.BoundBox.XMin + s.BoundBox.XMax) / 2, (s.BoundBox.YMin + s.BoundBox.YMax) / 2))
        xy = (round((s.BoundBox.XMin + s.BoundBox.XMax) / 2, 2), round((s.BoundBox.YMin + s.BoundBox.YMax) / 2, 2))
        if L.startswith("D5 M3x") and "Shoulder Bolt" in L:
            posts.setdefault(xy, set()).add("bolt")
        elif L.startswith("M3 Internally Threaded Spacer") or "Chicago Bolt" in L:  # live idler shaft
            posts.setdefault(xy, set()).add("shaft")
        elif L.startswith("M5 Spacer"):
            posts.setdefault(xy, set()).add("standoff")
        role =("plate" if any(t in L for t in PLATE_TAGS) else "spacer" if "XY Live Idler Spacer" in L else None)
        if role:
            q = s.Solids[0].copy(); q.fix(1e-4, 1e-5, 1e-3); q = q.removeSplitter()
            solids.append(q.Solids[0]); roles.append((role, L))
    below = [s for s in solids if s.BoundBox.ZMax <= ext.ZMin + 0.6 and s.BoundBox.XMax > ext.XMin + 5]
    z0 = max(s.BoundBox.ZMax for s in below)
    z1 = min(s.BoundBox.ZMin for s, r in zip(solids, roles) if r[0] == "plate" and s.BoundBox.ZMin > ext.ZMin)
    stub = (ext.XMin, ext.YMin, z0, 200.0, ext.YMax - ext.YMin, z1 - z0)
    main = sorted([i for i, r in enumerate(roles) if r[0] == "plate" and "Spacer" not in r[1]], key=lambda i: solids[i].BoundBox.ZMin)
    t = solids[main[0]].BoundBox.ZLength
    zg0, zg1 = solids[main[0]].BoundBox.ZMax, solids[main[-1]].BoundBox.ZMin  # gap between the two joint plates
    # Square the version's own spacers' corners up to the outline of the plate they sit on. In the 6 mm CF joint the
    # spacer's 3.0 mm corner radius and the bottom plate's 3.35 mm one touch the same edge at the same point and then
    # peel apart, leaving a sliver of plate face that tapers to zero width and can't be meshed. Filling it (same
    # material, about 0.1 mm^2) makes the spacer follow the plate's arc at each corner.
    for i in [i for i, r in enumerate(roles) if r[0] == "plate" and "Spacer" in r[1]]:
        sb = solids[i].BoundBox
        k = min(main, key=lambda m: min(abs(solids[m].BoundBox.ZMax - sb.ZMin), abs(solids[m].BoundBox.ZMin - sb.ZMax)))
        zt = solids[k].BoundBox.ZMax if solids[k].BoundBox.ZMax <= sb.ZMin + 0.05 else solids[k].BoundBox.ZMin
        # the plate's outline just inside the face the spacer sits on (a face can be split by pockets, a section can't)
        zc = zt - 0.05 if zt == solids[k].BoundBox.ZMax else zt + 0.05
        outline = Part.Face(max(solids[k].slice(App.Vector(0, 0, 1), zc), key=lambda w: Part.Face(w).Area))
        outline.translate(App.Vector(0, 0, sb.ZMin - outline.BoundBox.ZMin))
        prism = outline.extrude(App.Vector(0, 0, sb.ZLength))
        for cx, cy in ((sb.XMin, sb.YMin), (sb.XMax, sb.YMin), (sb.XMin, sb.YMax), (sb.XMax, sb.YMax)):
            corner = Part.makeBox(4, 4, sb.ZLength, App.Vector(min(cx, cx - 4 if cx == sb.XMax else cx),
                                                               min(cy, cy - 4 if cy == sb.YMax else cy), sb.ZMin))
            filler = prism.common(corner).cut(solids[i])
            if filler.Solids:
                f = solids[i].fuse(filler).removeSplitter().Solids
                if len(f) == 1:
                    solids[i] = f[0]
    # the version's own spacers are plate material: merge them into the bottom plate (saves a sliver-prone interface)
    merged = []
    for i in [i for i, r in enumerate(roles) if r[0] == "plate" and "Spacer" in r[1]]:
        f = solids[main[0]].fuse([solids[i]], 0.05).removeSplitter().Solids  # fuzzy: printed parts can sit 0.01 mm apart
        if len(f) == 1:
            solids[main[0]] = f[0]; merged.append(i)
    keep = [i for i in range(len(roles)) if i not in merged]
    solids, roles = [solids[i] for i in keep], [roles[i] for i in keep]
    post_E = {}
    for (x, y), kinds in posts.items():
        # (model diameter, E giving the real part's bending stiffness)
        if "shaft" in kinds: d, E = shaft_d, 200000 * (5 / shaft_d) ** 4  # 5 mm shaft in F695 bearings
        elif "standoff" in kinds: d, E = 10.0, 69000 + 200000 * (5 / 10) ** 4  # 10 mm aluminium standoff + D5 bolt
        else: d, E = 10.5, 200000 * (5 / 10.5) ** 4                      # D5 shoulder bolt (clear of the 8.3 mm relief)
        solids.append(Part.makeCylinder(d / 2, zg1 - zg0 + 2 * t, App.Vector(x, y, zg0 - t)))
        label = f"post {'+'.join(sorted(kinds))} ({x:.0f},{y:.0f})"
        roles.append(("post", label)); post_E[label] = E
    beam_bolts = bolt_positions(doc, "XY Joint Left", ("M4x20mm BHCS", "M4x10mm BHCS", "M4x16mm BHCS"))  # M4s into the X beam
    stub = add_stub(solids, roles, stub, beam_bolts, patch)
    for i in range(1, len(solids)):
        cut = solids[i].cut(Part.makeCompound(solids[:i])).Solids
        solids[i] = max(cut, key=lambda q: q.Volume)  # a post keeps its span between the plates
    fused = solids[0].generalFuse(solids[1:])[0]
    parts = []
    for s in fused.Solids:
        hits = [roles[j] for j, src in enumerate(solids) if src.common(s).Volume > 0.5 * s.Volume]
        r = hits[0] if hits else ("?", "?")
        parts.append(dict(role=r[0], label=r[1], bb=box(s), vol=s.Volume, E=post_E.get(r[1])))
    return Part.Compound(fused.Solids), dict(parts=parts, stub=stub, carriage=carriage, bolts=bolts)


plates, corners, idlers, joints = {}, {}, None, {}
for v, var in VARIANTS.items():
    doc = App.newDocument("a")
    Import.insert(glob.glob(os.path.join(ROOT, var, "*.step"))[0], doc.Name)
    rows = []
    for o in doc.Objects:
        if o.TypeId != "Part::Feature" or o.Shape.isNull() or not o.Shape.Solids:
            continue
        s = placed(o)
        rows.append(dict(label=o.Label, parents=parents(o), vol=s.Volume, bb=box(s)))
        for w in PLATES:
            key = f"{v}_{w.replace(' ', '')}"
            if o.Label.startswith(w) and key not in plates:
                s.exportBrep(os.path.join(WORK, key + ".brep"))
                plates[key] = dict(label=o.Label, bb=box(s), vol=s.Volume)
    json.dump(rows, open(os.path.join(WORK, f"parts_{v}.json"), "w"), indent=1)
    if v == "Metal":  # the belt path is the same in the three versions
        idlers = belt_wraps(doc)
    if v == "CF9":
        json.dump(belt_wraps(doc), open(os.path.join(WORK, "idlers_CF9.json"), "w"), indent=1)
    for model, patch in (("bonded", False), ("patch", True)):
        sfx = "" if model == "bonded" else "_patch"
        for cname, c in CORNERS.items():
            shape, parts, stub, zbolts = corner_sandwich(doc, c, patch)
            shape.exportBrep(os.path.join(WORK, f"corner_{v}_{cname}{sfx}.brep"))
            corners[f"{v}_{cname}{sfx}"] = dict(parts=parts, stub=stub, stub_dir=c["stub_dir"], model=model, zbolts=zbolts)
        if patch:
            continue  # the clamped-at-bolts XY joint has never meshed: not worth the time
        # The stand-in shaft post must clear the bearing-seat and relief circles in each version's plates; which size
        # meshes depends on the exact CAD, so export a few and let xyjoint.py use the first that meshes.
        alts = []
        for d in (15.4, 16.0, 14.6):
            shape, j = xy_joint_sandwich(doc, patch, shaft_d=d)
            f = f"xyjoint_{v}{sfx}_d{d:g}.brep"
            shape.exportBrep(os.path.join(WORK, f))
            alts.append(dict(j, file=f, shaft_d=d))
        joints[f"{v}{sfx}"] = dict(alts[0], model=model, alts=alts)
    App.closeDocument(doc.Name)
    print(f"GEOMETRY {var}: {len(rows)} solids")
json.dump(idlers, open(os.path.join(WORK, "idlers.json"), "w"), indent=1)
json.dump(plates, open(os.path.join(WORK, "plates.json"), "w"), indent=1)
json.dump(corners, open(os.path.join(WORK, "corners.json"), "w"), indent=1)
json.dump(joints, open(os.path.join(WORK, "xyjoints.json"), "w"), indent=1)
print(f"GEOMETRY {len(idlers)} belt wraps, {len(plates)} plates, {len(corners)} corners")
