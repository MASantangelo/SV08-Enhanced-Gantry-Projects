"""Shared inputs for the mechanical analysis: material data (typical datasheet values, about +-20 %) and assumptions."""

# name: E in-plane (MPa), Poisson, density (g/cm3), CTE (um/m/K)
MAT = {
    "ABS":        (2100, 0.35, 1.04, 90),
    "ASA":        (2000, 0.35, 1.07, 90),
    "PC":         (2300, 0.37, 1.20, 68),
    "ABS-CF15":   (5000, 0.35, 1.10, 40),
    "ASA-CF15":   (4800, 0.35, 1.12, 40),
    "PC-CF15":    (6000, 0.35, 1.24, 35),
    "CF 3K twill": (55000, 0.30, 1.55, 2.5),
    "6061-T6":    (68900, 0.33, 2.70, 23.6),
}
PRINTED = ["ABS", "ASA", "PC", "ABS-CF15", "ASA-CF15", "PC-CF15"]
PLATE_TAG = {"Printed": "Printed6mm", "CF": "CF6mm", "Metal": "Metal5mm", "CF9": "CF6mm"}

# Woven 0/90 CF-epoxy plate (3K twill, ~50 % fibre): stiff along the weave, soft in in-plane shear.
# CalculiX engineering constants: E1, E2, E3, nu12, nu13, nu23, G12, G13, G23 (MPa); axes 1/2 along the weave.
CF_ORTHO = (55000, 55000, 8000, 0.05, 0.30, 0.30, 4500, 3500, 3500)
# Plate materials as analysed: isotropic (E, nu) or orthotropic dict with the weave angle to the plate's X axis.
# Other printed materials are scaled from ABS by stiffness.
CASES = {
    "Printed ABS": ("Printed", (MAT["ABS"][0], MAT["ABS"][1])),
    "CF 0/90":     ("CF", dict(ortho=CF_ORTHO, angle=0)),
    "CF 45":       ("CF", dict(ortho=CF_ORTHO, angle=45)),
    "Metal":       ("Metal", (MAT["6061-T6"][0], MAT["6061-T6"][1])),
    "CF 9mm":      ("CF9", dict(ortho=CF_ORTHO, angle=0)),  # 9mm belt mod, analysed on its CF template plates
}
# belt stiffness relative to a 6 mm GT2 belt (it scales with the width of the fiberglass cord layer)
EA_SCALE = {"CF 9mm": 1.5}
MU_BELT_9 = 0.012        # kg/m, typical 9 mm GT2 belt

T_BELT = 35.6            # N per span, 8 lb
T_RANGE = (26.7, 35.6)   # N, 6-8 lb
EA_BELT = (8000, 25000)  # N per unit strain, 6 mm fiberglass GT2 (assumed range)
MU_BELT = 0.008          # kg/m, typical 6 mm GT2 belt
BELT_LOOP = 2100         # mm
M_TOOL = 0.40            # kg, Xol toolhead + A4T, without the MGN12H block (the block's mass comes from the CAD)
ROTOR_J = 68e-7          # kg*m^2, StepperOnline 17HS19-2504S-H-V1
PULLEY_R = 0.006366      # m, GT2 20-tooth pitch radius
MOTOR = dict(R=1.1, I_run=0.65 * 2.5)  # ohm per phase, run current (A) at 65 % of rated
CHAMBERS = (25, 55, 70)  # deg C: open, ASA/ABS, PC/nylon
T_ASSEMBLY = 25          # deg C, temperature the gantry is assembled and squared at
