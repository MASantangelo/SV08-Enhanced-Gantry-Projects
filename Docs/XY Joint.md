# Building the XY joints

Each XY joint carries one end of the toolhead (X) extrusion, rides on a Y rail carriage, and holds two idlers between its top and bottom plates: a **live idler** (a toothed pulley fixed to a Chicago bolt that turns in two bearings) and a **smooth idler** (a pair of flanged bearings on a shoulder bolt).

You need two joints, a left and a right. They're mirror images and go together the same way; the pictures show the right-hand printed joint. Where the carbon fiber or metal version differs, a note under the step says so.

![The finished right-hand XY joint](../Printed%20Version/Renders/XY%20Joint%20Right%20Printed%206mm%20-%20Iso.png)

**In the pictures:** orange parts are the ones you add in that step; grey parts are already fitted.

## Before you start

**Hardware for both joints**

| Qty | Part | Used in |
|---:|---|---|
| 4 | F695-2RS flanged bearing | Live idler (one in each plate) |
| 4 | 695-2RS flanged bearing | Smooth idler stacks |
| 2 | M5×40 Chicago bolt base | Live idler shafts |
| 2 | M4×8 ultra-thin flat head | Closes each Chicago bolt |
| 2 | GT2 20-tooth pulley (set-screw version) | Live idlers |
| 4 | D5 M3×35 shoulder bolt | Hold the plates together |
| 8 | M3×6 FHCS | Bearing retainers (M3×5 on the metal version) |
| 8 | M3×10 BHCS + 8 M3 washers | Y rail carriage |
| 4 | M4×20 BHCS, 4 M4×10 BHCS, 8 M4 washers, 8 M4 T-nuts | Toolhead extrusion |
| 4 | M5 spacer 10 mm OD × 10 mm, 4 M5 washers | Smooth idler stacks |
| 12 | M3 heat-set inserts (printed) / M3 nuts (CF) | Threaded points (tapped holes on the metal version) |

**Plates and spacers:** the four XY plates (top and bottom, left and right) and one 10 mm XY idler spacer per joint, from your version's `Base Components` folder (CF and metal use two 5 mm cut spacers per joint instead), plus one printed 30 mm XY live idler spacer per joint from [`Shared Components/Print Ready`](../Shared%20Components/Print%20Ready).

**Tools:** small metric hex keys (the pulley's M2 set screws need a 0.9 mm key), a soldering iron with a heat-set insert tip (printed version), and blue threadlocker.

## Preparing the plates

### 1. Press the bearing into the bottom plate (×1)

Press one F695 flanged bearing into the bearing seat, flange first into the step, until it sits fully down.

![Step 1](Images/XY%20Joint/01%20Bottom%20plate%20bearing.png)

> **Printed:** fit the bearing **before** the heat-set inserts. It backs up the thin wall between the insert and the bearing seat while the insert goes in.

### 2. Fit the threaded points in the bottom plate (×4)

Turn the plate over. Four threaded points go in from this face: two for the bearing retainers and two for the shoulder bolts.

![Step 2](Images/XY%20Joint/02%20Bottom%20plate%20inserts.png)

- **Printed:** heat-set inserts. Start each one straight by pulling it in with an M3 screw, set it flush or slightly deep, and trim any plastic pushed up around it. See [Installing the heat-set inserts](../Printed%20Version/README.md#installing-the-heat-set-inserts).
- **Carbon fiber:** drop an M3 nut into each hex pocket, with a dab of glue to keep it there while you assemble.
- **Metal:** nothing to fit; these holes are tapped M3.

### 3. Fit the bearing retainers in the bottom plate (×2)

Two M3×6 flat-head screws (M3×5 on metal) clamp the bearing's flange. Snug them down; don't overtighten into a printed plate.

![Step 3](Images/XY%20Joint/03%20Bottom%20plate%20retainers.png)

### 4–6. Do the same for the top plate

Bearing first (×1), then the two threaded points (×2), then the two retainers (×2).

| Bearing | Threaded points | Retainers |
|---|---|---|
| ![Step 4](Images/XY%20Joint/04%20Top%20plate%20bearing.png) | ![Step 5](Images/XY%20Joint/05%20Top%20plate%20inserts.png) | ![Step 6](Images/XY%20Joint/06%20Top%20plate%20retainers.png) |

## Assembling the joint

### 7. Mount the bottom plate to the Y carriage (×4)

Fix the bottom plate to the MGN9H carriage on the Y rail with four M3×10 button heads, each with an M3 washer. If the rail is already on the printer, this is the moment to do it there: the screws are hard to reach once the top plate is on.

![Step 7](Images/XY%20Joint/07%20Y%20carriage.png)

### 8. Fit the live idler shaft and pulley

Push the 40 mm Chicago bolt base up through the bottom bearing from underneath, so its head sits on the bearing. Slide the GT2 pulley onto the shaft with its set screws loose; you'll set its height at the end.

![Step 8](Images/XY%20Joint/08%20Live%20idler%20shaft%20and%20pulley.png)

### 9. Stack the smooth idler and the spacers

Over the shoulder-bolt insert next to the pulley, build the smooth idler from the bottom up: M5 spacer, M5 washer, two 695 flanged bearings with their flanges facing outward, M5 washer, M5 spacer. Put the 30 mm XY live idler spacer over the other shoulder-bolt position, and the 10 mm spacer at the outer end, where the toolhead extrusion sits.

![Step 9](Images/XY%20Joint/09%20Idler%20stack%20and%20spacers.png)

### 10. Attach the toolhead extrusion

Slide two M4 T-nuts into the bottom slot of the toolhead extrusion and two into the top slot. Sit the end of the extrusion on the 10 mm spacer and fix it from below with two M4×20 button heads and washers through the bottom plate and spacer. The bolt holes line up with the stock SV08 toolhead extrusion's holes, 5 mm and 25 mm from its end.

![Step 10](Images/XY%20Joint/10%20Extrusion%20T-nuts.png)

### 11. Close the joint with the top plate

Lower the top plate over the stack, so the Chicago bolt passes through its bearing.

- Two D5 M3×35 shoulder bolts go down through the top plate, the idler stack and the 30 mm spacer, into the bottom plate's threaded points. Seat the shoulders firmly.
- Two M4×10 button heads with washers go into the top T-nuts.
- An M4×8 ultra-thin flat head closes the top of the Chicago bolt. Add a drop of blue threadlocker: the shaft turns with the pulley.

![Step 11](Images/XY%20Joint/11%20Top%20plate.png)

### 12. Set the pulley height

With the belt in place, set the pulley so it runs about 0.5 mm clear of the nearest bearing (a folded piece of paper makes a good shim), then tighten its set screws onto the Chicago bolt. Turn it by hand: the shaft and pulley should spin freely, with no rubbing.

## Checks before moving on

- Both idlers spin freely by hand.
- The joint slides the full length of the Y rail without binding.
- No screw head stands proud where a belt passes.

---

[Back to the build guides](README.md) · [FAQ](../FAQ.md)

<sub>Guide format modeled after the [Monolith Gantry](https://github.com/Monolith3D/Monolith_Gantry) documentation.</sub>
