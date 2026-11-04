"""Step 2: FEA of every left-side plate of every version under its measured 8 lb idler loads, then how much
the plates' deflection lengthens the belt path compared with the belt's own stretch.

Each plate is held at the bolts that fix it to the extrusions, Z carriage or MGN9 carriage. Each idler load is
split between the top and bottom plate by belt height (the shaft is a lever between the two bores).
Writes plates_res.json, belt_path.json and <plate>_res.npz (for figures) into SV08_ANALYSIS_DIR.
"""
import json
import math
import os
import re
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import fealib
from materials import BELT_LOOP, CASES, EA_BELT, EA_SCALE, MAT, PRINTED, T_BELT

WORK = fealib.WORK
plates = json.load(open(os.path.join(WORK, "plates.json")))
IDLERS = {"*": json.load(open(os.path.join(WORK, "idlers.json"))),
          "CF9": json.load(open(os.path.join(WORK, "idlers_CF9.json")))}  # the 9mm mod's belts run at other heights
PAIRS = [("FrontLeftBottom", "FrontLeftTop"), ("BackLeftBottomPlate", "BackLeftTopPlate"),
         ("XYLiveIdlerLeftBottomPlate", "XYLiveIdlerLeftTopPlate")]
OTHER = {a: b for a, b in PAIRS} | {b: a for a, b in PAIRS}
FIXING = re.compile(r"^(M4x\d+(mm)? BHCS|M3x10mm BHCS)")  # frame and carriage bolts; M3x10 only at the XY joints


def tag(case):
    return case.replace(" ", "").replace("/", "-")


def zmid(key):
    b = plates[key]["bb"]
    return (b[2] + b[5]) / 2


res = {}
for key, meta in plates.items():
    var, name = key.split("_", 1)
    idlers = IDLERS.get(var, IDLERS["*"])
    b = meta["bb"]
    zb, zt = sorted((zmid(key), zmid(f"{var}_{OTHER[name]}")))
    is_bottom = zmid(key) == zb
    inside = lambda x, y, pad=0.5: b[0] - pad < x < b[3] + pad and b[1] - pad < y < b[4] + pad
    fixes = []
    for p in json.load(open(os.path.join(WORK, f"parts_{var}.json"))):
        q = p["bb"]; cx, cy = (q[0] + q[3]) / 2, (q[1] + q[4]) / 2
        if not FIXING.match(p["label"]) or not inside(cx, cy) or q[5] < b[2] + 0.5 or q[2] > b[5] - 0.5:
            continue
        if p["label"].startswith("M3x10mm") and not any("XY Joint" in s for s in p["parents"]):
            continue  # the M3 x 10 at a front corner is the tensioner pivot, not a fixing
        fixes.append((cx, cy))
    m = fealib.mesh(os.path.join(WORK, key + ".brep"))
    fix_idx = np.unique(np.concatenate([fealib.bore_nodes(m, x, y, rmax=3.5)[0] for x, y in fixes]))
    loads = []
    for i in idlers:
        if not i["asm"].endswith("L") or not inside(i["x"], i["y"], -2):
            continue
        share = (zt - i["z"]) / (zt - zb) if is_bottom else (i["z"] - zb) / (zt - zb)
        idx, r = fealib.bore_nodes(m, i["x"], i["y"], rmax=8)
        if len(idx):
            loads.append((idx, np.array([i["fx"], i["fy"], 0]) * share, i["x"], i["y"], r))
    xyz = m["xyz"]
    near_bolt = np.min(np.hypot(xyz[:, None, 0] - np.array(fixes)[None, :, 0], xyz[:, None, 1] - np.array(fixes)[None, :, 1]), axis=1) < 4.5
    near_bore = np.min([np.hypot(xyz[:, 0] - x, xyz[:, 1] - y) - (r + 3) for _, _, x, y, r in loads], axis=0) < 0
    for case, (cv, mat) in CASES.items():
        if cv != var:
            continue
        U, vm = fealib.solve(m, {"*": mat}, fix_idx, [l[:4] for l in loads])
        k = f"{case}|{name}"
        res[k] = dict(
            bolts=len(fixes),
            loads=[dict(x=x, y=y, F=float(np.linalg.norm(F)), u=float((U[idx] @ (F / np.linalg.norm(F))).mean() * 1000))
                   for idx, F, x, y, _ in loads],
            u_peak_um=float(np.linalg.norm(U, axis=1).max() * 1000),
            vm_peak=float(vm.max()), vm_away=float(vm[~near_bolt & ~near_bore].max()))
        np.savez(os.path.join(WORK, f"{tag(case)}_{name}_res.npz"), xyz=xyz, U=U, vm=vm)
        print(f"PLATE {case:11s} {name:27s} {len(fixes)} bolts, {len(loads)} loads: peak {res[k]['u_peak_um']:6.2f} um, "
              f"stress {res[k]['vm_away']:4.1f} MPa away from bolts and bores ({vm.max():4.1f} at them)")
json.dump(res, open(os.path.join(WORK, "plates_res.json"), "w"), indent=1)

# ---- belt path lengthening: each shaft moves by the lever-weighted bore displacements ----
print("\nBelt path lengthening from plate deflection (one belt loop = every left-side idler, by symmetry)")
path = {}
for case, (var, _) in CASES.items():
    idlers = IDLERS.get(var, IDLERS["*"])
    dL = 0.0
    for bot, top in PAIRS:
        kb, kt = f"{case}|{bot}", f"{case}|{top}"
        zb, zt = zmid(f"{var}_{bot}"), zmid(f"{var}_{top}")
        for i in idlers:
            if not i["asm"].endswith("L"):
                continue
            look = lambda k: next((q["u"] for q in res[k]["loads"] if abs(q["x"] - i["x"]) < .5 and abs(q["y"] - i["y"]) < .5), 0.0)
            ub, ut = look(kb), look(kt)
            if ub == 0 and ut == 0:
                continue
            sb = (zt - i["z"]) / (zt - zb)
            dL += (sb * ub + (1 - sb) * ut) / 1000 * 2 * math.sin(math.radians(i["ang"]) / 2)
    path[case] = dL
stretch = [T_BELT * BELT_LOOP / ea for ea in EA_BELT]
rows = ([(m, path["Printed ABS"] * MAT["ABS"][0] / MAT[m][0]) for m in PRINTED]
        + [(c, path[c]) for c in CASES if not c.startswith("Printed")])
out = {}
for name, dL in rows:
    st = [s / EA_SCALE.get(name, 1.0) for s in stretch]  # a stiffer (wider) belt stretches less
    out[name] = dict(dL_um=dL * 1000, compliance_added=[dL / s for s in st])
    print(f"  {name:9s} {dL * 1000:6.1f} um -> adds {dL / st[0] * 100:4.2f}-{dL / st[1] * 100:4.2f} % "
          f"to the belt's compliance (EA {EA_BELT[0]}-{EA_BELT[1]} N x {EA_SCALE.get(name, 1.0)})")
json.dump(out, open(os.path.join(WORK, "belt_path.json"), "w"), indent=1)
