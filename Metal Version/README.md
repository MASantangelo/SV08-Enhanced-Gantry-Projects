# SV08 Metal Gantry (5 mm)

The metal variant: every gantry plate is machined from 5 mm 6061 aluminium, with tapped M3 holes in place of the heat-set inserts (printed) and M3 hex nuts (CF).

- **[Bill of Materials](BOM.md)**: every part with quantities, purchase links and notes. It's generated from `SV08_M5_BOM_from_STEP.xlsx`, which you can also download.

![The metal gantry, seen from the front right](Renders/Full%20Gantry%20-%20Front%20Right.png)

## Quick links

| I want to... | Go to |
|---|---|
| Buy the hardware | [BOM.md](BOM.md) |
| Install it | [Installation guide](../Docs/Installation.md) |
| Machine the plates | [Base Components](Base%20Components), with the [hole guide for machining](#hole-guide-for-machining) |
| Print the shared parts | [Shared Components/Print Ready](../Shared%20Components/Print%20Ready), or all at once from the [Metal Printed Components 3MF](Base%20Components/Metal%20Printed%20Components.3mf) |
| Look at the assembly in 3D | [Full assembly STL](For%20Viewing/SV08-M5%20Dual%20Shear%20Live%20Idlers%20Front%20Tensioners.stl) · [Sub-assemblies](Base%20Assemblies/For%20Viewing) |

## Full assembly

- `SV08-M5 Dual Shear Live Idlers Front Tensioners.step`: the full gantry assembly
  - [`For Viewing/`](For%20Viewing): STL copy for previewing on GitHub. It's about 32 MB, so give it a few seconds to load.
- [`Renders/`](Renders): the full gantry from four angles and each sub-assembly, generated from the STEP files

## Plates

[`Base Components`](Base%20Components) has all 14 parts as STEP files, with 3D previews in [`Base Components/For Viewing`](Base%20Components/For%20Viewing):

- 4 front corner plates, 4 back corner plates and 4 XY live idler plates, in mirrored left/right pairs
- the 5 mm XY live idler spacer
- the **metal tensioner lever arm** (`Tensioner Lever Arm Revised - 5mm Metal Only`), 4 per machine. It's a flat 5 mm version of the shared lever, cut from the same stock as the plates.

The spacers that every version shares are in [`Shared Components`](../Shared%20Components). Metal builds use the metal lever arm above instead of the shared one. [`Metal Printed Components.3mf`](Base%20Components/Metal%20Printed%20Components.3mf) has the printed parts a metal build needs on one plate (OrcaSlicer), including 4 printed copies of the metal lever arm if you'd rather print them than machine them.

## Sub-assemblies

[`Base Assemblies`](Base%20Assemblies) has each finished sub-assembly as STEP, with a 3D preview in [`Base Assemblies/For Viewing`](Base%20Assemblies/For%20Viewing).

| XY Joint Left | XY Joint Right |
|---|---|
| ![XY joint left, metal](Renders/XY%20Joint%20Left%20Metal5mm%20-%20Iso.png) | ![XY joint right, metal](Renders/XY%20Joint%20Right%20Metal5mm%20-%20Iso.png) |
| **Back Left Motor** | **Back Right Motor** |
| ![Back left motor assembly, metal](Renders/Back%20Left%20Motor%20Assembly%20Metal5mm%20-%20Iso.png) | ![Back right motor assembly, metal](Renders/Back%20Right%20Motor%20Assembly%20Metal5mm%20-%20Iso.png) |
| **Front Left Motor** | **Front Right Motor** |
| ![Front left motor assembly, metal](Renders/Front%20Left%20Motor%20Assembly%20Metal5mm%20-%20Iso.png) | ![Front right motor assembly, metal](Renders/Front%20Right%20Motor%20Assembly%20Metal5mm%20-%20Iso.png) |

- **XY joints:** live idler in dual shear. The bearing retainers are M3 × 5 flat heads that end flush with the plate faces.
- **Back motor corners:** the bearing retainers are M3 × 4 flat heads, which end on the floor of the pulley-clearance relief. The D2F endstop screws straight into tapped M2 holes, so no nuts are needed. Its M2 × 8 screws stick out about 0.2 mm under the top plate; a 0.2 mm shim from the tensioner hardware covers that if you want it flush.
- **Front motor corners:** the bearing pocket on the front **top** plates is flipped so its flange ledge is on the motor side, so the clamp load goes into the plate instead of the retainer screws. The live idler shaft is a 30 mm Chicago bolt; see the build note below about the shim under its base head and sanding the screw head under the motor. Retainers are M3 × 4 on the top plate and M3 × 5 on the bottom. The tensioner uses the 5 mm metal lever arms. See the build note below about the shoulder bolts and the motor.

### Hole guide for machining

| Hole | Size | Notes |
|---|---|---|
| **M3 tapped** | Ø2.5 tap drill | Tap M3×0.5. Some are tapped from the bottom of a shallow pocket. |
| **M2 tapped** | Ø1.6 tap drill | On the back top plates (endstop mount). Use cutting fluid and back the tap out often; M2 taps break easily. |
| **M3 / M4 / M5 clearance** | Ø3.2 / Ø4.3 / Ø5.3 | Close fit |
| **Shoulder-bolt holes** | Ø5.00 | Locating fit for the D5 shoulder bolts. For the best fit, drill Ø4.8 and ream to Ø5 H7. |
| **Bearing seats** | Ø13.00 bore, Ø16.20 step: 2.0 mm deep on the XY plates, 2.4 mm on the front plates, 1.6 mm on the back plates | Locating fit for F695 flanged bearings. The deeper XY and front steps set the bearing spans for the Chicago bolt idler shafts. |
| **Motor boss** | Ø22.00 | Locates the NEMA 17 boss on the front top plates |
| **Tensioner slot** | 5.3 mm wide | Clearance, so the tensioner shaft can slide |
| **MR63ZZ seat** (lever arm) | Ø6 H7 × 2.6 mm deep | Light press for the 3 × 6 × 2.5 bearing. If it comes out loose, use a bearing-retaining compound (e.g. Loctite 641 or 609) rather than remachining. |

The pockets and steps (bearing seats, countersunk screw seats, the pulley-clearance relief on the back top plates, the lever arm bearing seat) need a mill; a waterjet or laser can't cut partial-depth features.

### Build note: shoulder-bolt tips stick out 1 mm

The D5 M3 shoulder bolts are the same ones the CF and printed versions use. Their M3 thread is 6 mm long, but the metal bottom plates are 5 mm thick, so about **1 mm of thread sticks out** under each bottom plate when the shoulder is seated. This is expected and doesn't affect function.

If it bothers you, trim the extra millimetre off the thread end: cut it, then run an M3 nut off over the cut to clean up the thread. **Don't put a washer under the bolt head to hide the tip.** That lifts the shoulder off the bottom plate, and the shoulder seating on that plate is what holds the bearing axle rigidly.

### Build note: front corner shoulder bolts thread into the motor

On the **front** motor corners, the four D5 M3 × 30 shoulder bolts are also the motor mounting screws: they pass up through both plates and thread into the motor. With the 5 mm plates, all 6 mm of thread would go into the motor, but NEMA 17 mounting holes are often only about 4.5 mm deep, so the bolts could bottom out before the motor is clamped. Use one of these:

- **2 mm of washers under each shoulder-bolt head** (two 1 mm M5-size washers, which clear the Ø5 shoulder). This leaves about 4 mm of thread in the motor. Unlike on the XY joints and back corners, a washer is fine here: the shoulder still locates in both plates, and the bolt clamps the motor onto the stack.
- **Or trim the M3 thread to 4 mm** (cut 2 mm off, then run an M3 nut off over the cut to clean up the thread), with no washers.

### Build note: front idler Chicago bolts need a shim and a sanded head

Each front live idler is a 30 mm Chicago bolt: the base head at the bottom, an M4 × 8 ultra-thin flat head at the top. Two things differ from the printed and CF versions because of the 5 mm plates:

- **Shim the base head with one M5 washer (5 × 10 × 1 mm).** The bearing span is 29 mm, 1 mm shorter than the bolt, so without the washer the base head doesn't clamp the lower bearing. The bearing's inner race stands slightly proud of its seal, so a standard 10 mm washer bears on the race and clears the seal.
- **Sand the top screw head down to about 1.0 mm.** As supplied, the 1.2 mm head sits only 0.2 mm under the motor. Rub it flat on sandpaper laid on a flat surface until it measures about 1.0 mm; that leaves 0.4 mm, the same as the other versions.

The XY joints need neither: their 40 mm Chicago bolts match the 40 mm bearing span exactly, and nothing sits above or below them.

### Build note: back corner motor screws need washers (or a trim)

The four M3 × 35 screws that hold each back motor pass through both 5 mm plates and the 20 mm standoff. With the thinner metal plates, almost 5 mm of thread would reach the motor, more than most NEMA 17 holes are deep. Put **two M3 washers (3 × 7 × 0.5–0.6 mm) under each head**, as the CAD shows, or **trim 1–2 mm off each screw** (then run an M3 nut off over the cut to clean up the thread). Either way, about 3–4 mm of thread goes into the motor.

Every plate passes [`tools/plate-check.ps1`](../tools), which checks thickness, hole sizes, minimum wall thickness (1.5 mm) and left/right mirror symmetry.
