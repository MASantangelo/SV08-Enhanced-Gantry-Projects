# Mechanical Analysis

An engineering check of the three gantry versions (printed, carbon fiber and 6061 aluminium) and of the 9mm belt mod. It answers two questions: **is each version stiff and strong enough for the loads it carries, and what limits each one in practice?** It covers the plates, the corner and XY joints, and the gantry as a whole. It ends with how to check your own build.

## How it was done

- **Geometry** comes straight from each version's full assembly STEP file: part volumes and positions, plate shapes and the belt path. Belt wrap angles and load directions are measured from the belt model.
- **Plates and joints** were analysed with finite elements: each part was meshed in gmsh (quadratic tetrahedra) and solved with CalculiX, the solver that ships with FreeCAD.
- **Carbon fiber** is modelled as a woven 0/90 laminate, stiff along the weave and soft in in-plane shear, with the weave either along the plate's edges (0/90) or at 45°.
- **The gantry as a whole** (sag, vibration modes, yaw, thermal bow) uses beam models of the extrusions and rails, with the joint stiffness taken from the FEA.
- **Material values** are typical datasheet figures. Treat every number as ±20 %, and use the results to compare versions and find weak links, not as exact predictions.
- **To rerun it** after a design change, use the scripts in [`tools/analysis`](tools/analysis). See [tools/README.md](tools/README.md#mechanical-analysis).

## Summary

In the tables, **↑** means higher is better and **↓** means lower is better. Tables without arrows are inputs or reference values.

| | Better | Printed (ABS → PC-CF) | CF, weave 0/90 | CF, weave 45° | Metal 5 mm | 9mm belt mod (on CF) |
|---|---|---|---|---|---|---|
| **Plate set mass** (corners + XY joints) | ↓ | 268–319 g | 383 g | 383 g | 594 g | 444 g |
| **Y-axis acceleration** (same motors, rotors included) | ↑ | baseline → −0.7 % | −1.3 % | −1.3 % | −3.5 % | −2.2 % |
| **Worst plate deflection under belt load** | ↓ | 63 → 22 µm | 8.2 µm | 7.7 µm | 3.6 µm | 7.7 µm |
| **Extra belt-path compliance from the plates** | ↓ | 1.2–3.7 % → 0.4–1.3 % | 0.1–0.4 % | 0.1–0.4 % | 0.05–0.14 % | 0.14–0.43 % |
| **Corner joint stiffness** (metal = 1) | ↑ | 0.34 → 0.54 | 0.86 | 0.75 | 1.00 | 0.90 front, 1.8 back |
| **XY joint pitch stiffness** (metal = 1) | ↑ | 0.07 → 0.19 | 0.77 | 0.53 | 1.00 | 0.76 |
| **Gantry vertical bounce** (on extrusions + XY joints) | ↑ | 59 → 93 Hz | 157 Hz | 138 Hz | 168 Hz | 159 Hz |
| **Y resonance** (belt-limited) | ↑ | 38–68 Hz | 38–68 Hz | 38–68 Hz | 38–67 Hz | 47–82 Hz |
| **Gantry yaw mode** | ↑ | 111–189 Hz | 157–209 Hz | 151–205 Hz | 196–236 Hz | 166–234 Hz |
| **Y-axis thermal bow, 55 / 70 °C chamber** (bonded corners) | ↓ | 176 / 265 → 130 / 195 µm | 106 / 158 µm | 115 / 173 µm | 95 / 142 µm | 83 / 124 µm |
| **Plate under a motor, 55 / 70 °C chamber** | ↓ | 82–94 / 97–109 °C | same | same | 71–78 / 86–93 °C | as CF |

**What matters, in order:**

1. **The belts set XY stiffness.** Even ABS plates add under 4 % to the belt path's flex, so X and Y resonances match across versions within a few percent.
2. **Printed XY joints are the vertical weak link.** The bottom plate between the MGN9 block and the X beam bends. In ABS the gantry bounces at about **60 Hz**, inside the XY resonance range, which can put Z ripples on prints. PC-CF reaches 93 Hz; CF and metal 140–170 Hz.
3. **Thermal bow is the biggest structural load.** The steel rails bend the aluminium extrusions as the chamber warms: up to 0.33 mm at 55 °C and 0.5 mm at 70 °C. T-nut joints slip under it. Stiff corners halve the bow, and drilled through-bolts in CF or metal hold it without slipping. Heat-soak before calibrating.
4. **ABS and ASA are too hot under the motors** in a heated chamber. PC and PC-CF are fine at 55 °C and marginal at 70 °C. Aluminium keeps the motors 10–15 °C cooler.
5. **Cut CF with the weave along the plate edges.** These plates are limited by bending, not shear, so 45° is worse.
6. **Metal's mass costs little.** The motor rotors add 0.67 kg of effective mass to every version, so metal is only 3.5 % slower than printed ABS.
7. **The 9mm belt mod is the stiffest XY setup here.** Its belts are about 1.5× as stiff, which lifts the X and Y resonances by about 20 %, and its deeper corners hold the extrusions tighter against thermal bow. See [9mm belt mod](#9mm-belt-mod).

## Basis

| Input | Value | Source |
|---|---|---|
| Belts | Gates GT2, 6 mm, tensioned to 6–8 lb (26.7–35.6 N) per span | Given |
| Belt stiffness | EA = 8,000–25,000 N per unit strain. That's the 0.15–0.4 % stretch typical of fiberglass-cord belts at working tension, and it predicts a Y resonance of 38–68 Hz, where printers in this class usually measure. Measured GT-2 stiffness varies with load ([Wang et al., 2018](https://www.mdpi.com/2218-6581/7/4/75)). Every conclusion here holds across the whole range. | Assumed |
| Belt mass | About 8 g/m for 6 mm GT2, 12 g/m for 9 mm (for the tensioning tables) | Typical |
| 9 mm belts | 1.5× the stiffness of a 6 mm belt (the cord layer is 1.5× as wide), at the same 6–8 lb | Assumed |
| Toolhead | 0.40 kg (Xol + A4T), plus the 72 g MGN12H block from the CAD | Given / CAD |
| X beam | 2020 extrusion + MGN12 rail, 0.47 kg | CAD |
| XY joint hardware | 0.20 kg for both joints | CAD |
| Motors | StepperOnline 17HS19-2504S-H-V1: 68 g·cm² rotor, 1.1 Ω, run at 65 % of 2.5 A. On 20-tooth pulleys, the four rotors add about 0.67 kg of effective mass to any X or Y move. | Datasheet |
| Chamber | 25 °C open, 55 °C (ASA/ABS), 70 °C (PC/nylon). The gantry is assembled at 25 °C. | Given |
| Y extrusion + MGN9 rail stiffness | Taken halfway between the bare extrusion and the fully composite section | Assumed |

**Materials:**

| Material | E, in-plane (GPa) ↑ | Density (g/cm³) ↓ | Tensile (MPa) ↑ | HDT @ 0.45 MPa (°C) ↑ | CTE (µm/m·K), closest to aluminium's 23.6 is best | Long-term clamp stress, approx. (MPa) ↑ |
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

| Acceleration | Swing per span ↓ | Slack side keeps (from 6–8 lb) ↑ |
|---|---|---|
| 20,000 mm/s² | ±6.4 N | 20–29 N |
| 40,000 mm/s² | ±12.7 N | 14–23 N |
| 50,000 mm/s² | ±15.9 N | 11–20 N |

The belts stay taut at all of these. At the high end, 6 lb leaves the slack side with little margin, so tension toward 8 lb if you run 40k or more.

## Plate FEA

All six left-side plates of each version (front corner, back corner and XY joint, top and bottom) were loaded with their measured idler loads at 8 lb. Each plate's share of every load was set by belt height, and the plates were held at their extrusion and Z-carriage bolts.

![Front left top plate displacement under belt load: printed ABS, carbon fiber with the weave at 0/90 and at 45°, and aluminium](Renders/Analysis/Plate%20FEA%20-%20Front%20Left%20Top.png)

| Plate (all rows ↓) | Printed (ABS) | CF 0/90 | CF 45° | Metal 5 mm | 9mm mod (CF 0/90) |
|---|---|---|---|---|---|
| Front corner, top | 60 µm | 4.7 µm | 5.7 µm | 3.6 µm | 5.1 µm |
| Front corner, bottom | 43 µm | 8.2 µm | 6.8 µm | 2.9 µm | 7.7 µm |
| Back corner, top / bottom | 11 / 20 µm | 1.6 / 0.8 µm | 1.5 / 0.7 µm | 0.3 / 0.4 µm | 1.5 / 0.8 µm |
| XY joint, top / bottom | 63 / 19 µm | 8.2 / 3.0 µm | 7.7 / 4.9 µm | 2.9 / 0.9 µm | 6.7 / 3.9 µm |
| Peak stress away from bolts and bores | 2.8 MPa | 6.5 MPa | 11.8 MPa | 5.0 MPa | 7.4 MPa |
| Peak stress at bolt and bore edges | 11 MPa | 28 MPa | 16 MPa | 12 MPa | 32 MPa |

Deflections are peak values per plate. Other printed materials scale with stiffness: ASA 66 µm, PC 57 µm, ABS-CF 26 µm, ASA-CF 27 µm and PC-CF 22 µm at the worst plate.

- **Stresses are low in every version.** The peaks at bolt and bore edges are partly a modelling artefact of rigid supports. Against tensile strength the margin is a factor of about 3–4 for printed parts and 15+ for CF and metal.
- **CF's soft in-plane shear doubles its deflection** compared with treating it like a metal, but that's still a few microns. The weave angle makes almost no difference here.

**Effect on the belt path.** Adding up how far each shaft moves, times its wrap factor, gives the extra belt length the plates allow. Compared with the belt's own stretch:

| Version | Belt path lengthening ↓ | Extra compliance (EA 8,000 → 25,000 N) ↓ |
|---|---|---|
| Printed ABS / ASA / PC | 111 / 116 / 101 µm | 1.2–3.7 % / 1.2–3.9 % / 1.1–3.4 % |
| Printed ABS-CF / ASA-CF / PC-CF | 47 / 48 / 39 µm | 0.4–1.6 % |
| CF 0/90 / 45° | 11.9 / 11.4 µm | 0.12–0.40 % |
| Metal 5 mm | 4.3 µm | 0.05–0.14 % |
| 9mm mod (CF 0/90) | 8.6 µm | 0.14–0.43 % (against the stiffer 9 mm belt) |

## Corner joints

How rigidly a corner holds the end of its Y extrusion sets how much the gantry sags and how well it resists thermal bow. The corner sandwich was modelled with both plates, the printed 20 mm spacer plate, the Z carriage spacer and a 2020 stub, all bonded together and fixed at the Z-carriage bolts. A pure bending moment was applied to the stub.

| Version | Front corner ↑ | Back corner ↑ | Relative to metal ↑ |
|---|---|---|---|
| Printed ABS (plates and spacers) | 6,380 N·m/rad | 6,910 N·m/rad | 0.34–0.37 |
| Printed PC-CF (plates and spacers) | 10,130 N·m/rad | 13,920 N·m/rad | 0.54–0.74 |
| CF, weave 0/90 | 16,110 N·m/rad | ≈ front* | 0.86 |
| CF, weave 45° | 14,150 N·m/rad | ≈ front* | 0.75 |
| Metal 5 mm | 18,760 N·m/rad | ≈ front* | 1.00 |
| 9mm belt mod (CF 0/90) | 16,810 N·m/rad | 34,280 N·m/rad | 0.90–1.83 |

\*The CF and metal back-corner plates didn't mesh cleanly, so the front value is used. In the printed version the back corners came out stiffer than the front, so this is conservative.

These are upper bounds. Bonded contact is stiffer than a real bolted joint, and the stock Z carriage, its rail and the Z drive aren't included. Those are the same in every version.

## XY joints

Each XY joint holds the end of the X beam and rides on one MGN9 carriage. The joint was modelled with both plates, its spacers, the steel shafts and standoffs that tie the plates together, and a 200 mm stub of the X beam. It was held only where the MGN9 block bolts on, and 49 N (5 kg) was hung on the end of the stub, sideways and vertically. The same setup is described as a bench test under [Checking your own build](#checking-your-own-build).

| Version | Sideways at the stub end ↓ | Vertical at the stub end ↓ | Pitch stiffness, per joint ↑ | Yaw stiffness, per joint ↑ |
|---|---|---|---|---|
| Bare 2020 stub (rigid joint) | 0.17 mm | 0.17 mm | n/a | n/a |
| Printed ABS | 2.4 mm | 16.9 mm | 150 N·m/rad | 1,130 N·m/rad |
| Printed PC-CF | 1.0 mm | 6.3 mm | 410 N·m/rad | 2,860 N·m/rad |
| CF, weave 0/90 | 0.54 mm | 1.7 mm | 1,660 N·m/rad | 6,840 N·m/rad |
| CF, weave 45° | 0.58 mm | 2.4 mm | 1,140 N·m/rad | 6,070 N·m/rad |
| Metal 5 mm | 0.34 mm | 1.3 mm | 2,150 N·m/rad | 14,690 N·m/rad |
| 9mm belt mod (CF 0/90) | 0.55 mm | 1.7 mm | 1,640 N·m/rad | 6,600 N·m/rad |

**The joint pivots where its bottom plate leaves the MGN9 block.** About 25 mm of plate between the block and the X beam carries the whole moment. Vertically that bends the plate through its thickness, which is a plate's weakest direction. Sideways it bends the plate in its own plane, which is much stiffer.

**In the printer the static effect is small.** The X beam's weight drops each beam end by 4–7 µm with CF or metal, 21 µm with PC-CF and 56 µm with ABS. Z tilt and the bed mesh take that out.

**The dynamic effect is not small for printed joints.** The joints act as springs under the moving gantry, in series with the Y extrusions:

| Version | Gantry bounce on the Y extrusions alone ↑ | Including the XY joints ↑ | With the toolhead bouncing on the X beam (lower bound) ↑ |
|---|---|---|---|
| Printed ABS | 213 Hz | **59 Hz** | 56 Hz |
| Printed PC-CF | 235 Hz | 93 Hz | 80 Hz |
| CF, weave 0/90 | 246 Hz | 157 Hz | 111 Hz |
| CF, weave 45° | 241 Hz | 138 Hz | 104 Hz |
| Metal 5 mm | 249 Hz | 168 Hz | 115 Hz |
| 9mm belt mod (CF 0/90) | 260 Hz | 159 Hz | 112 Hz |

The toolhead bouncing on the X beam on its own sits at 157 Hz in every version.

- **Printed ABS bounces in the same range as the XY resonances (38–68 Hz).** XY moves can then drive vertical vibration at the nozzle, because the nozzle sits below the beam and every acceleration also tips the gantry. That can show as faint ripples or Z banding that input shaping doesn't remove, since input shaping only targets X and Y.
- **PC-CF is borderline, and CF and metal are clear.** If you print the XY joints, PC-CF or another stiff CF-filled grade is the better choice, even if the corners stay in a cheaper plastic.

**The 45° weave is worse here.** The joint is loaded in bending, not in-plane shear, and bending stiffness along the plate comes from fibres running along it. 0/90 is about 50 % stiffer in pitch than 45°.

## The gantry as a whole

### Moving mass and acceleration

| Version | Moving in Y ↓ | Plus motor rotors ↓ | Y acceleration (same motor force) ↑ |
|---|---|---|---|
| Printed ABS | 1.21 kg | 1.88 kg | baseline |
| Printed PC-CF | 1.22 kg | 1.89 kg | −0.7 % |
| CF | 1.23 kg | 1.90 kg | −1.3 % |
| Metal 5 mm | 1.27 kg | 1.94 kg | −3.5 % |
| 9mm belt mod (CF) | 1.25 kg | 1.92 kg | −2.2 % |

Moving in Y means the X beam and rail, both XY joints, the toolhead and the MGN12H block. The four rotors add the same 0.67 kg to every version, which is why the plate material barely moves the acceleration figure. X moves carry only the toolhead and block (0.47 kg) plus the rotors, and are the same in every version.

### Sag under gravity

| Version | Peak sag at the nozzle ↓ | Variation front to back ↓ |
|---|---|---|
| Printed ABS | 17 µm | 5.5 µm |
| Printed PC-CF | 16 µm | 4.6 µm |
| CF | 15–16 µm | 4.2–4.3 µm |
| Metal | 15 µm | 4.1 µm |
| 9mm belt mod | 15 µm | 3.8 µm |

Sag comes from the toolhead, the X beam and the joints hanging on the Y extrusions. It is static, so Z tilt calibration and the bed mesh take it out. **Sag isn't a concern in any version.**

### Vibration modes

| Mode (all rows ↑) | Printed ABS | Printed PC-CF | CF 0/90 | CF 45° | Metal | 9mm belt mod |
|---|---|---|---|---|---|---|
| Y axis, belt-limited | 38–67 Hz | 38–68 Hz | 38–68 Hz | 38–68 Hz | 38–67 Hz | 47–82 Hz |
| X axis, belt-limited | 61–107 Hz | 62–109 Hz | 62–109 Hz | 62–109 Hz | 62–109 Hz | 76–134 Hz |
| Gantry yaw (X beam twisting about Z) | 111–180 Hz | 126–189 Hz | 157–209 Hz | 151–205 Hz | 196–236 Hz | 166–234 Hz |
| Gantry vertical bounce (see XY joints) | 56–59 Hz | 80–93 Hz | 111–157 Hz | 104–138 Hz | 115–168 Hz | 112–159 Hz |

Ranges span the belt stiffness range, or the bounce with and without the toolhead mode.

- **Yaw** is resisted by the Y belt runs and by both XY joints together. Stiffer joints raise it, which more than makes up for the metal joints' extra mass.
- The Z drive's own compliance, which isn't modelled, would lower the bounce modes equally in every version.

### Thermal bow

Both Y axes have a steel MGN9 rail screwed under an aluminium 2020 extrusion. Aluminium expands about twice as much as steel, so when the gantry warms the pair bends like a bimetal strip: the middle of each Y axis rises. The corner joints resist that, and they carry a restraining moment as a result.

![Y-axis thermal bow at 55 °C and 70 °C chamber temperatures by version](Renders/Analysis/Thermal%20Bow%20-%20Y%20Axis.png)

| Version | Bow, 55 °C (bonded corners) ↓ | Bow, 70 °C ↓ | Corner moment, 55 / 70 °C ↓ | Shear on each plate, 55 / 70 °C ↓ |
|---|---|---|---|---|
| No restraint | 333 µm | 500 µm | n/a | n/a |
| Printed ABS | 176 µm | 265 µm | 12 / 18 N·m | 460 / 700 N |
| Printed PC-CF | 130 µm | 195 µm | 16 / 24 N·m | 600 / 900 N |
| CF 0/90 | 106 µm | 158 µm | 18 / 26 N·m | 670 / 1,010 N |
| CF 45° | 115 µm | 173 µm | 17 / 25 N·m | 650 / 970 N |
| Metal 5 mm | 95 µm | 142 µm | 18 / 28 N·m | 700 / 1,060 N |
| 9mm belt mod | 83 µm | 124 µm | 19 / 29 N·m | 740 / 1,110 N |

**The joints will slip.** The moment is carried as a shear couple between the plates and the extrusion. The two M4 screws per plate hold about 500 N by friction when freshly torqued, and less in a printed plate once its preload has relaxed (about 280 N). At 70 °C every version is past that. So in practice:

- **Partial restraint.** The bow ends up between the bonded values and the free value.
- **Bolts take the load.** Once a joint slips, the bolts bear in their holes. In printed plates that's about 10–15 MPa on each M4 hole, above the long-term limit for ABS and ASA, so holes can slowly oval over many heat cycles. CF and metal handle it easily.
- **Joints can settle.** Repeated heat cycles can walk a joint slightly. Re-check the corner bolts after the first few hot prints in every version, or through-bolt them (see [Clamping the extrusions](#clamping-the-extrusions-t-nuts-or-drilled-through-bolts)).

**The X beam bows too.** Its MGN12 rail is on the front face, so it bows sideways: up to 0.32 mm at 55 °C and 0.47 mm at 70 °C across the travel if the XY joints let the ends rotate, and roughly a third of that if they hold them square. That bends the X travel slightly in Y. It's the same in every version.

**What to do:**

- Heat-soak the chamber before Z tilt and the bed mesh, so the bow is already in place when it gets measured.
- Keep the chamber temperature consistent between calibration and printing.

### Clamping the extrusions: T-nuts or drilled through-bolts

As designed, each plate is held to the extrusions by M4 screws into drop-in T-nuts. That's the cheap option, and it's nearly good enough. The upgrade is to through-bolt the stack instead, at the same positions:

1. An M4 socket head with a washer goes under the bottom plate.
2. It runs up through a 4.3 mm hole drilled top to bottom through the centre of the extrusion.
3. It comes out through the top plate, with a washer and a nylon-insert locknut on top.

Like the T-nuts, it uses the existing hole positions, which line up with the stock SV08 extrusions.

**What drilling buys you:**

1. **A positive stop.** Once friction lets go, a T-nut can slide along its slot, so a corner can creep a little along the extrusion with every heat cycle. A bolt in a drilled hole can't move further than its clearance. This applies in every version, including printed.
2. **More clamping force where the plates can take it.** One bolt clamps both plates and the extrusion in a single stack, and it can be torqued harder than a T-nut, whose slot lips start to give at about 1.5–2 N·m. CF and metal plates take 2.5–3 N·m easily. Printed plates can't use the extra torque: the plastic under the washer still limits them to about 1 N·m (1.3 N·m with a nylon locknut, because the nylon takes some of the torque).
3. **Stiffer corners.** A tight through-bolt clamps close to the bonded joint the FEA assumes. A T-nut joint behaves more like a joint clamped only at its bolts. Running the front corners both ways puts the difference at about 20–25 %:

| Corner (front) | Clamped at bolts only (T-nut-like) ↑ | Bonded (tight through-bolt) ↑ | Y-axis bow, 55 °C ↓ | Y-axis bow, 70 °C ↓ |
|---|---|---|---|---|
| CF, weave 0/90 | 12,170 N·m/rad | 16,090 N·m/rad | 127 → 106 µm | 190 → 159 µm |
| CF, weave 45° | 11,440 N·m/rad | 14,140 N·m/rad | 132 → 115 µm | 197 → 173 µm |
| Metal 5 mm | 14,170 N·m/rad | 18,750 N·m/rad | 115 → 95 µm | 173 → 142 µm |

The printed corners' clamped-at-bolts model didn't mesh, so printed isn't in this table.

**Holding against thermal bow.** This compares how much shear each plate can hold by friction (two bolts per plate, friction coefficient 0.2) with what the bow puts on it:

| Clamp | Torque | Preload per bolt | Holds per plate ↑ |
|---|---|---|---|
| T-nut | 1.0 / 1.5 N·m | 1,250 / 1,880 N | 500 / 750 N |
| Through-bolt, printed plates | 1.3 N·m | 1,250 N | 500 N |
| Through-bolt, CF or metal | 2.5 / 3.0 N·m | 2,750 / 3,380 N | 1,100 / 1,350 N |

| Needed per plate ↓ | 55 °C chamber | 70 °C chamber |
|---|---|---|
| Printed ABS | 460 N | 700 N |
| Printed PC-CF | 600 N | 900 N |
| CF | 650–670 N | 970–1,010 N |
| Metal | 710 N | 1,060 N |
| 9mm belt mod | 740 N | 1,110 N |

- **CF, metal and the 9mm mod through-bolted at 3 N·m hold at both chamber temperatures,** and at 2.5 N·m they hold up to 55 °C.
- **T-nuts slip at 70 °C in every version,** and at 55 °C unless torqued toward 1.5 N·m.
- **Printed plates slip either way,** so for printed the drilled hole's value is the positive stop.

**The XY joints** take the same treatment for the two M4s that hold the X beam. The bolt then clamps the top plate, the beam, the 10 mm spacer and the bottom plate as one stack, so the beam can't shift in the joint under the belt squeeze or hard acceleration.

How much stiffer that makes the joint isn't measured: the clamped-at-bolts version of the XY joint model didn't mesh. Two things bound it:
- **The ceiling:** the bonded figures in [XY joints](#xy-joints) are the most a perfect clamp could give.
- **The main flex doesn't change:** most of the joint's flex is the bottom plate bending where it leaves the MGN9 block, which through-bolting doesn't touch.

Expect a joint that stays tight and consistent, close to those bonded figures, rather than one that beats them.

**Hardware:**

| Where | Stack to clamp | Bolt (M4 socket head) | Room above (nut) | Room below (head) |
|---|---|---|---|---|
| Corners, into the Y extrusion (2 per corner) | 32 mm (printed, CF) / 30 mm (metal) | M4×45 / M4×40 | Clear at all four positions | Inner positions clear. Back outer: about 1.5 mm to spare. **Front outer, beside the Z carriage: only room for a button head and washer, as now.** |
| XY joints, into the X beam (2 per joint) | 42 mm (printed, CF) / 40 mm (metal) | M4×55 / M4×50 | Clear | Clear |
| 9mm belt mod, corners | 42 mm | M4×55 | Clear | As above: the front outer position only takes a button head |
| 9mm belt mod, XY joints | 47 mm | M4×60 | Clear | Clear |

Lengths assume about 1 mm washers and a 5 mm DIN 985 locknut, with a thread or two showing. M4×35 is too short everywhere. The nylon insert is good to about 120 °C, so 70 °C chambers are fine, but replace the nut after a few removals.

**Drilling:**

- **Square and centred.** Use a drill press, square to the face, through the centre of the slot.
- **Clearance:** 4.3 mm, or 4.5 mm if you want a little float to line up with both plates.
- **The outer holes sit close to the extrusion ends,** at the stock positions:

| Hole | Wall left between the hole and the extrusion end |
|---|---|
| XY joint (X beam) | 2.85 mm |
| Corners (Y extrusion) | 2.85–2.95 mm |
| X back extrusion (if you through-bolt it too) | **1.35 mm** |

The XY joint and corner holes are still several times stronger than needed: the tear-out estimate is about 3–4 kN against loads of about 0.5 kN. The X back extrusion's holes are the tightest; that joint isn't loaded by thermal bow, so it can stay on T-nuts. The risk is the drill wandering toward the end, or the thin wall bulging. Drill slowly with the end supported, deburr, and check that the saw-cut end is square before you start.

### Motor heat

Each motor dissipates about 8 W at 65 % of rated current. Printed and CF plates insulate, so the motor case and the plate under it run hot. Aluminium plates spread the heat into the frame. These are estimates:

| Chamber | Motor case and plate, printed or CF ↓ | On aluminium ↓ |
|---|---|---|
| 25 °C (open, PLA/PETG) | 52–64 °C | 41–48 °C |
| 55 °C (ASA/ABS) | 82–94 °C | 71–78 °C |
| 70 °C (PC/nylon) | 97–109 °C | 86–93 °C |

Plastic under a clamped motor needs to stay well below its heat-deflection temperature, or the clamp slowly sinks in.

| Plate material | 25 °C chamber (margin ↑) | 55 °C chamber (margin ↑) | 70 °C chamber (margin ↑) |
|---|---|---|---|
| ABS / ASA (HDT 95–98 °C) | Fine | **Too close**: 0–15 °C margin | **Over** |
| PC / PC-CF (HDT 125–130 °C) | Fine | Fine: 30–45 °C margin | Marginal: 15–30 °C margin |
| CF-epoxy plate (Tg ~120 °C) | Fine | Fine: 25–40 °C margin | Marginal: 10–25 °C margin, so check your supplier's Tg |
| Aluminium | Fine | Fine | Fine, and the motors run 10–15 °C cooler |

### Creep and belt tension

Printed plates keep deflecting slowly under constant belt load at chamber temperature.

- **Printed ABS:** over about 1,000 hours that lets about 75 µm more belt into the path, which drops tension by **0.3–0.9 N** of 35.6 N (1–2.5 %).
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

| Material | Plate set ↓ | XY joint plates ↓ | Worst plate deflection ↓ | Extra belt compliance ↓ | Corner joint (metal = 1) ↑ | Heat growth (100 mm, +40 K) ↓ |
|---|---|---|---|---|---|---|
| ABS | 268 g | 65 g | 63 µm | 1.2–3.7 % | 0.34 | +0.27 mm |
| ASA | 276 g | 67 g | 66 µm | 1.2–3.9 % | ~0.33 | +0.27 mm |
| PC | 309 g | 75 g | 57 µm | 1.1–3.4 % | ~0.36 | +0.18 mm |
| ABS-CF15 | 283 g | 69 g | 26 µm | 0.5–1.6 % | ~0.5 | +0.07 mm |
| ASA-CF15 | 289 g | 70 g | 27 µm | 0.5–1.6 % | ~0.5 | +0.07 mm |
| PC-CF15 | 319 g | 78 g | 22 µm | 0.4–1.3 % | 0.54 | +0.05 mm |

Corner joint values marked ~ are interpolated between the ABS and PC-CF FEA runs.

**Strength is fine. The limits are joint stiffness, heat and creep:**

1. **The XY joints.** In ABS or ASA they let the gantry bounce at about 59 Hz (see [XY joints](#xy-joints)). Print the XY joint plates in PC-CF or another stiff CF-filled grade, or use the CF or metal joints with printed corners.
2. **Heat.** In an ASA/ABS or PC chamber, ABS and ASA plates under the motors sit at or past their heat-deflection temperature. Use PC or PC-CF for any enclosed, heated printing.
3. **Washers on plastic.** An M4 at 1–1.5 N·m preloads to about 1,250–1,900 N. Under a standard 9 mm washer that's 26–39 MPa on the plate face, 3–6× the long-term limit, so the joint slowly relaxes. Relaxed joints slip more easily under the thermal-bow moment.
   - Use 12 mm OD washers, which halve the stress.
   - Keep torque modest, and re-check the bolts after the first few heat cycles.
4. **Softer corners.** Printed corners are a third to a half as stiff as metal, which adds 35–120 µm of thermal bow. Heat-soaking before calibration takes care of it.
5. **Heat-set inserts** only carry light axial loads here (bearing retainers and similar). Their real limit is installation quality and torque (see the [Printed README](Printed%20Version/README.md#installing-the-heat-set-inserts)).

**Material ranking:** PC-CF > PC ≈ ABS-CF ≈ ASA-CF > ABS ≈ ASA. CF filler more than doubles stiffness and cuts heat growth by about 4× for about 5 % more mass. PC raises heat resistance the most.

## Carbon fiber version (6 mm)

| | Better | Weave 0/90 | Weave 45° |
|---|---|---|---|
| Plate set / XY joint plates | ↓ | 383 g / 89 g | 383 g / 89 g |
| Worst plate deflection | ↓ | 8.2 µm | 7.7 µm |
| Corner joint (metal = 1) | ↑ | 0.86 | 0.75 |
| XY joint pitch (metal = 1) | ↑ | 0.77 | 0.53 |
| Gantry vertical bounce | ↑ | 157 Hz | 138 Hz |
| Thermal bow, 55 / 70 °C | ↓ | 106 / 158 µm | 115 / 173 µm |

- **Cut the plates with the weave along the plate edges (0/90).** A woven CF plate is stiff along its fibres and soft in in-plane shear. These plates are limited by bending, not shear, so fibres running along the plate do more good than fibres at 45°.
- **Nearly as stiff as metal for 35 % less plate mass.** With the weave at 0/90, CF reaches 75–90 % of the metal version's joint stiffness and stays far ahead of printed plates.
- **Barely expands with heat**, so it shrinks slightly relative to the aluminium frame as things warm up (−0.08 mm over 100 mm at +40 K). The close-fit clearance holes absorb that.
- **No creep** at these stresses. The thermal-bow couple (up to about 1,000 N per plate at 70 °C) is well within what the laminate and its bolt holes can take.
- **Heat:** the epoxy's glass transition is typically around 120 °C. At 70 °C chambers the plate under a motor can reach 100–110 °C, so check your supplier's Tg, or use a high-Tg grade if you print PC or nylon.
- **Threads** come from PEM standoffs bonded into hex pockets. Their strength is the epoxy bond, but they only carry clamp and retainer loads. Follow the [CF build notes](README.md#carbon-fiber-version-6-mm): epoxy every standoff.
- **What limits it:**
  - CF is brittle at edges and countersinks, so overtightening flat heads can crack the top layers.
  - It needs a mill for the partial-depth features.
  - CF touching bare aluminium can corrode galvanically in humid conditions. The epoxy surface mostly insulates it, but sealed edges help.

## Metal version (5 mm 6061)

| Plate set ↓ | XY joint plates ↓ | Worst plate deflection ↓ | Corner joint ↑ | XY joint pitch ↑ | Gantry vertical bounce ↑ | Thermal bow, 55 / 70 °C ↓ |
|---|---|---|---|---|---|---|
| 594 g | 137 g | 3.6 µm | 1.00 | 1.00 | 168 Hz | 95 / 142 µm |

The plate set mass includes the four 5 mm aluminium tensioner lever arms (28 g).

- **Stiffest in every result here,** including the highest gantry bounce and yaw frequencies.
- **Most robust long-term.** It expands at the same rate as the aluminium frame, so heat cycles add no plate-growth stress. It doesn't creep, and washer pressure is far below 6061's yield, so bolted joints hold their preload.
- **Heat sink for the motors.** Aluminium plates keep the motor cases about 10–15 °C cooler than printed or CF plates, the only version with comfortable margin at 70 °C chambers.
- **Tapped threads are stronger than the screws.** An M3 thread in 6061 with 4 mm of engagement strips at about 4,700 N, more than an M3 class 8.8 screw can carry (about 2,900 N). With 3 mm of engagement, as on the shorter retainers, it's about 3,500 N. Normal M3 torque (about 1–1.2 N·m) is safe. Use cutting fluid when tapping and don't bottom the tap in blind holes.
- **What limits it: mass, and only a little.** The metal XY joints add about 70 g to the Y axis compared with printed ABS and 48 g compared with CF. Counting the motor rotors, that's about 3.5 % less Y acceleration than printed ABS for the same motors. The 5 mm plates also change some screw lengths (see the [Metal build notes](README.md#metal-version-5-mm)).

## 9mm belt mod

The [9mm belt mod](CF%20Version/9mm%20Belt%20Mod) widens both belts to 9 mm. To fit the wider belts, the corners open from a 20 mm to a 30 mm gap, with a 5 mm riser above and below each extrusion, and the XY joints open to 35 mm. The plates themselves don't change. It's modelled here on its CF template plates with the weave at 0/90; on aluminium or printed plates, the plate-driven results move the way they do in the main versions.

| | Better | CF 0/90 (6 mm belts) | 9mm belt mod |
|---|---|---|---|
| Plate set mass (with the 5 mm risers) | ↓ | 383 g | 444 g |
| Mass moving in Y | ↓ | 1.23 kg | 1.25 kg |
| Worst plate deflection | ↓ | 8.2 µm | 7.7 µm |
| Extra belt-path compliance from the plates | ↓ | 0.12–0.40 % | 0.14–0.43 % |
| Corner joint, front / back | ↑ | 16,110 / ≈16,110 N·m/rad | 16,810 / 34,280 N·m/rad |
| XY joint pitch / yaw | ↑ | 1,660 / 6,840 N·m/rad | 1,640 / 6,600 N·m/rad |
| Y resonance, belt-limited | ↑ | 38–68 Hz | 47–82 Hz |
| X resonance, belt-limited | ↑ | 62–109 Hz | 76–134 Hz |
| Gantry yaw | ↑ | 157–209 Hz | 166–234 Hz |
| Gantry vertical bounce | ↑ | 157 Hz | 159 Hz |
| Y-axis thermal bow, 55 / 70 °C (bonded corners) | ↓ | 106 / 158 µm | 83 / 124 µm |

**What the wider belts buy:**

- **About 20 % higher X and Y resonances.** The belts are about 1.5× as stiff, and they set XY stiffness in every version, so this is the biggest XY gain available here. The extra 17 g in the joints barely registers once the motor rotors are counted (−0.9 % acceleration compared with 6 mm CF).
- **Stiffer back corners, less thermal bow.** The back corner sandwich is now 36 mm deep instead of 26 mm, with the risers and the X back extrusion filling it, and it holds the Y extrusion about twice as stiffly. The front corner stays about where CF was. Together that cuts the bonded thermal bow by about 20 %.
- **The XY joints are unchanged in practice.** The 35 mm joint is about as stiff as the 30 mm one. Its weak spot is still the bottom plate where it leaves the MGN9 block, and that hasn't changed.
- **The belt loads are the same at the same tension.** The plates see nearly the same forces. If you tension 9 mm belts harder than 6–8 lb, every belt load and plate deflection here scales up in proportion, and the plates still have large margins.

**Through-bolting** works the same way, with longer bolts: M4×55 at the corners (42 mm stack) and M4×60 at the XY joints (47 mm stack). The bow shear on each plate is a little higher (740 N at 55 °C, 1,110 N at 70 °C), still within what CF through-bolted at 3 N·m holds (1,350 N).

**Risers:** the analysis assumes they're cut from the plate stock and clamped solid. Printed risers sit in the clamp stack like the shared spacers, so the same advice applies: print them in PC, PC-CF or another CF-filled grade.

**Belt tension by frequency (9 mm GT2, about 12 g/m):**

| Free span | 6 lb (26.7 N) | 7 lb (31.1 N) | 8 lb (35.6 N) |
|---|---|---|---|
| 100 mm | 236 Hz | 255 Hz | 272 Hz |
| 150 mm | 157 Hz | 170 Hz | 182 Hz |
| 200 mm | 118 Hz | 127 Hz | 136 Hz |

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

Klipper's `TEST_RESONANCES` should find Y around 38–68 Hz and X around 61–109 Hz with 6 mm belts (47–82 Hz and 76–134 Hz with the 9mm mod), depending mostly on belt tension. Much lower than that points at loose belts or a loose joint.

On a printed build, also run the test with the accelerometer reading Z, or look at its Z trace. A peak around 55–95 Hz is the XY-joint bounce described above.

### XY joint bench test

To measure a joint's stiffness directly:

1. **Calibrate the setup first.** Clamp a bare 200 mm piece of 2020 in a vise with 25 mm held. Hang 5 kg at 175 mm and read the deflection at that same point. It should be about **0.18 mm** (about 7 thousandths of an inch). If it isn't, the setup is the problem: fix that before testing the joint.
2. **Hold the joint by its MGN9 block,** not by its plates. Use a short piece of rail with the block on it, clamped to the bench, which is how the printer holds it.
3. **Put the dial on a stand on the bench itself,** never on the part, with its tip at the load point and square to the load.
4. **Use a fine enough dial.** A 0.01 mm or 0.0001″ dial resolves these differences; a 0.001″ dial only just resolves the metal joint.
5. **Load gently.** Start from 0.5 kg and step up, and read each step after the dial settles. For printed joints, stay at 1 kg or less: the predictions below scale with load, and 5 kg on a printed ABS joint bends the plate far enough to risk permanent damage.

Predicted deflection at the stub end, with 49 N (5 kg) at about 172 mm from where the beam leaves the joint. Scale linearly for other loads.

| Version | Sideways ↓ | Vertical ↓ |
|---|---|---|
| Bare 2020 stub, rigid joint | 0.17 mm | 0.17 mm |
| Printed ABS | 2.4 mm | 16.9 mm |
| Printed PC-CF | 1.1 mm | 6.3 mm |
| CF, weave 0/90 | 0.54 mm | 1.7 mm |
| CF, weave 45° | 0.58 mm | 2.4 mm |
| Metal 5 mm | 0.34 mm | 1.3 mm |
| 9mm belt mod (CF) | 0.55 mm | 1.7 mm |

The model bonds every contact and holds the MGN9 block rigidly, so a real joint should measure a little more than these figures, not less. A reading well below them means the dial or the clamp isn't where the table assumes.

## Limits of this analysis

- **Bonded and fixed.** The FEA treats contacts as bonded and bolt holes as rigidly fixed. Real bolted joints are softer, which affects all three versions but the printed one most.
- **XY joint shafts.** In the XY joint model, the shafts and standoffs are simplified posts with the real parts' bending stiffness.
- **Z side not modelled.** The stock Z carriages, Z rails, Z drive and printer frame aren't included. They're identical across versions and would lower the bounce modes equally.
- **CF and metal back corners** use the front-corner value. Where the 20 mm spacer plate meets those back plates, its rounded corners end within 0.02 mm of an edge on the plate. The leftover faces are too small to mesh. That's a modelling limitation, not a fault in the parts.
- **Clamped-at-bolts models** (the T-nut comparison) only meshed for the corners of the main versions, not for the XY joints or the 9mm mod.
- **Assumed inputs.** Belt stiffness, rail-to-extrusion coupling, the motor's thermal resistance and creep factors are assumed. The ranges are stated where they matter.
- **Plastics vary.** Creep and heat limits for printed plastics depend strongly on brand, print settings and chamber temperature. The figures here are for comparison.
- **Walls not checked here.** Thin webs around pockets aren't checked individually in this analysis; the [`tools/plate-check.ps1`](tools) wall checks cover those.
