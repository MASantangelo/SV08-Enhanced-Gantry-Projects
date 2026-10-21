"""Step 5: the gantry as a whole, using beam models of the extrusions and rails with the corner stiffness from
corners.py and the belt-path compliance from plates.py: masses and acceleration, gravity sag, vertical bounce,
XY belt resonance, gantry yaw, belt dynamics and tensioning, thermal bow at each chamber temperature, joint slip,
motor heat, creep and X beam buckling. Writes frame_res.json into SV08_ANALYSIS_DIR.
"""
import json
import math
import os
import sys

import numpy as np
from scipy.linalg import eigh

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from materials import (BELT_LOOP, CHAMBERS, EA_BELT, M_TOOL, MAT, MOTOR, MU_BELT, PLATE_TAG, PRINTED, PULLEY_R,
                       ROTOR_J, T_ASSEMBLY, T_BELT, T_RANGE)

WORK = os.environ["SV08_ANALYSIS_DIR"]
g = 9.81
E_AL, E_ST = 69000.0, 200000.0
I_2020 = 6936.0  # mm^4
load = lambda n: json.load(open(os.path.join(WORK, n)))
parts = {v: load(f"parts_{v}.json") for v in PLATE_TAG}
plates = load("plates.json")
corners = load("corners_res.json")
belt = load("belt_path.json")
xyj = load("xyjoint_res.json")
xyj_geo = load("xyjoints.json")["Metal"]
# XY joint as a spring: it pivots where the bottom plate leaves the MGN9 carriage. The bench load sits LEVER from
# that edge; the X beam's own reaction sits ARM from it (middle of the length the beam is clamped over).
c_edge = xyj_geo["carriage"][3]
LEVER = (xyj_geo["stub"][0] + xyj_geo["stub"][3] - c_edge) / 1000
ARM = ((xyj_geo["stub"][0] + max(p["bb"][3] for p in xyj_geo["parts"] if p["role"] == "plate")) / 2 - c_edge) / 1000
F_BENCH = 49.0


def joint_k(case, mode):
    """Rotational stiffness (N*m/rad) of one XY joint from the bench FEA, the bare stub's own bending removed."""
    r = xyj.get(case)
    if not r:
        return None
    add = (r[mode] - r["bare_stub_um"]) / 1e6
    return F_BENCH * LEVER / (add / LEVER)

# case: version, plate material (for mass), key into belt_path.json, creep factor (extra deflection / elastic)
CASES = {"Printed ABS": ("Printed", "ABS", "ABS", 0.67), "Printed PC-CF15": ("Printed", "PC-CF15", "PC-CF15", 0.30),
         "CF 0/90": ("CF", "CF 3K twill", "CF 0/90", 0.0), "CF 45": ("CF", "CF 3K twill", "CF 45", 0.0),
         "Metal": ("Metal", "6061-T6", "Metal", 0.0)}


def k_corner(case, corner, model="bonded"):
    hit = [c["k_rot"] for c in corners if c["case"] == case and c["corner"] == corner and c.get("model", "bonded") == model]
    return hit[0] * 1000 if hit else None  # N*mm/rad


# ---- masses from the CAD ----
def vol(v, pred):
    return sum(p["vol"] for p in parts[v] if pred(p)) / 1000  # cm3


in_joint = lambda p: any("XY Joint" in s for s in p["parents"])
is_plate = lambda v: (lambda p: PLATE_TAG[v] in p["label"] or "5mm Metal Only" in p["label"])
print("== Plate mass (g): corners (incl. metal lever arms) | XY joints | total")
for v, mats in (("Printed", PRINTED), ("CF", ["CF 3K twill"]), ("Metal", ["6061-T6"])):
    c, j = vol(v, lambda p: is_plate(v)(p) and not in_joint(p)), vol(v, lambda p: is_plate(v)(p) and in_joint(p))
    for m in mats:
        d = MAT[m][2]
        print(f"  {v:8s} {m:12s} {c * d:5.0f} | {j * d:4.0f} | {(c + j) * d:5.0f}")


def density(p):
    l = p["label"]
    if "Insert" in l: return 8.5
    if "SOLID" in l or "Pulley" in l: return 2.7
    return 7.85


