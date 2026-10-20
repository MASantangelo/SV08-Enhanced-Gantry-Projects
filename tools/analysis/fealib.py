"""Minimal gmsh + CalculiX pipeline: mesh a BREP, pick boundary and load nodes by geometry, solve, read results.

Both programs ship with FreeCAD 1.0. Work files go to SV08_ANALYSIS_DIR, which should be a short path:
CalculiX fails when its file paths pass Windows' 260-character limit.
"""
import os
import re
import subprocess

import numpy as np

BIN = os.environ.get("SV08_FREECAD_BIN", r"C:\Program Files\FreeCAD 1.0\bin")
WORK = os.environ["SV08_ANALYSIS_DIR"]


def mesh(brep, clmax=2.0, clmin=0.6, fragment=False):
    """Quadratic tets (straight-sided, so curved edges can't invert elements). With fragment=True the solids
    are fragmented first, so parts that touch share nodes (bonded contact)."""
    inp = os.path.join(WORK, "m.inp")
    src = os.path.join(WORK, "m.geo")
    # A different element size, or a looser tolerance for faces that touch, usually gets past a meshing failure.
    for tol, scale in ((0.001, 1.0), (0.001, 0.85), (0.001, 1.15), (0.05, 1.0), (0.05, 0.85), (0.05, 0.7)):
        if fragment:
            with open(src, "w") as f:
                f.write('SetFactory("OpenCASCADE");\nGeometry.ToleranceBoolean = %g;\nMerge "%s";\n'
                        'BooleanFragments{ Volume{:}; Delete; }{}\n' % (tol, brep.replace("\\", "/")))
        elif tol > 0.001:
            break
        if os.path.exists(inp):
            os.remove(inp)
        r = subprocess.run([os.path.join(BIN, "gmsh.exe"), src if fragment else brep, "-3", "-order", "2",
                            "-clmax", str(clmax * scale), "-clmin", str(clmin), "-setnumber", "Mesh.SecondOrderLinear", "1",
                            "-optimize_netgen", "-format", "inp", "-o", inp], capture_output=True)
        if (r.returncode == 0 or b"Done writing" in r.stdout) and has_tets(inp):
            break
    else:
        raise RuntimeError("gmsh could not mesh " + os.path.basename(brep))
    if not has_tets(inp):
        raise RuntimeError("gmsh could not mesh " + os.path.basename(brep))
    nodes, tets, elset = {}, [], []
    mode = cur = None
    for line in open(inp):
        if line.startswith("*"):
            u = line.upper()
            mode = "N" if u.startswith("*NODE") else ("E" if "C3D10" in u else None)
            if mode == "E":
                m = re.search(r"ELSET=(\w+)", line, re.I)
                cur = m.group(1) if m else "V"
            continue
        p = line.replace(",", " ").split()
        if not p:
            continue
        if mode == "N":
            nodes[int(p[0])] = [float(p[1]), float(p[2]), float(p[3])]
        elif mode == "E":
            tets.append([int(x) for x in p[:11]]); elset.append(cur)
    ids = np.array(sorted(nodes))
    return dict(ids=ids, xyz=np.array([nodes[i] for i in ids]), tets=np.array(tets), elset=np.array(elset))


def has_tets(inp):
    return os.path.exists(inp) and any("C3D10" in line.upper() for line in open(inp) if line.startswith("*"))


def bore_nodes(m, cx, cy, rmax=9.0, band=0.3):
    """Nodes on the innermost cylindrical wall around a vertical axis at (cx, cy), and that wall's radius."""
    d = m["xyz"]
    r = np.hypot(d[:, 0] - cx, d[:, 1] - cy)
    sel = r < rmax
    if not sel.any():
        return np.array([], int), None
    rmin = r[sel].min()
    return np.where(sel & (r < rmin + band))[0], rmin


