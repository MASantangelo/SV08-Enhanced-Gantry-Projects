"""Step 1 of the mechanical analysis: pull everything the analysis needs out of the three assembly STEPs.

Run with FreeCAD's freecadcmd (see analysis.ps1). Writes into SV08_ANALYSIS_DIR:
  parts_<Variant>.json   every solid: label, parent assemblies, volume, bounding box (assembly coordinates)
  idlers.json            every belt wrap: idler position, belt height, wrap angle, load vector at 8 lb
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
VARIANTS = ["Printed Version", "CF Version", "Metal Version"]
T_BELT = 35.6  # N, 8 lb
PLATES = ["Front Left Bottom", "Front Left Top", "Back Left Bottom Plate", "Back Left Top Plate",
          "XY Live Idler Left Bottom Plate", "XY Live Idler Left Top Plate"]
PLATE_TAGS = ("Printed6mm", "CF6mm", "Metal5mm")
# 2020 stub: x, y, z, dx, dy, dz. y/z are refitted to the plate and spacer faces of each version.
CORNERS = {
    "Front": dict(asm="Front Left Motor Assembly", stub=(-259, -208, 29.3, 20, 90, 20), stub_dir=+1),
    "Back": dict(asm="Back Left Motor Assembly", stub=(-259, 190, 29.3, 20, 71, 20), stub_dir=-1),
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


def corner_sandwich(doc, c):
    solids, roles = [], []
    for o in doc.Objects:
        if o.TypeId != "Part::Feature" or not any(p.Label.startswith(c["asm"]) for p in o.InListRecursive):
            continue
        L = o.Label
        if any(t in L for t in PLATE_TAGS) and "Lever" not in L:
            role = "plate"
        elif "Spacer Plate 20mm" in L or "Z Carriage Spacer" in L:
            role = "spacer"
        else:
            continue
        q = placed(o).Solids[0].copy()
        q.fix(1e-4, 1e-5, 1e-3)
        q = q.removeSplitter()
        solids.append(q.Solids[0]); roles.append((role, L))
    # fit the stub exactly between the plates and against the spacer plate's face
    x, y, z, dx, dy, dz = c["stub"]
    pl = sorted([s for s, r in zip(solids, roles) if r[0] == "plate"], key=lambda q: q.BoundBox.ZMin)
    sp = next(s for s, r in zip(solids, roles) if "Spacer Plate 20mm" in r[1])
    z0, z1 = pl[0].BoundBox.ZMax, pl[-1].BoundBox.ZMin
    y0, y1 = (sp.BoundBox.YMax, y + dy) if c["stub_dir"] > 0 else (y, sp.BoundBox.YMin)
    stub = (x, y0, z0, dx, y1 - y0, z1 - z0)
    solids.append(Part.makeBox(dx, y1 - y0, z1 - z0, App.Vector(x, y0, z0))); roles.append(("stub", "2020 stub"))
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
    return Part.Compound(fused.Solids), parts, stub


def xy_joint_sandwich(doc):
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
        if L.startswith("D5 M3x35mm Shoulder Bolt"):
            posts.setdefault(xy, set()).add("bolt")
        elif L.startswith("M3 Internally Threaded Spacer"):
            posts.setdefault(xy, set()).add("shaft")
        elif L.startswith("M5 Spacer 10mm OD"):
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
        if "shaft" in kinds: d, E = 16.0, 200000 * (5 / 16) ** 4        # 5 mm shaft in F695 bearings
        elif "standoff" in kinds: d, E = 10.0, 69000 + 200000 * (5 / 10) ** 4  # 10 mm aluminium standoff + D5 bolt
        else: d, E = 8.0, 200000 * (5 / 8) ** 4                          # D5 shoulder bolt through a printed spacer
        solids.append(Part.makeCylinder(d / 2, zg1 - zg0 + 2 * t, App.Vector(x, y, zg0 - t)))
        label = f"post {'+'.join(sorted(kinds))} ({x:.0f},{y:.0f})"
        roles.append(("post", label)); post_E[label] = E
    solids.append(Part.makeBox(stub[3], stub[4], stub[5], App.Vector(*stub[:3]))); roles.append(("stub", "2020 stub"))
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
for var in VARIANTS:
    v = var.split()[0]
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
    if v == "Metal":  # the belt path is the same in every version
        idlers = belt_wraps(doc)
    for cname, c in CORNERS.items():
        shape, parts, stub = corner_sandwich(doc, c)
        shape.exportBrep(os.path.join(WORK, f"corner_{v}_{cname}.brep"))
        corners[f"{v}_{cname}"] = dict(parts=parts, stub=stub, stub_dir=c["stub_dir"])
    shape, joints[v] = xy_joint_sandwich(doc)
    shape.exportBrep(os.path.join(WORK, f"xyjoint_{v}.brep"))
    App.closeDocument(doc.Name)
    print(f"GEOMETRY {var}: {len(rows)} solids")
json.dump(idlers, open(os.path.join(WORK, "idlers.json"), "w"), indent=1)
json.dump(plates, open(os.path.join(WORK, "plates.json"), "w"), indent=1)
json.dump(corners, open(os.path.join(WORK, "corners.json"), "w"), indent=1)
json.dump(joints, open(os.path.join(WORK, "xyjoints.json"), "w"), indent=1)
print(f"GEOMETRY {len(idlers)} belt wraps, {len(plates)} plates, {len(corners)} corners")