P = parts["Printed"]
M_JOINT_HW = sum(p["vol"] * density(p) for p in P if in_joint(p) and not ("Printed6mm" in p["label"] or "Spacer x" in p["label"])) / 1e6
M_XBEAM = (next(p for p in P if "Toolhead X-Axis" in p["label"])["vol"] * 2.7 + next(p for p in P if "X MGN12H Rail" in p["label"])["vol"] * 7.8) / 1e6
M_BLOCK = next(p for p in P if p["label"].startswith("MGN12H Linear Rail Slide"))["vol"] * 7.85 / 1e6
M_HEAD = M_TOOL + M_BLOCK  # everything that moves in X
M_YEXT = (next(p for p in P if "Gantry Y-Axis" in p["label"])["vol"] * 2.7 + next(p for p in P if p["label"] == "Y Axis Linear Rail")["vol"] * 7.8) / 1e6
M_ROTOR = 4 * ROTOR_J / PULLEY_R ** 2  # all four motors turn for any X or Y move in CoreXY AWD
print(f"  Moving with Y besides the plates: X beam {M_XBEAM:.3f} kg, joint hardware {M_JOINT_HW:.3f} kg, "
      f"toolhead {M_TOOL:.3f} + MGN12H block {M_BLOCK:.3f} kg; motor rotors add {M_ROTOR:.3f} kg effective")

b = lambda k: plates[k]["bb"]
L_Y = b("Printed_BackLeftTopPlate")[1] - b("Printed_FrontLeftTop")[4]
L_X = -2 * b("Printed_XYLiveIdlerLeftBottomPlate")[3]
# Y extrusion + MGN9 rail underneath: bare 6,936 mm^4, ~21,000 fully composite; screwed every 40 mm -> 14,000
EI_Y = E_AL * 14000.0
# X beam + MGN12 rail on its front face: the rail sits at the beam's height, so it only adds its own stiffness
EI_X = E_AL * I_2020 + E_ST * 8 * 12 ** 3 / 12
print(f"  Y span between plate edges {L_Y:.1f} mm, X span between XY joint plates {L_X:.1f} mm")


def beam(L, EI, k0, k1, n=120, rho=0.0):
    """Euler beam, pinned ends with rotational springs k0/k1 (N*mm/rad). Returns K, M (consistent), x."""
    x = np.linspace(0, L, n + 1); h = L / n
    K = np.zeros((2 * n + 2,) * 2); M = np.zeros_like(K)
    ke = EI / h ** 3 * np.array([[12, 6 * h, -12, 6 * h], [6 * h, 4 * h * h, -6 * h, 2 * h * h],
                                 [-12, -6 * h, 12, -6 * h], [6 * h, 2 * h * h, -6 * h, 4 * h * h]])
    me = rho * h / 420 * np.array([[156, 22 * h, 54, -13 * h], [22 * h, 4 * h * h, 13 * h, -3 * h * h],
                                   [54, 13 * h, 156, -22 * h], [-13 * h, -3 * h * h, -22 * h, 4 * h * h]])
    for e in range(n):
        d = slice(2 * e, 2 * e + 4); K[d, d] += ke; M[d, d] += me
    K[1, 1] += k0; K[-1, -1] += k1
    return K, M, x


def free_dofs(K):
    return [i for i in range(K.shape[0]) if i not in (0, K.shape[0] - 2)]


def static(K, f):
    fr = free_dofs(K); u = np.zeros(len(f)); u[fr] = np.linalg.solve(K[np.ix_(fr, fr)], f[fr]); return u


at = lambda x, a: int(round(a / (x[1] - x[0])))
out = {}
for case, (v, pm, _, _) in CASES.items():
    kf, kb = k_corner(case, "Front"), k_corner(case, "Back")
    note = ""
    if kb is None: kb, note = kf, "back corner not meshed: front value used"
    if kf is None: kf, note = kb, "front corner not meshed: back value used"
    m_plates = vol(v, lambda p: is_plate(v)(p) and in_joint(p)) * MAT[pm][2] / 1000
    out[case] = dict(k_front=kf / 1000, k_back=kb / 1000, note=note, m_joint_plates=m_plates,
                     m_y=M_XBEAM + M_JOINT_HW + m_plates + M_HEAD)
    print(f"  {case:16s} corners {kf / 1e6:5.2f} / {kb / 1e6:5.2f} kN*m/rad{'  (' + note + ')' if note else ''}")

print("\n== Moving mass and acceleration (same motor force; motor rotors included)")
ref = out["Printed ABS"]["m_y"] + M_ROTOR
for case, o in out.items():
    o["a_rel_y"] = ref / (o["m_y"] + M_ROTOR)
    print(f"  {case:16s} Y: {o['m_y']:.3f} kg + rotors {M_ROTOR:.3f} kg -> acceleration {(o['a_rel_y'] - 1) * 100:+5.1f} % vs printed ABS")

