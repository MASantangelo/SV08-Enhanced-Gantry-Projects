# Mechanical Analysis

An engineering check of the three gantry versions: printed, carbon fiber and 6061 aluminium. It answers two questions: **is each version stiff and strong enough for the loads it carries, and what limits each one in practice?** It covers the plates, the corner and XY joints, and the gantry as a whole. It ends with how to check your own build.

## How it was done

- **Geometry** comes straight from each version's full assembly STEP file: part volumes and positions, plate shapes and the belt path. Belt wrap angles and load directions are measured from the belt model.
- **Plates and joints** were analysed with finite elements: each part was meshed in gmsh (quadratic tetrahedra) and solved with CalculiX, the solver that ships with FreeCAD.
- **Carbon fiber** is modelled as a woven 0/90 laminate, stiff along the weave and soft in in-plane shear, with the weave either along the plate's edges (0/90) or at 45°.
- **The gantry as a whole** (sag, vibration modes, yaw, thermal bow) uses beam models of the extrusions and rails, with the joint stiffness taken from the FEA.
- **Material values** are typical datasheet figures. Treat every number as ±20 %, and use the results to compare versions and find weak links, not as exact predictions.
- **To rerun it** after a design change, use the scripts in [`tools/analysis`](tools/analysis). See [tools/README.md](tools/README.md#mechanical-analysis).

## Summary

| | Printed (ABS → PC-CF) | CF, weave 0/90 | CF, weave 45° | Metal 5 mm |
|---|---|---|---|---|
| **Plate set mass** (corners + XY joints) | 267–318 g | 383 g | 383 g | 594 g |
| **Y-axis acceleration** (same motors, rotors included) | baseline → −0.7 % | −1.3 % | −1.3 % | −3.6 % |
| **Worst plate deflection under belt load** | 59 → 21 µm | 6.4 µm | 5.8 µm | 3.3 µm |
| **Extra belt-path compliance from the plates** | 1.1–3.5 % → 0.4–1.2 % | 0.1–0.3 % | 0.1–0.3 % | 0.04–0.14 % |
| **Corner joint stiffness** (metal = 1) | 0.34 → 0.54 | 0.86 | 0.76 | 1.00 |
| **XY joint pitch stiffness** (metal = 1) | 0.07 → 0.19 | 0.80 | 0.54 | 1.00 |
| **Gantry vertical bounce** (on extrusions + XY joints) | 60 → 95 Hz | 160 Hz | 141 Hz | 170 Hz |
| **Y resonance** (belt-limited) | 38–68 Hz | 38–68 Hz | 38–68 Hz | 38–67 Hz |
| **Gantry yaw mode** | 111–189 Hz | 157–209 Hz | 152–206 Hz | 194–235 Hz |
| **Y-axis thermal bow, 55 / 70 °C chamber** (bonded corners) | 177 / 265 → 130 / 195 µm | 106 / 158 µm | 115 / 173 µm | 95 / 143 µm |
| **Plate under a motor, 55 / 70 °C chamber** | 82–94 / 97–109 °C | same | same | 71–78 / 86–93 °C |

**What matters, in order:**

1. **The belts set XY stiffness in every version.** Belt loads act in the plane of the plates and every shaft is held by both plates. Even ABS plates add under 4 % to the belt path's flex, and CF and metal add well under 1 %. The Y and X resonances that input shaping deals with are the same in all versions to within a few percent.
2. **The XY joints are the vertical weak link in a printed build.** Each XY joint hangs the X beam off its MGN9 carriage through about 25 mm of bottom plate. In ABS that's soft enough to drop the moving gantry's vertical bounce to about **60 Hz**, inside the range of the XY resonances. Vertical vibration excited by XY moves can then show up on prints. PC-CF lifts it to about 95 Hz, and CF and metal sit at 140–170 Hz.
3. **Thermal bow is the biggest structural load in the gantry.** The steel rails bolted to the aluminium extrusions bend the extrusions as the chamber warms: 0.33 mm across the Y span at 55 °C, 0.5 mm at 70 °C, if nothing resists it. Holding the extrusion ends against that takes 12–28 N·m at each corner, far more than the belts ever put on the plates, and the corner bolts slip at those loads. Stiffer corners roughly halve the bow.
4. **At ASA/ABS and PC/nylon chamber temperatures, ABS and ASA plates are too close to their softening point** where the motors sit on them. PC and PC-CF are fine at 55 °C and marginal at 70 °C. Aluminium also keeps the motors 10–15 °C cooler.
5. **Weave at 45° doesn't help these plates.** In-plane shear isn't what limits them. Bending is, and the 0/90 weave is stiffer in bending along the plate's edges. Cut CF plates with the weave along the edges.
6. **Metal costs mass, but less than it looks.** The motors' rotors count for about 0.67 kg of effective moving mass, so the metal XY joints cost only about 3.6 % of Y acceleration compared with printed ABS.

## Basis

| Input | Value | Source |
|---|---|---|
| Belts | Gates GT2, 6 mm, tensioned to 6–8 lb (26.7–35.6 N) per span | Given |
| Belt stiffness | EA = 8,000–25,000 N per unit strain. That's the 0.15–0.4 % stretch typical of fiberglass-cord belts at working tension, and it predicts a Y resonance of 38–68 Hz, where printers in this class usually measure. Measured GT-2 stiffness varies with load ([Wang et al., 2018](https://www.mdpi.com/2218-6581/7/4/75)). Every conclusion here holds across the whole range. | Assumed |
| Belt mass | About 8 g/m (for the tensioning table) | Typical for 6 mm GT2 |
| Toolhead | 0.40 kg (Xol + A4T), plus the 72 g MGN12H block from the CAD | Given / CAD |
| X beam | 2020 extrusion + MGN12 rail, 0.47 kg | CAD |
| XY joint hardware | 0.20 kg for both joints | CAD |
| Motors | StepperOnline 17HS19-2504S-H-V1: 68 g·cm² rotor, 1.1 Ω, run at 65 % of 2.5 A. On 20-tooth pulleys, the four rotors add about 0.67 kg of effective mass to any X or Y move. | Datasheet |
| Chamber | 25 °C open, 55 °C (ASA/ABS), 70 °C (PC/nylon). The gantry is assembled at 25 °C. | Given |
| Y extrusion + MGN9 rail stiffness | Taken halfway between the bare extrusion and the fully composite section | Assumed |

**Materials:**

| Material | E, in-plane (GPa) | Density (g/cm³) | Tensile (MPa) | HDT @ 0.45 MPa (°C) | CTE (µm/m·K) | Long-term clamp stress, approx. (MPa) |
|---|---|---|---|---|---|---|
| ABS | 2.1 | 1.04 | 40 | 95 | 90 | 6 |
| ASA | 2.0 | 1.07 | 40 | 98 | 90 | 6 |
| PC | 2.3 | 1.20 | 60 | 125 | 68 | 10 |
| ABS-CF15 | 5.0 | 1.10 | 45 | 100 | 40 | 9 |
| ASA-CF15 | 4.8 | 1.12 | 45 | 102 | 40 | 9 |
| PC-CF15 | 6.0 | 1.24 | 65 | 130 | 35 | 14 |
| CF plate, 3K twill (epoxy) | 55 along the weave, **4.5 in shear**, 8 through the thickness | 1.55 | 550 | ~120 (resin Tg, check your supplier) | 2.5 | high |
| 6061-T6 aluminium | 68.9 | 2.70 | 310 | n/a | 23.6 | 150 |

Printed values are for parts printed flat, loaded in the layer plane, at or near 100 % infill. CF-filled grades vary a lot between brands. The long-term clamp stress column is a rough guide to how hard a washer can press on the material for months near chamber temperature without noticeable creep.

## Belt loads

Each corner is a top and bottom plate 20 mm apart, clamping the 2020 extrusion between them. Each XY joint is a plate pair 30 mm apart. The bottom belt runs at z ≈ 34 mm and the top belt at z ≈ 44 mm, both between the plates, and every idler, live idler and motor shaft is supported by **both** plates (dual shear).

The load an idler puts on its shaft is 2·T·sin(wrap/2). Wrap angles are measured from the belt model. The left side is listed; the right side mirrors it with the other belt.

| Location | Part | Wrap | Load at 6 lb | Load at 8 lb |
|---|---|---|---|---|
| Front corner | Motor pulley | 180° | 53 N | 71 N |
| Front corner | Bearing stack, outer front | 132° | 49 N | 65 N |
| Front corner | Live idler | 126° | 48 N | 63 N |
| Front corner | Tensioner idler | 96° | 40 N | 53 N |
| Front corner | Bearing stack, corner | 90° | 38 N | 50 N |
| Front corner | Bearing stack, inner | 79° | 34 N | 45 N |
| XY joint | Live idler / bearing stack | 88° | 37 N | 50 N |
| Back corner | Motor pulley | 141° | 50 N | 67 N |
| Back corner | Shared shaft: top 137° + bottom 47° | both belts | ≤ 71 N | ≤ 94 N |
| Back corner | Shared shaft: top 94° + bottom 20° | both belts | ≤ 48 N | ≤ 64 N |

**Net pull on each assembly at 8 lb**, summing all its idlers:

| Assembly | Net pull | Direction |
|---|---|---|
| Back corner | 89 N | Inward and forward |
| Front corner | 50 N | Outward and backward |
| XY joint | 70 N | Inward, so the X beam is squeezed by 70 N |

These forces balance through the frame. The belt plane sits closer to one plate, so that plate takes about 70 % of each idler load.

**Acceleration:** each belt span's tension changes by about m·a/4 during a move. With the heaviest version (1.27 kg moving in Y):

| Acceleration | Swing per span | Slack side keeps (from 6–8 lb) |
|---|---|---|
| 20,000 mm/s² | ±6.4 N | 20–29 N |
| 40,000 mm/s² | ±12.7 N | 14–23 N |
| 50,000 mm/s² | ±15.9 N | 11–20 N |

The belts stay taut at all of these. At the high end, 6 lb leaves the slack side with little margin, so tension toward 8 lb if you run 40k or more.

## Plate FEA

All six left-side plates of each version (front corner, back corner and XY joint, top and bottom) were loaded with their measured idler loads at 8 lb. Each plate's share of every load was set by belt height, and the plates were held at their extrusion and Z-carriage bolts.

![Front left top plate displacement under belt load: printed ABS, carbon fiber with the weave at 0/90 and at 45°, and aluminium](Renders/Analysis/Plate%20FEA%20-%20Front%20Left%20Top.png)

| Plate | Printed (ABS) | CF 0/90 | CF 45° | Metal 5 mm |
|---|---|---|---|---|
| Front corner, top | 59 µm | 5.3 µm | 5.5 µm | 3.3 µm |
| Front corner, bottom | 42 µm | 4.0 µm | 4.2 µm | 1.8 µm |
| Back corner, top / bottom | 9 / 20 µm | 0.8 / 1.1 µm | 0.8 / 1.0 µm | 0.3 / 0.4 µm |
| XY joint, top / bottom | 57 / 20 µm | 6.4 / 1.9 µm | 5.8 / 2.3 µm | 2.6 / 0.7 µm |
| Peak stress away from bolts and bores | 3.0 MPa | 5.6 MPa | 5.1 MPa | 3.9 MPa |
| Peak stress at bolt and bore edges | 9 MPa | 15 MPa | 15 MPa | 11 MPa |

Deflections are peak values per plate. Other printed materials scale with stiffness: ASA 62 µm, PC 54 µm, ABS-CF 25 µm, ASA-CF 26 µm and PC-CF 21 µm at the worst plate.

- **Stresses are low in every version.** The peaks at bolt and bore edges are partly a modelling artefact of rigid supports. Against tensile strength the margin is a factor of about 4 for printed parts and 20+ for CF and metal.
- **CF's soft in-plane shear doubles its deflection** compared with treating it like a metal, but that's still a few microns. The weave angle makes almost no difference here.

**Effect on the belt path.** Adding up how far each shaft moves, times its wrap factor, gives the extra belt length the plates allow. Compared with the belt's own stretch:

| Version | Belt path lengthening | Extra compliance (EA 8,000 → 25,000 N) |
|---|---|---|
| Printed ABS / ASA / PC | 105 / 110 / 96 µm | 1.1–3.5 % / 1.2–3.7 % / 1.0–3.2 % |
| Printed ABS-CF / ASA-CF / PC-CF | 44 / 46 / 37 µm | 0.4–1.5 % |
| CF 0/90 / 45° | 9.5 / 9.2 µm | 0.10–0.32 % |
| Metal 5 mm | 4.0 µm | 0.04–0.14 % |

## Corner joints

How rigidly a corner holds the end of its Y extrusion sets how much the gantry sags and how well it resists thermal bow. The corner sandwich was modelled with both plates, the printed 20 mm spacer plate, the Z carriage spacer and a 2020 stub, all bonded together and fixed at the Z-carriage bolts. A pure bending moment was applied to the stub.

| Version | Front corner | Back corner | Relative to metal |
|---|---|---|---|
| Printed ABS (plates and spacers) | 6,390 N·m/rad | 6,890 N·m/rad | 0.34 |
| Printed PC-CF (plates and spacers) | 10,140 N·m/rad | 13,870 N·m/rad | 0.54–0.74 |
| CF, weave 0/90 | 16,110 N·m/rad | ≈ front* | 0.86 |
| CF, weave 45° | 14,150 N·m/rad | ≈ front* | 0.76 |
| Metal 5 mm | 18,730 N·m/rad | ≈ front* | 1.00 |

\*The CF and metal back-corner plates didn't mesh cleanly, so the front value is used. In the printed version the back corners came out stiffer than the front, so this is conservative.

These are upper bounds. Bonded contact is stiffer than a real bolted joint, and the stock Z carriage, its rail and the Z drive aren't included. Those are the same in every version.

## XY joints

Each XY joint holds the end of the X beam and rides on one MGN9 carriage. The joint was modelled with both plates, its spacers, the steel shafts and standoffs that tie the plates together, and a 200 mm stub of the X beam. It was held only where the MGN9 block bolts on, and 49 N (5 kg) was hung on the end of the stub, sideways and vertically. The same setup is described as a bench test under [Checking your own build](#checking-your-own-build).

| Version | Sideways at the stub end | Vertical at the stub end | Pitch stiffness, per joint | Yaw stiffness, per joint |
|---|---|---|---|---|
| Bare 2020 stub (rigid joint) | 0.17 mm | 0.17 mm | n/a | n/a |
| Printed ABS | 2.4 mm | 16.9 mm | 150 N·m/rad | 1,120 N·m/rad |
| Printed PC-CF | 1.1 mm | 6.3 mm | 410 N·m/rad | 2,820 N·m/rad |
| CF, weave 0/90 | 0.55 mm | 1.6 mm | 1,720 N·m/rad | 6,730 N·m/rad |
| CF, weave 45° | 0.59 mm | 2.3 mm | 1,170 N·m/rad | 6,060 N·m/rad |
| Metal 5 mm | 0.35 mm | 1.3 mm | 2,170 N·m/rad | 14,250 N·m/rad |

**The joint pivots where its bottom plate leaves the MGN9 block.** About 25 mm of plate between the block and the X beam carries the whole moment. Vertically that bends the plate through its thickness, which is a plate's weakest direction. Sideways it bends the plate in its own plane, which is much stiffer.

**In the printer the static effect is small.** The X beam's weight drops each beam end by 4–7 µm with CF or metal, 20 µm with PC-CF and 54 µm with ABS. Z tilt and the bed mesh take that out.

**The dynamic effect is not small for printed joints.** The joints act as springs under the moving gantry, in series with the Y extrusions:

| Version | Gantry bounce on the Y extrusions alone | Including the XY joints | With the toolhead bouncing on the X beam (lower bound) |
|---|---|---|---|
| Printed ABS | 213 Hz | **60 Hz** | 56 Hz |
| Printed PC-CF | 235 Hz | 95 Hz | 81 Hz |
| CF, weave 0/90 | 246 Hz | 160 Hz | 112 Hz |
| CF, weave 45° | 241 Hz | 141 Hz | 105 Hz |
| Metal 5 mm | 249 Hz | 170 Hz | 115 Hz |

The toolhead bouncing on the X beam on its own sits at 157 Hz in every version.

- **Printed ABS bounces in the same range as the XY resonances (38–68 Hz).** XY moves can then drive vertical vibration at the nozzle, because the nozzle sits below the beam and every acceleration also tips the gantry. That can show as faint ripples or Z banding that input shaping doesn't remove, since input shaping only targets X and Y.
- **PC-CF is borderline, and CF and metal are clear.** If you print the XY joints, PC-CF or another stiff CF-filled grade is the better choice, even if the corners stay in a cheaper plastic.

**The 45° weave is worse here.** The joint is loaded in bending, not in-plane shear, and bending stiffness along the plate comes from fibres running along it. 0/90 is about 50 % stiffer in pitch than 45°.

## The gantry as a whole

### Moving mass and acceleration

| Version | Moving in Y | Plus motor rotors | Y acceleration (same motor force) |
|---|---|---|---|
| Printed ABS | 1.20 kg | 1.87 kg | baseline |
| Printed PC-CF | 1.22 kg | 1.89 kg | −0.7 % |
| CF | 1.23 kg | 1.90 kg | −1.3 % |
| Metal 5 mm | 1.27 kg | 1.94 kg | −3.6 % |

Moving in Y means the X beam and rail, both XY joints, the toolhead and the MGN12H block. The four rotors add the same 0.67 kg to every version, which is why the plate material barely moves the acceleration figure. X moves carry only the toolhead and block (0.47 kg) plus the rotors, and are the same in every version.

### Sag under gravity

| Version | Peak sag at the nozzle | Variation front to back |
|---|---|---|
| Printed ABS | 17 µm | 5.5 µm |
| Printed PC-CF | 16 µm | 4.6 µm |
| CF | 15–16 µm | 4.1–4.3 µm |
| Metal | 15 µm | 4.1 µm |

Sag comes from the toolhead, the X beam and the joints hanging on the Y extrusions. It is static, so Z tilt calibration and the bed mesh take it out. **Sag isn't a concern in any version.**

### Vibration modes

| Mode | Printed ABS | Printed PC-CF | CF 0/90 | CF 45° | Metal |
|---|---|---|---|---|---|
| Y axis, belt-limited | 39–67 Hz | 38–68 Hz | 38–68 Hz | 38–68 Hz | 38–67 Hz |
| X axis, belt-limited | 62–107 Hz | 62–109 Hz | 62–109 Hz | 62–109 Hz | 62–109 Hz |
| Gantry yaw (X beam twisting about Z) | 111–181 Hz | 126–189 Hz | 157–209 Hz | 152–206 Hz | 194–235 Hz |
| Gantry vertical bounce (see XY joints) | 56–60 Hz | 81–95 Hz | 112–160 Hz | 105–141 Hz | 115–170 Hz |

Ranges span the belt stiffness range, or the bounce with and without the toolhead mode.

- **Yaw** is resisted by the Y belt runs and by both XY joints together. Stiffer joints raise it, which more than makes up for the metal joints' extra mass.
- The Z drive's own compliance, which isn't modelled, would lower the bounce modes equally in every version.

### Thermal bow

Both Y axes have a steel MGN9 rail screwed under an aluminium 2020 extrusion. Aluminium expands about twice as much as steel, so when the gantry warms the pair bends like a bimetal strip: the middle of each Y axis rises. The corner joints resist that, and they carry a restraining moment as a result.

![Y-axis thermal bow at 55 °C and 70 °C chamber temperatures by version](Renders/Analysis/Thermal%20Bow%20-%20Y%20Axis.png)

| Version | Bow, 55 °C (bonded corners) | Bow, 70 °C | Corner moment, 55 / 70 °C | Shear on each plate, 55 / 70 °C |
|---|---|---|---|---|
| No restraint | 333 µm | 500 µm | n/a | n/a |
| Printed ABS | 177 µm | 265 µm | 12 / 18 N·m | 460 / 700 N |
| Printed PC-CF | 130 µm | 195 µm | 16 / 24 N·m | 600 / 900 N |
| CF 0/90 | 106 µm | 158 µm | 18 / 26 N·m | 670 / 1,010 N |
| CF 45° | 115 µm | 173 µm | 17 / 25 N·m | 650 / 970 N |
| Metal 5 mm | 95 µm | 143 µm | 18 / 28 N·m | 700 / 1,060 N |

**The joints will slip.** The moment is carried as a shear couple between the plates and the extrusion. The two M4 screws per plate hold about 500 N by friction when freshly torqued, and less in a printed plate once its preload has relaxed (about 280 N). At 70 °C every version is past that. So in practice:

- **Partial restraint.** The bow ends up between the bonded values and the free value.
- **Bolts take the load.** Once a joint slips, the bolts bear in their holes. In printed plates that's about 10–15 MPa on each M4 hole, above the long-term limit for ABS and ASA, so holes can slowly oval over many heat cycles. CF and metal handle it easily.
- **Joints can settle.** Repeated heat cycles can walk a joint slightly. Re-check the corner bolts after the first few hot prints in every version.

**The X beam bows too.** Its MGN12 rail is on the front face, so it bows sideways: up to 0.32 mm at 55 °C and 0.47 mm at 70 °C across the travel if the XY joints let the ends rotate, and roughly a third of that if they hold them square. That bends the X travel slightly in Y. It's the same in every version.

**What to do:**

- Heat-soak the chamber before Z tilt and the bed mesh, so the bow is already in place when it gets measured.
- Keep the chamber temperature consistent between calibration and printing.

### Motor heat

Each motor dissipates about 8 W at 65 % of rated current. Printed and CF plates insulate, so the motor case and the plate under it run hot. Aluminium plates spread the heat into the frame. These are estimates:

| Chamber | Motor case and plate, printed or CF | On aluminium |
|---|---|---|
| 25 °C (open, PLA/PETG) | 52–64 °C | 41–48 °C |
| 55 °C (ASA/ABS) | 82–94 °C | 71–78 °C |
| 70 °C (PC/nylon) | 97–109 °C | 86–93 °C |

Plastic under a clamped motor needs to stay well below its heat-deflection temperature, or the clamp slowly sinks in.

| Plate material | 25 °C chamber | 55 °C chamber | 70 °C chamber |
|---|---|---|---|
| ABS / ASA (HDT 95–98 °C) | Fine | **Too close**: 0–15 °C margin | **Over** |
| PC / PC-CF (HDT 125–130 °C) | Fine | Fine: 30–45 °C margin | Marginal: 15–30 °C margin |
| CF-epoxy plate (Tg ~120 °C) | Fine | Fine: 25–40 °C margin | Marginal: 10–25 °C margin, so check your supplier's Tg |
| Aluminium | Fine | Fine | Fine, and the motors run 10–15 °C cooler |

### Creep and belt tension

Printed plates keep deflecting slowly under constant belt load at chamber temperature.

- **Printed ABS:** over about 1,000 hours that lets about 70 µm more belt into the path, which drops tension by **0.3–0.8 N** of 35.6 N (1–2 %).
- **Printed PC-CF:** about 0.1 N.
- **CF and metal:** none.

The bolted clamps relaxing matter more than the plates themselves; see the printed section.

## Other checks (every version)

| Check | Result |
|---|---|
| Idler shaft bending (D5 shoulder bolt, held at both ends) | 3 µm at the corners, 11 µm at the XY joints, at 71 N |
| Bearing seat pressure (F695, Ø13 × 4 mm) | About 1 MPa |
| X beam buckling under the 70 N XY-joint squeeze | Euler load about 51,000 N, a factor of 700+ |
| Fatigue | Belt tension swings of ±6–13 N give stress swings of a few MPa at most, far below the endurance limit of every material here |
| Tensioner lever arm (lever estimate) | About 2 MPa bending, a factor of 20+ even for ABS |
| Printed shared spacers in the corner clamp | Two M4 bolts at 1 N·m give about 5–7 MPa on the spacer plates' footprint. That's at the long-term limit for ABS and ASA. **Print the shared spacers in PC, PC-CF or another CF-filled grade if you can**, in every version. |

## Printed version (6 mm)

| Material | Plate set | XY joint plates | Worst plate deflection | Extra belt compliance | Corner joint (metal = 1) | Heat growth (100 mm, +40 K) |
|---|---|---|---|---|---|---|
| ABS | 267 g | 65 g | 59 µm | 1.1–3.5 % | 0.34 | +0.27 mm |
| ASA | 274 g | 67 g | 62 µm | 1.2–3.7 % | ~0.33 | +0.27 mm |
| PC | 308 g | 75 g | 54 µm | 1.0–3.2 % | ~0.36 | +0.18 mm |
| ABS-CF15 | 282 g | 68 g | 25 µm | 0.5–1.5 % | ~0.5 | +0.07 mm |
| ASA-CF15 | 287 g | 70 g | 26 µm | 0.5–1.5 % | ~0.5 | +0.07 mm |
| PC-CF15 | 318 g | 77 g | 21 µm | 0.4–1.2 % | 0.54 | +0.05 mm |

Corner joint values marked ~ are interpolated between the ABS and PC-CF FEA runs.

**Strength is fine. The limits are joint stiffness, heat and creep:**

1. **The XY joints.** In ABS or ASA they let the gantry bounce at about 60 Hz (see [XY joints](#xy-joints)). Print the XY joint plates in PC-CF or another stiff CF-filled grade, or use the CF or metal joints with printed corners.
2. **Heat.** In an ASA/ABS or PC chamber, ABS and ASA plates under the motors sit at or past their heat-deflection temperature. Use PC or PC-CF for any enclosed, heated printing.
3. **Washers on plastic.** An M4 at 1–1.5 N·m preloads to about 1,250–1,900 N. Under a standard 9 mm washer that's 26–39 MPa on the plate face, 3–6× the long-term limit, so the joint slowly relaxes. Relaxed joints slip more easily under the thermal-bow moment.
   - Use 12 mm OD washers, which halve the stress.
   - Keep torque modest, and re-check the bolts after the first few heat cycles.
4. **Softer corners.** Printed corners are a third to a half as stiff as metal, which adds 35–120 µm of thermal bow. Heat-soaking before calibration takes care of it.
5. **Heat-set inserts** only carry light axial loads here (bearing retainers and similar). Their real limit is installation quality and torque (see the [Printed README](Printed%20Version/README.md#installing-the-heat-set-inserts)).

**Material ranking:** PC-CF > PC ≈ ABS-CF ≈ ASA-CF > ABS ≈ ASA. CF filler more than doubles stiffness and cuts heat growth by about 4× for about 5 % more mass. PC raises heat resistance the most.

## Carbon fiber version (6 mm)

| | Weave 0/90 | Weave 45° |
|---|---|---|
| Plate set / XY joint plates | 383 g / 89 g | 383 g / 89 g |
| Worst plate deflection | 6.4 µm | 5.8 µm |
| Corner joint (metal = 1) | 0.86 | 0.76 |
| XY joint pitch (metal = 1) | 0.80 | 0.54 |
| Gantry vertical bounce | 160 Hz | 141 Hz |
| Thermal bow, 55 / 70 °C | 106 / 158 µm | 115 / 173 µm |

- **Cut the plates with the weave along the plate edges (0/90).** A woven CF plate is stiff along its fibres and soft in in-plane shear. These plates are limited by bending, not shear, so fibres running along the plate do more good than fibres at 45°.
- **Nearly as stiff as metal for 35 % less plate mass.** With the weave at 0/90, CF reaches 80–90 % of the metal version's joint stiffness and stays far ahead of printed plates.
- **Barely expands with heat**, so it shrinks slightly relative to the aluminium frame as things warm up (−0.08 mm over 100 mm at +40 K). The close-fit clearance holes absorb that.
- **No creep** at these stresses. The thermal-bow couple (up to about 1,000 N per plate at 70 °C) is well within what the laminate and its bolt holes can take.
- **Heat:** the epoxy's glass transition is typically around 120 °C. At 70 °C chambers the plate under a motor can reach 100–110 °C, so check your supplier's Tg, or use a high-Tg grade if you print PC or nylon.
- **Threads** come from PEM standoffs bonded into hex pockets. Their strength is the epoxy bond, but they only carry clamp and retainer loads. Follow the [CF build notes](README.md#carbon-fiber-version-6-mm): epoxy every standoff.
- **What limits it:**
  - CF is brittle at edges and countersinks, so overtightening flat heads can crack the top layers.
  - It needs a mill for the partial-depth features.
  - CF touching bare aluminium can corrode galvanically in humid conditions. The epoxy surface mostly insulates it, but sealed edges help.

## Metal version (5 mm 6061)

| Plate set | XY joint plates | Worst plate deflection | Corner joint | XY joint pitch | Gantry vertical bounce | Thermal bow, 55 / 70 °C |
|---|---|---|---|---|---|---|
| 594 g | 135 g | 3.3 µm | 1.00 | 1.00 | 170 Hz | 95 / 143 µm |

The plate set mass includes the four 5 mm aluminium tensioner lever arms (28 g).

- **Stiffest in every result here,** including the highest gantry bounce and yaw frequencies.
- **Most robust long-term.** It expands at the same rate as the aluminium frame, so heat cycles add no plate-growth stress. It doesn't creep, and washer pressure is far below 6061's yield, so bolted joints hold their preload.
- **Heat sink for the motors.** Aluminium plates keep the motor cases about 10–15 °C cooler than printed or CF plates, the only version with comfortable margin at 70 °C chambers.
- **Tapped threads are stronger than the screws.** An M3 thread in 6061 with 4 mm of engagement strips at about 4,700 N, more than an M3 class 8.8 screw can carry (about 2,900 N). With 3 mm of engagement, as on the shorter retainers, it's about 3,500 N. Normal M3 torque (about 1–1.2 N·m) is safe. Use cutting fluid when tapping and don't bottom the tap in blind holes.
- **What limits it: mass, and only a little.** The metal XY joints add about 70 g to the Y axis compared with printed ABS and 46 g compared with CF. Counting the motor rotors, that's about 3.6 % less Y acceleration than printed ABS for the same motors. The 5 mm plates also change some screw lengths (see the [Metal build notes](README.md#metal-version-5-mm)).

## Checking your own build

### Belt tension

Pluck a free belt span and measure its frequency with a phone app, or Klipper's tools. Measure the span length between the points where the belt leaves its pulleys, because the frequency depends on it.

| Free span | 6 lb (26.7 N) | 7 lb (31.1 N) | 8 lb (35.6 N) |
|---|---|---|---|
| 100 mm | 289 Hz | 312 Hz | 334 Hz |
| 150 mm | 193 Hz | 208 Hz | 222 Hz |
| 200 mm | 144 Hz | 156 Hz | 167 Hz |

These assume about 8 g/m for a 6 mm GT2 belt, so a different belt shifts them by a few hertz. Get all four belts to the same frequency at the same span length.

### Resonance test

Klipper's `TEST_RESONANCES` should find Y around 38–68 Hz and X around 62–109 Hz, depending mostly on belt tension. Much lower than that points at loose belts or a loose joint.

On a printed build, also run the test with the accelerometer reading Z, or look at its Z trace. A peak around 55–95 Hz is the XY-joint bounce described above.

### XY joint bench test

To measure a joint's stiffness directly:

1. **Calibrate the setup first.** Clamp a bare 200 mm piece of 2020 in a vise with 25 mm held. Hang 5 kg at 175 mm and read the deflection at that same point. It should be about **0.18 mm** (about 7 thousandths of an inch). If it isn't, the setup is the problem: fix that before testing the joint.
2. **Hold the joint by its MGN9 block,** not by its plates. Use a short piece of rail with the block on it, clamped to the bench, which is how the printer holds it.
3. **Put the dial on a stand on the bench itself,** never on the part, with its tip at the load point and square to the load.
4. **Use a fine enough dial.** A 0.01 mm or 0.0001″ dial resolves these differences; a 0.001″ dial only just resolves the metal joint.
5. **Load gently.** Start from 0.5 kg and step up, and read each step after the dial settles. For printed joints, stay at 1 kg or less: the predictions below scale with load, and 5 kg on a printed ABS joint bends the plate far enough to risk permanent damage.

Predicted deflection at the stub end, with 49 N (5 kg) at about 172 mm from where the beam leaves the joint. Scale linearly for other loads.

| Version | Sideways | Vertical |
|---|---|---|
| Bare 2020 stub, rigid joint | 0.17 mm | 0.17 mm |
| Printed ABS | 2.4 mm | 16.9 mm |
| Printed PC-CF | 1.1 mm | 6.3 mm |
| CF, weave 0/90 | 0.55 mm | 1.6 mm |
| CF, weave 45° | 0.59 mm | 2.3 mm |
| Metal 5 mm | 0.35 mm | 1.3 mm |

The model bonds every contact and holds the MGN9 block rigidly, so a real joint should measure a little more than these figures, not less. A reading well below them means the dial or the clamp isn't where the table assumes.

## Limits of this analysis

- **Bonded and fixed.** The FEA treats contacts as bonded and bolt holes as rigidly fixed. Real bolted joints are softer, which affects all three versions but the printed one most.
- **XY joint shafts.** In the XY joint model, the shafts and standoffs are simplified posts with the real parts' bending stiffness.
- **Z side not modelled.** The stock Z carriages, Z rails, Z drive and printer frame aren't included. They're identical across versions and would lower the bounce modes equally.
- **CF and metal back corners** use the front-corner value because their plates didn't mesh cleanly.
- **Assumed inputs.** Belt stiffness, rail-to-extrusion coupling, the motor's thermal resistance and creep factors are assumed. The ranges are stated where they matter.
- **Plastics vary.** Creep and heat limits for printed plastics depend strongly on brand, print settings and chamber temperature. The figures here are for comparison.
- **Walls not checked here.** Thin webs around pockets aren't checked individually in this analysis; the [`tools/plate-check.ps1`](tools) wall checks cover those.