def solve(m, mats, fixed_idx, loads):
    """mats: {elset name or '*': (E MPa, nu) or dict(ortho=9 engineering constants, angle=deg)}.
    fixed_idx: node indices held in x, y and z.
    loads: (node indices, force vector N, cx, cy). A bore load is spread over its nodes weighted by
    max(0, cos) between each node's radial direction and the force, i.e. onto the wall the shaft presses on.
    Returns nodal displacement (mm) and von Mises stress (MPa)."""
    job = os.path.join(WORK, "j")
    ids, xyz = m["ids"], m["xyz"]
    with open(job + ".inp", "w") as f:
        f.write("*NODE, NSET=NALL\n")
        for i, p in zip(ids, xyz):
            f.write(f"{i},{p[0]:.5f},{p[1]:.5f},{p[2]:.5f}\n")
        sets = sorted(set(m["elset"]))
        for s in sets:
            f.write(f"*ELEMENT, TYPE=C3D10, ELSET=E_{s}\n")
            for t in m["tets"][m["elset"] == s]:
                f.write(",".join(str(x) for x in t) + "\n")
        for s in sets:
            mat = mats.get(s, mats.get("*"))
            if isinstance(mat, dict):  # orthotropic, axis 1 at `angle` degrees from X in the XY plane
                a = np.radians(mat["angle"])
                c = mat["ortho"]
                f.write(f"*ORIENTATION, NAME=O_{s}\n{np.cos(a):.6f},{np.sin(a):.6f},0,{-np.sin(a):.6f},{np.cos(a):.6f},0\n"
                        f"*MATERIAL, NAME=M_{s}\n*ELASTIC, TYPE=ENGINEERING CONSTANTS\n"
                        f"{','.join(str(v) for v in c[:8])}\n{c[8]}\n"
                        f"*SOLID SECTION, ELSET=E_{s}, MATERIAL=M_{s}, ORIENTATION=O_{s}\n")
            else:
                E, nu = mat
                f.write(f"*MATERIAL, NAME=M_{s}\n*ELASTIC\n{E},{nu}\n*SOLID SECTION, ELSET=E_{s}, MATERIAL=M_{s}\n")
        f.write("*NSET, NSET=FIX\n")
        for k in range(0, len(fixed_idx), 12):
            f.write(",".join(str(ids[j]) for j in fixed_idx[k:k + 12]) + "\n")
        f.write("*BOUNDARY\nFIX,1,3\n*STEP\n*STATIC\n*CLOAD\n")
        for idx, F, cx, cy in loads:
            F = np.asarray(F, float)
            radial = xyz[idx, :2] - [cx, cy]
            radial /= np.linalg.norm(radial, axis=1)[:, None] + 1e-12
            w = np.clip(radial @ (F[:2] / (np.linalg.norm(F[:2]) + 1e-12)), 0, None)
            if w.sum() == 0:
                w = np.ones(len(idx))
            w /= w.sum()
            for j, wj in zip(idx, w):
                for d in range(3):
                    if wj > 0 and F[d]:
                        f.write(f"{ids[j]},{d + 1},{F[d] * wj:.6e}\n")
        f.write("*NODE FILE\nU\n*EL FILE\nS\n*END STEP\n")
    n = str(os.cpu_count() or 4)
    r = subprocess.run([os.path.join(BIN, "ccx.exe"), "j"], cwd=WORK, capture_output=True, text=True,
                       env=dict(os.environ, OMP_NUM_THREADS=n, CCX_NPROC_EQUATION_SOLVER=n))
    if "Job finished" not in r.stdout:
        raise RuntimeError(r.stdout[-2000:])
    return read_frd(job + ".frd", ids)


def read_frd(path, ids):
    pos = {n: i for i, n in enumerate(ids)}
    U = np.zeros((len(ids), 3)); S = np.zeros((len(ids), 6)); blk = None
    for line in open(path):
        if line.startswith(" -4"):
            blk = "U" if "DISP" in line else ("S" if "STRESS" in line else None)
        elif line.startswith(" -1") and blk:
            n = int(line[3:13])
            vals = [float(line[13 + 12 * k: 25 + 12 * k]) for k in range((len(line.rstrip()) - 13) // 12)]
            if n in pos:
                if blk == "U": U[pos[n]] = vals[:3]
                else: S[pos[n]] = vals[:6]
    sx, sy, sz, txy, tyz, tzx = S.T
    vm = np.sqrt(0.5 * ((sx - sy) ** 2 + (sy - sz) ** 2 + (sz - sx) ** 2) + 3 * (txy ** 2 + tyz ** 2 + tzx ** 2))
    return U, vm