print("\n== Gravity sag at the nozzle (static: Z tilt and the bed mesh take it out)")
for case, o in out.items():
    P_side = (M_XBEAM + M_JOINT_HW + o["m_joint_plates"] + M_HEAD) * g / 2
    KY, _, xy = beam(L_Y, EI_Y, o["k_front"] * 1000, o["k_back"] * 1000)
    KX, _, xx = beam(L_X, EI_X, 0, 0)  # X beam pinned in the joints: conservative
    fx = np.zeros(KX.shape[0]); fx[2 * at(xx, L_X / 2)] -= M_HEAD * g; fx[0::2] -= M_XBEAM * g / len(xx)
    wx = static(KX, fx)[2 * at(xx, L_X / 2)]
    sag = []
    for yj in np.linspace(20, L_Y - 20, 25):
        f = np.zeros(KY.shape[0]); f[0::2] -= M_YEXT * g / len(xy); f[2 * at(xy, yj)] -= P_side
        sag.append((static(KY, f)[2 * at(xy, yj)] + wx) * 1000)
    o.update(sag_max_um=-min(sag), sag_var_um=max(sag) - min(sag))
    print(f"  {case:16s} max {-min(sag):5.1f} um, front-to-back variation {max(sag) - min(sag):4.1f} um")

print("\n== XY joints as springs (from the bench FEA): pitch (vertical) and yaw (sideways), per joint")
for case, o in out.items():
    kp, ky = joint_k(case, "vertical"), joint_k(case, "sideways")
    o.update(joint_k_pitch=kp, joint_k_yaw=ky, joint_k_vert=kp / ARM ** 2 / 1000 if kp else None)
    if kp:
        sag = (M_XBEAM + M_JOINT_HW / 2 + M_HEAD) / 2 * g * ARM / kp * ARM * 1e6
        o["joint_sag_um"] = sag
        print(f"  {case:16s} pitch {kp:6.0f} N*m/rad (vertical {kp / ARM ** 2 / 1000:5.0f} N/mm at the beam),"
              f" yaw {ky:6.0f} N*m/rad; static drop at the beam end {sag:4.1f} um")

print("\n== Vertical bounce (moving gantry on the Y extrusions and the XY joints; toolhead on the X beam)")
for case, o in out.items():
    K, M, xy = beam(L_Y, 2 * EI_Y, 2 * o["k_front"] * 1000, 2 * o["k_back"] * 1000, rho=2 * M_YEXT / L_Y)
    m_g = M_XBEAM + M_JOINT_HW + o["m_joint_plates"] + M_HEAD
    j = 2 * at(xy, L_Y / 2); M[j, j] += m_g
    fr = free_dofs(K)
    w2 = eigh(K[np.ix_(fr, fr)] * 1000, M[np.ix_(fr, fr)], eigvals_only=True, subset_by_index=[0, 0])[0]
    f_y_ext = math.sqrt(w2) / 2 / math.pi
    f_g = f_y_ext
    if o.get("joint_k_vert"):  # both joints, in series with the extrusions
        k_ext = (2 * math.pi * f_y_ext) ** 2 * m_g
        k = 1 / (1 / k_ext + 1 / (2 * o["joint_k_vert"] * 1000))
        f_g = math.sqrt(k / m_g) / 2 / math.pi
    f_t = math.sqrt(48 * EI_X / L_X ** 3 * 1000 / (M_HEAD + 17 / 35 * M_XBEAM)) / 2 / math.pi
    f_c = 1 / math.sqrt(1 / f_g ** 2 + 1 / f_t ** 2)  # Dunkerley: lower bound for the coupled mode
    o.update(f_bounce_extrusions=f_y_ext, f_bounce_gantry=f_g, f_bounce_tool=f_t, f_bounce=f_c)
    print(f"  {case:16s} on the Y extrusions alone {f_y_ext:4.0f} Hz, with the XY joints {f_g:4.0f} Hz,"
          f" toolhead on X beam {f_t:4.0f} Hz, together >= {f_c:4.0f} Hz")

