"""Step 4: predicted XY joint bench test. One left XY joint (plates, spacers and the steel shafts and standoffs tying
the plates together) with a 200 mm stub of 2020 in it, the MGN9 carriage side held fixed, 49 N (5 kg) hung on the stub's end: sideways (racking, in the plane of the plates) and vertically.

Bonded contacts and a rigidly held carriage, so this is the stiffest the joint can be; a real bolted joint adds a
little more. The bare-stub line is a 2020 extrusion fixed where it leaves the plates: the joint's own share is the
difference. Each joint is also run with the beam held only by clamp patches at its bolts (what a loose T-nut joint
tends toward); results for that model are named "<case> (patch)". Writes xyjoint_res.json into SV08_ANALYSIS_DIR.
"""
import json
import os
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import fealib
from materials import CF_ORTHO, MAT

WORK = fealib.WORK
meta = json.load(open(os.path.join(WORK, "xyjoints.json")))
F = 49.0  # N, 5 kg
I_2020, E_AL = 6936.0, 69000.0
iso = lambda m: MAT[m][:2]
# case: version, version plates and spacers, shared printed spacer
CASES = [("Printed ABS", "Printed", iso("ABS"), iso("ABS")),
         ("Printed PC-CF15", "Printed", iso("PC-CF15"), iso("PC-CF15")),
         ("CF 0/90", "CF", dict(ortho=CF_ORTHO, angle=0), iso("ABS")),
         ("CF 45", "CF", dict(ortho=CF_ORTHO, angle=45), iso("ABS")),
         ("Metal", "Metal", iso("6061-T6"), iso("ABS"))]

res = {}
meshes = {}
for (name, var, plate_mat, spacer_mat), model in [(c, m) for m in ("bonded", "patch") for c in CASES]:
    key = var if model == "bonded" else var + "_patch"
    if model == "patch":
        name = name + " (patch)"
    j = meta[key]
    if key not in meshes:
        try:
            meshes[key] = fealib.mesh(os.path.join(WORK, f"xyjoint_{key}.brep"), clmax=2.5, clmin=0.8, fragment=True)
        except RuntimeError as e:
            print(f"XYJOINT {key}: skipped ({e})"); meshes[key] = None
    m = meshes[key]
    if m is None:
        continue
    xyz = m["xyz"]
    sets = sorted(set(m["elset"]))
    role, part = {}, {}
    for s in sets:
        P = xyz[np.searchsorted(m["ids"], m["tets"][m["elset"] == s][:, 1:5])]
        cen = P.mean(1)
        vol = abs(np.einsum("ij,ij->i", np.cross(P[:, 1] - P[:, 0], P[:, 2] - P[:, 0]), P[:, 3] - P[:, 0])).sum() / 6
        part[s] = min(j["parts"], key=lambda p: (-np.all((cen > np.array(p["bb"][:3]) - .1) & (cen < np.array(p["bb"][3:]) + .1), axis=1).mean(),
                                                  abs(vol - p["vol"])))
        role[s] = part[s]["role"]
    c = j["carriage"]  # the MGN9 block sits on the bottom plate's top face
    fix = [np.where(np.hypot(xyz[:, 0] - x, xyz[:, 1] - y) < 1.9)[0] for x, y in j["bolts"]]
    fix.append(np.where((abs(xyz[:, 2] - c[2]) < 0.05) & (xyz[:, 0] > c[0]) & (xyz[:, 0] < c[3])
                        & (xyz[:, 1] > c[1]) & (xyz[:, 1] < c[4]))[0])
    fix = np.unique(np.concatenate(fix))
    sx, sy, sz, dx, dy, dz = j["stub"]
    end = np.where(abs(xyz[:, 0] - (sx + dx)) < 0.05)[0]
    edge = max(p["bb"][3] for p in j["parts"] if p["role"] == "plate")
    L = sx + dx - edge
    out = {}
    for mode, d in (("sideways", 1), ("vertical", 2)):
        # keep a 2020's bending stiffness in the loaded direction whatever the stub's cross-section
        e_stub = E_AL * I_2020 / ((dz * dy ** 3 if d == 1 else dy * dz ** 3) / 12)
        mats = {s: (plate_mat if role[s] == "plate" else spacer_mat if role[s] == "spacer"
                    else (part[s]["E"], 0.3) if role[s] == "post" else (69000, 0.33) if role[s] == "clamp"
                    else (e_stub, 0.33)) for s in sets}
        f = [0, 0, 0]; f[d] = F / len(end)
        U, _ = fealib.solve(m, mats, fix, [(np.array([k]), list(f), 0, 0) for k in end])
        out[mode] = float(U[end, d].mean() * 1000)
    bare = F * L ** 3 / (3 * E_AL * I_2020) * 1000
    res[name] = dict(free_length=L, bare_stub_um=bare, model=model, **out)
    print(f"XYJOINT {name:16s} free length {L:5.1f} mm: sideways {out['sideways']:6.1f} um, vertical {out['vertical']:6.1f} um"
          f"  (bare 2020 stub alone {bare:5.1f} um; joint adds {out['sideways'] - bare:5.1f} / {out['vertical'] - bare:5.1f})")
json.dump(res, open(os.path.join(WORK, "xyjoint_res.json"), "w"), indent=1)
