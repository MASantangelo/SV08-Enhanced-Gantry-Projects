"""Step 3: how stiffly each corner sandwich holds the end of its Y extrusion against vertical bending.

Model: both plates, the printed 20 mm spacer plate and Z carriage spacer, and a solid 20x20 stub with the bending
stiffness of a 2020 extrusion, all bonded (an upper bound on a bolted joint). Fixed at the two M4 x 45 bolts into
the Z carriage and on the Z carriage spacer's lower face. Each corner is run twice: bonded (a perfect clamp, the
best a through-bolt can do) and clamp patches (touching only at the bolts, what a loose T-nut joint tends toward).
A pure bending moment on the stub's free end; the
rotation of the stub where it leaves the plates gives the joint's rotational stiffness.
Writes corners_res.json into SV08_ANALYSIS_DIR.
"""
import json
import os
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import fealib
from materials import CF_ORTHO, MAT

WORK = fealib.WORK
meta = json.load(open(os.path.join(WORK, "corners.json")))
iso = lambda m: MAT[m][:2]
# per version: (case, plate material, printed spacer material). In CF and metal builds the spacer barely matters.
CASES = {"Printed": [("Printed ABS", iso("ABS"), iso("ABS")), ("Printed PC-CF15", iso("PC-CF15"), iso("PC-CF15"))],
         "CF": [("CF 0/90", dict(ortho=CF_ORTHO, angle=0), iso("ABS")), ("CF 45", dict(ortho=CF_ORTHO, angle=45), iso("ABS"))],
         "Metal": [("Metal", iso("6061-T6"), iso("ABS"))]}
BOLTS = {"Front": [(-227.5, -214.0), (-255.0, -214.0)], "Back": [(-227.5, 272.0), (-255.0, 272.0)]}
E_AL, I_2020 = 69000.0, 6936.0  # the stub is a solid box given a 2020 extrusion's bending stiffness
M0 = 1000.0  # N*mm

res = []
for key, c in meta.items():
    var, corner = key.split("_")[:2]
    model = c.get("model", "bonded")
    try:
        m = fealib.mesh(os.path.join(WORK, f"corner_{key}.brep"), clmax=2.5, clmin=0.8, fragment=True)
    except RuntimeError as e:
        print(f"CORNER {key}: skipped ({e})")
        continue
    xyz = m["xyz"]
    sets = sorted(set(m["elset"]))
    role = {}
    for s in sets:  # match each meshed volume to its part: centroids inside the part's box, then closest volume
        P = xyz[np.searchsorted(m["ids"], m["tets"][m["elset"] == s][:, 1:5])]
        cen = P.mean(1)
        vol = abs(np.einsum("ij,ij->i", np.cross(P[:, 1] - P[:, 0], P[:, 2] - P[:, 0]), P[:, 3] - P[:, 0])).sum() / 6

        def score(p):
            b = p["bb"]
            inside = np.all((cen > np.array(b[:3]) - .1) & (cen < np.array(b[3:]) + .1), axis=1).mean()
            return (-inside, abs(vol - p["vol"]))
        role[s] = min(c["parts"], key=score)["role"]
    _, count = np.unique(np.round(xyz, 4), axis=0, return_counts=True)
    if (count > 1).sum() > 50:
        print(f"CORNER {key}: skipped (parts not bonded: {(count > 1).sum()} duplicate nodes)")
        continue
    fix = [np.where(np.hypot(xyz[:, 0] - x, xyz[:, 1] - y) < 2.6)[0] for x, y in BOLTS[corner]]
    zs = next(p for p in c["parts"] if p["label"].startswith("Z Carriage"))["bb"]
    fix.append(np.where((abs(xyz[:, 2] - zs[2]) < 0.05) & np.all((xyz[:, :2] > np.array(zs[:2]) - .1)
                                                                  & (xyz[:, :2] < np.array(zs[3:5]) + .1), axis=1))[0])
    fix = np.unique(np.concatenate(fix))
    sx, sy, sz, dx, dy, dz = c["stub"]
    y_end = sy + dy if c["stub_dir"] > 0 else sy
    pl = [p for p in c["parts"] if p["role"] == "plate"]
    y_edge = max(p["bb"][4] for p in pl) if c["stub_dir"] > 0 else min(p["bb"][1] for p in pl)
    in_stub = (xyz[:, 0] > sx - .05) & (xyz[:, 0] < sx + dx + .05)
    end = np.where(in_stub & (abs(xyz[:, 1] - y_end) < 0.05))[0]
    sec = np.where(in_stub & (abs(xyz[:, 1] - y_edge) < 0.6) & (xyz[:, 2] > sz + 1) & (xyz[:, 2] < sz + dz - 1))[0]
    zc = xyz[end, 2].mean(); arm = xyz[end, 2] - zc
    loads = [(np.array([j]), [0, f, 0], 0, 0) for j, f in zip(end, M0 * arm / (arm ** 2).sum())]
    for case, plate_mat, spacer_mat in CASES[var]:
        e_stub = E_AL * I_2020 / (dx * dz ** 3 / 12)  # keeps a 2020's bending stiffness whatever the stub's height
        mats = {s: (plate_mat if role[s] == "plate" else spacer_mat if role[s] == "spacer"
                    else (69000, 0.33) if role[s] == "clamp" else (e_stub, 0.33)) for s in sets}
        try:
            U, _ = fealib.solve(m, mats, fix, loads)
        except RuntimeError:
            print(f"CORNER {key}: skipped (the mesh has inverted elements)")
            break
        theta = abs(np.polyfit(xyz[sec, 2], U[sec, 1], 1)[0])
        res.append(dict(case=case, corner=corner, model=model, k_rot=M0 / theta / 1000))
        print(f"CORNER {case:16s} {corner:5s} {model:6s} k = {M0 / theta / 1000:7.0f} N*m/rad")
json.dump(res, open(os.path.join(WORK, "corners_res.json"), "w"), indent=1)
