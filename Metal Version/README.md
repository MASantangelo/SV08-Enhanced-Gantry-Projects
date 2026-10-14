# SV08 Metal Gantry (5 mm)

**Work in progress.** The plates are designed and checked. Sub-assemblies are being added one at a time; the full assembly, bill of materials and remaining renders are still to come.

The metal variant: every gantry plate is machined from 5 mm 6061 aluminium, with tapped M3 holes in place of the heat-set inserts (printed) and PEM standoffs (CF).

## Plates (available now)

[`Base Components`](Base%20Components) has all 13 parts as STEP files, with 3D previews in [`Base Components/For Viewing`](Base%20Components/For%20Viewing):

- 4 front corner plates, 4 back corner plates and 4 XY live idler plates, in mirrored left/right pairs
- the 5 mm XY live idler spacer

The spacers and tensioner lever arms that every version shares are in [`Shared Components`](../Shared%20Components).

## Sub-assemblies (in progress)

[`Base Assemblies`](Base%20Assemblies) has each finished sub-assembly as STEP, with a 3D preview in [`Base Assemblies/For Viewing`](Base%20Assemblies/For%20Viewing).

| XY Joint Left | XY Joint Right |
|---|---|
| ![XY joint left, metal](Renders/XY%20Joint%20Left%20Metal5mm%20-%20Iso.png) | ![XY joint right, metal](Renders/XY%20Joint%20Right%20Metal5mm%20-%20Iso.png) |
| **Back Left Motor** | **Back Right Motor** |
| ![Back left motor assembly, metal](Renders/Back%20Left%20Motor%20Assembly%20Metal5mm%20-%20Iso.png) | ![Back right motor assembly, metal](Renders/Back%20Right%20Motor%20Assembly%20Metal5mm%20-%20Iso.png) |

- **XY joints:** live idler in dual shear. The bearing retainers are M3 × 5 flat heads that end flush with the plate faces.
- **Back motor corners:** the bearing retainers are M3 × 4 flat heads, which end on the floor of the pulley-clearance relief. The D2F endstop screws straight into tapped M2 holes, so no nuts are needed. Its M2 × 8 screws stick out about 0.2 mm under the top plate; a 0.2 mm shim from the tensioner hardware covers that if you want it flush.

### Hole guide for machining

| Hole | Size | Notes |
|---|---|---|
| **M3 tapped** | Ø2.5 tap drill | Tap M3×0.5. Some are tapped from the bottom of a shallow pocket. |
| **M2 tapped** | Ø1.6 tap drill | On the back top plates (endstop mount). Use cutting fluid and back the tap out often; M2 taps break easily. |
| **M3 / M4 / M5 clearance** | Ø3.2 / Ø4.3 / Ø5.3 | Close fit |
| **Shoulder-bolt holes** | Ø5.00 | Locating fit for the D5 shoulder bolts. For the best fit, drill Ø4.8 and ream to Ø5 H7. |
| **Bearing seats** | Ø13.00 bore, Ø16.20 × 1.6 mm step | Locating fit for F695 flanged bearings |
| **Motor boss** | Ø22.00 | Locates the NEMA 17 boss on the front top plates |
| **Tensioner slot** | 5.3 mm wide | Clearance, so the tensioner shaft can slide |

The pockets and steps (bearing seats, countersunk screw seats, the pulley-clearance relief on the back top plates) need a mill; a waterjet or laser can't cut partial-depth features.

### Build note: shoulder-bolt tips stick out 1 mm

The D5 M3 shoulder bolts are the same ones the CF and printed versions use. Their M3 thread is 6 mm long, but the metal bottom plates are 5 mm thick, so about **1 mm of thread sticks out** under each bottom plate when the shoulder is seated. This is expected and doesn't affect function.

If it bothers you, trim the extra millimetre off the thread end: cut it, then run an M3 nut off over the cut to clean up the thread. **Don't put a washer under the bolt head to hide the tip.** That lifts the shoulder off the bottom plate, and the shoulder seating on that plate is what holds the bearing axle rigidly.

Every plate passes [`tools/plate-check.ps1`](../tools), which checks thickness, hole sizes, minimum wall thickness (1.5 mm) and left/right mirror symmetry.