print("\n== XY belt resonance (CoreXY, AWD: each belt held by both motors) and gantry yaw")
L1, L2 = 407.0, 500.0     # belt path from the toolhead to the nearest motor on each side, toolhead centred (CAD)
RUNS, HALF = (0.190, 0.240), 0.229  # Y belt runs either side of a centred XY joint (m), joint half-spacing (m)
for case, (v, pm, bk, _) in CASES.items():
    o = out[case]
    add = belt[bk]["compliance_added"]
    k = [2 * ea * (1 / L1 + 1 / L2) / (1 + a) * 1000 for ea, a in zip(EA_BELT, add)]
    I = M_XBEAM * 0.426 ** 2 / 12 + (M_JOINT_HW + o["m_joint_plates"]) * HALF ** 2  # 426 mm X beam
    # the belts and both XY joints resist the same rotation of the X beam, so they add
    kj = 2 * (o.get("joint_k_yaw") or 0)
    yaw = [math.sqrt((2 * ea * sum(1 / r for r in RUNS) * HALF ** 2 + kj) / I) / 2 / math.pi for ea in EA_BELT]
    o.update(f_y=[math.sqrt(q / o["m_y"]) / 2 / math.pi for q in k], f_x=[math.sqrt(q / M_HEAD) / 2 / math.pi for q in k], f_yaw=yaw)
    print(f"  {case:16s} Y {o['f_y'][0]:3.0f}-{o['f_y'][1]:3.0f} Hz, X {o['f_x'][0]:3.0f}-{o['f_x'][1]:3.0f} Hz,"
          f" yaw {yaw[0]:3.0f}-{yaw[1]:3.0f} Hz")

print("\n== Belt tension swing under acceleration (each span changes by about m*a/4; pretension 6-8 lb)")
m_max = max(o["m_y"] for o in out.values())
swing = {a: m_max * a / 1000 / 4 for a in (20000, 40000, 50000)}
for a, s in swing.items():
    print(f"  {a:6d} mm/s^2: +-{s:4.1f} N per span (heaviest version); slack side keeps {T_RANGE[0] - s:4.1f}-{T_RANGE[1] - s:4.1f} N")

print(f"\n== Belt tension by plucked frequency, f = sqrt(T/mu)/(2L), mu = {MU_BELT * 1000:.1f} g/m")
freq = {}
for L in (100, 150, 200):
    freq[L] = [math.sqrt(T / MU_BELT) / (2 * L / 1000) for T in (26.7, 31.1, 35.6)]
    print(f"  span {L} mm: 6 lb {freq[L][0]:4.0f} Hz, 7 lb {freq[L][1]:4.0f} Hz, 8 lb {freq[L][2]:4.0f} Hz")


def bimetal(A1, I1, A2, I2, d, dT):
    """Curvature of an aluminium beam (1) with a steel rail (2) screwed to it, centroids d apart, warmed by dT."""
    de = (23.6e-6 - 11.5e-6) * dT
    EA1, EA2 = E_AL * A1, E_ST * A2
    EI = E_AL * I1 + E_ST * I2 + EA1 * EA2 * d * d / (EA1 + EA2)
    return de * EA1 * EA2 * d / ((EA1 + EA2) * (E_AL * I1 + E_ST * I2) + EA1 * EA2 * d * d), EI


bow = {}
for chamber in CHAMBERS[1:]:
    dT = chamber - T_ASSEMBLY
    kap, EIc = bimetal(174, I_2020, 48, 180, 13.25, dT)       # MGN9 under each Y extrusion: bows vertically
    kapx, _ = bimetal(174, I_2020, 96, 12 * 8 ** 3 / 12, 13.9, dT)  # MGN12 on the X beam's front face: bows sideways
    free_y, free_x = kap * L_Y ** 2 / 8 * 1000, kapx * L_X ** 2 / 8 * 1000
    print(f"\n== Thermal bow, {chamber} C chamber (+{dT} K): Y axes free {free_y:.0f} um, X beam free {free_x:.0f} um sideways")
    bow[chamber] = dict(dT=dT, free_y=free_y, free_x=free_x, cases={})
    for case, o in out.items():
        k = 2 / (1 / o["k_front"] + 1 / o["k_back"]) * 1000
        M = (kap * L_Y / 2) / (1 / k + L_Y / (2 * EIc))
        r = dict(bow_um=(kap - M / EIc) * L_Y ** 2 / 8 * 1000, moment_Nm=M / 1000, plate_shear_N=M / 26.0)
        bow[chamber]["cases"][case] = r
        print(f"  {case:16s} bonded corners {r['bow_um']:4.0f} um, corner moment {r['moment_Nm']:4.1f} N*m,"
              f" plate shear {r['plate_shear_N']:4.0f} N vs ~500 N friction{' -> slips' if r['plate_shear_N'] > 500 else ''}")

print("\n== Joint clamping: bonded (a tight through-bolt, best case) vs clamp patches (a loose T-nut joint)")
kap30, EIc30 = bimetal(174, I_2020, 48, 180, 13.25, CHAMBERS[1] - T_ASSEMBLY)
kap45, EIc45 = bimetal(174, I_2020, 48, 180, 13.25, CHAMBERS[2] - T_ASSEMBLY)
clamp = {}
for case, o in out.items():
    r = {}
    for model in ("bonded", "patch"):
        kf, kb = k_corner(case, "Front", model), k_corner(case, "Back", model)
        kf, kb = kf or kb, kb or kf
        name = case if model == "bonded" else case + " (patch)"
        kp, ky = joint_k(name, "vertical"), joint_k(name, "sideways")
        if not (kf and kp):
            continue
        k = 2 / (1 / kf + 1 / kb) * 1000
        bows = []
        for kap, EIc in ((kap30, EIc30), (kap45, EIc45)):
            M = (kap * L_Y / 2) / (1 / k + L_Y / (2 * EIc))
            bows.append((kap - M / EIc) * L_Y ** 2 / 8 * 1000)
        m_g = M_XBEAM + M_JOINT_HW + o["m_joint_plates"] + M_HEAD
        k_ext = (2 * math.pi * o["f_bounce_extrusions"]) ** 2 * m_g
        k_v = 2 * kp / ARM ** 2
        f_b = math.sqrt(1 / (1 / k_ext + 1 / k_v) / m_g) / 2 / math.pi
        I = M_XBEAM * 0.426 ** 2 / 12 + (M_JOINT_HW + o["m_joint_plates"]) * HALF ** 2
        yaw = [math.sqrt((2 * ea * sum(1 / q for q in RUNS) * HALF ** 2 + 2 * ky) / I) / 2 / math.pi for ea in EA_BELT]
        r[model] = dict(k_corner=(kf + kb) / 2 / 1000, k_pitch=kp, k_yaw=ky, bow=bows, f_bounce=f_b, f_yaw=yaw)
    clamp[case] = r
    if len(r) == 2:
        b, p = r["bonded"], r["patch"]
        print(f"  {case:16s} corner {p['k_corner']:6.0f} -> {b['k_corner']:6.0f} N*m/rad, bow 55 C {p['bow'][0]:4.0f} -> {b['bow'][0]:4.0f} um,"
              f" 70 C {p['bow'][1]:4.0f} -> {b['bow'][1]:4.0f} um; XY joint pitch {p['k_pitch']:5.0f} -> {b['k_pitch']:5.0f} N*m/rad,"
              f" bounce {p['f_bounce']:4.0f} -> {b['f_bounce']:4.0f} Hz, yaw {p['f_yaw'][0]:3.0f}-{p['f_yaw'][1]:3.0f} -> {b['f_yaw'][0]:3.0f}-{b['f_yaw'][1]:3.0f} Hz")

print("\n== Motor heat (estimate): case temperature and what the plate under it sees")
p_motor = 2 * MOTOR["I_run"] ** 2 * MOTOR["R"] + 2.0  # copper in both phases + ~2 W iron loss
heat = {}
for chamber in CHAMBERS:
    insul = [chamber + p_motor * r for r in (3.5, 5.0)]   # on printed or CF plates (they insulate)
    sink = [chamber + p_motor * r for r in (2.0, 3.0)]    # on aluminium plates (they spread heat into the frame)
    heat[chamber] = dict(insulating=insul, aluminium=sink)
    print(f"  {chamber} C chamber: {p_motor:.1f} W per motor -> case {insul[0]:3.0f}-{insul[1]:3.0f} C on printed/CF plates,"
          f" {sink[0]:3.0f}-{sink[1]:3.0f} C on aluminium")

print("\n== Belt tension lost to plate creep (~1000 h near chamber temperature)")
for case, (v, pm, bk, cr) in CASES.items():
    extra = belt[bk]["dL_um"] * cr / 1000
    out[case]["creep_loss_N"] = [extra * ea / BELT_LOOP for ea in EA_BELT]
    print(f"  {case:16s} {out[case]['creep_loss_N'][0]:4.2f}-{out[case]['creep_loss_N'][1]:4.2f} N of {T_BELT} N")

Pcr = math.pi ** 2 * EI_X / L_X ** 2
print(f"\n== X beam buckling under the 70 N XY-joint squeeze: Euler load {Pcr:.0f} N, factor {Pcr / 70:.0f}")
json.dump(dict(cases=out, clamp=clamp, bow=bow, heat=heat, p_motor=p_motor, swing=swing, freq=freq, m_rotor=M_ROTOR,
               m_head=M_HEAD, buckling_factor=Pcr / 70), open(os.path.join(WORK, "frame_res.json"), "w"), indent=1)
