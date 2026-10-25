# Installing the gantry

This guide builds the gantry in place on the printer, corner by corner. It covers the frame and all four motor corners so far; the XY joints and belt tensioning follow.

**In the pictures:** orange parts are the ones you add in that step; grey parts are already fitted. They show the front left corner of the printed version. Where the carbon fiber or metal version differs, a note under the step says so.

## Before you start

- **The printer:** take the old gantry off so that only the Z carriages (the Z-axis motor mounts) remain, and raise them about 150 mm above the bed to give yourself room to work.
- **Tape:** several parts are pushed up through a plate from below and held with a small piece of tape until the plate above holds them. Painter's tape works well.
- **Threadlocker:** blue (medium strength) for the screw that closes each Chicago bolt.

### Hardware for one front corner

| Qty | Part |
|---:|---|
| 1 | Bottom plate, top plate, front spacer plate (20 mm, printed) and Z carriage spacer (printed) |
| 2 | Tensioner lever arms, each with an MR63ZZ bearing (3 × 6 × 2.5 mm) |
| 3 | F695-2RS flanged bearings: two in the bottom plate (motor shaft and live idler), one in the top plate (live idler) |
| 8 | 695-2RS flanged bearings, in four stacks of two |
| 4 | D5 M3×30 shoulder bolts (these are also the motor screws) |
| 1 | M5×30 Chicago bolt base and 1 M4×8 ultra-thin flat head |
| 2 | GT2 20-tooth pulleys (one live idler, one on the motor) |
| 6 | M3×6 FHCS (bearing retainers; metal: see its BOM) |
| 2 | M3×10 BHCS and 4 M3 shims (0.2 mm), for the lever arms |
| 4 | M4×10 BHCS, 4 M4 washers and 4 M4 T-nuts (if using T-nuts) |
| 2 | M4×45 BHCS and 2 M4 washers (into the Z carriage) |
| 2 | M5×45 BHCS, 2 M5 nuts |
| 12 | M5 washers |
| 4 | M5 spacers, 10 mm OD × 10 mm |
| 1 | M5 spacer, 8 mm OD × 20 mm |
| 1 | M5 spacer, 8 mm OD × 30 mm |
| 8 | M3 heat-set inserts (printed) or M3 nuts (carbon fiber); tapped holes on metal |
| 1 | Motor with a 5 mm × ~37 mm shaft |

## 0. Prepare the parts on the bench

Do this for every corner before you start on the printer.

- **Plates:**
  - **Printed:** press the bearings in first, then fit the heat-set inserts (see [Installing the heat-set inserts](../Printed%20Version/README.md#installing-the-heat-set-inserts)), and run a 5 mm drill through each 5.1 mm shoulder-bolt hole by hand.
  - **Carbon fiber:** drop an M3 nut into each hex pocket with a dab of glue.
  - **Metal:** tap the M3 holes.
- **Lever arms:** press an MR63ZZ bearing into each.

| Bottom plate | Top plate | Lever arms |
|---|---|---|
| ![Bottom plate threaded points](Images/Front%20Corners/00a%20Bottom%20plate%20prep.png) | ![Top plate threaded points](Images/Front%20Corners/00b%20Top%20plate%20prep.png) | ![Lever arm bearings](Images/Front%20Corners/00c%20Lever%20arm%20bearings.png) |

## The frame (all four corners)

### 1. Z carriage spacer and bottom plates

On each corner (not the XY joints), fit the Z carriage spacer, then the bottom plate. Hold them in place temporarily with any M4 bolt at least 12 mm long; it's replaced in step 15.

![Step 1](Images/Front%20Corners/01%20Z%20carriage%20spacer%20and%20bottom%20plate.png)

### 2. Extrusion hardware on the bottom plates

**If you're using T-nuts:** fit the T-nuts, washers and M4×10 bolts on each bottom plate: 2 on each front corner and 4 on each back corner, 12 in all.
**If you're using the extrusions' through holes:** skip this step.

> **Back corners:** on the X extrusion bolt nearest the motor, the printed back motor spacer goes under the bolt head in place of the washer.

![Step 2](Images/Front%20Corners/02%20Bottom%20extrusion%20hardware.png)

### 3. Fit the Y and X extrusions

- **T-nuts:** slide the extrusions onto the T-nuts at each corner.
- **Through holes:** run a bolt through the extrusion and secure it to the plate with a nut, temporarily, so the whole frame holds together.

## Front left corner

### 4. Bottom bearings

Fit the two bearings in the bottom plate (the motor shaft's dual-shear bearing and the live idler's bearing), and secure each with its flat-head retainers.

![Step 4](Images/Front%20Corners/04%20Bottom%20bearings.png)

### 5. Shoulder bolts (×4)

Push the four shoulder bolts up through the bottom plate and hold them with a small piece of tape.

![Step 5](Images/Front%20Corners/05%20Shoulder%20bolts.png)

> **Metal:** put two 1 mm M5 washers under each shoulder-bolt head (or trim the thread to 4 mm), so the bolts don't bottom out in the motor.

### 6. Chicago bolt base

Push the Chicago bolt base up through the live idler's bottom bearing, and hold it with tape.

![Step 6](Images/Front%20Corners/06%20Chicago%20bolt%20base.png)

> **Metal:** put one M5 washer under the base head as a shim.

### 7. Bottom lever arm

Fix the bottom lever arm to the bottom plate with an M3×10 button head and its shims, as shown in the STEP files.

![Step 7](Images/Front%20Corners/07%20Bottom%20lever%20arm.png)

### 8. Tensioner idler bolt

Push an M5×45 up through the bottom, head down, and hold it with tape. This is only temporary: it gives you a post to stack the tensioner idler's bearings on in the next step. In step 17 you take it out and put it back from the top, which is how the picture shows it.

![Step 8](Images/Front%20Corners/08%20Tensioner%20idler%20bolt.png)

### 9. Fill the posts

Add the bearings, spacers and pulley to the six posts from steps 5, 6 and 8. Leave the pulley's set screws loose.

- **Three of the shoulder bolts and the tensioner idler bolt** each get a bearing stack: an M5 washer, two 695 flanged bearings, an M5 washer and a 10 mm M5 spacer.
- **The fourth shoulder bolt** gets the 20 mm M5 spacer only.
- **The Chicago bolt** gets the live idler pulley.

![Step 9](Images/Front%20Corners/09%20Post%20stacks%20and%20idler%20pulley.png)

> **Check the order of the spacers and bearings against the CAD or this guide's pictures for the corner you're building.** On the front left (bottom belt), the bearings sit at the bottom of each stack with the spacer above. On the front right (top belt), it's the other way up. Built the wrong way round, the belt runs at the wrong height.

### 10. Front spacer plate

Set the 20 mm front spacer plate on the bottom plate.

![Step 10](Images/Front%20Corners/10%20Front%20spacer%20plate.png)

### 11. Top plate bearing

Fit the live idler's bearing in the top plate and secure it with its flat-head retainers.

![Step 11](Images/Front%20Corners/11%20Top%20plate%20bearing.png)

### 12. Top extrusion hardware

- **T-nuts:** fit the T-nuts, M4 bolts and washers for the top plate.
- **Through holes:** remove the temporary nut and bolt from this corner.

### 13. Route the belt

Run the belt through the pulleys and bearings, leaving room for the motor pulley. The front left carries the bottom belt; the front right carries the top belt.

### 14. Fit the top plate

Lower the top plate into place and secure it with the T-nuts, or with the through bolts and nuts under the bottom plate.

![Step 14](Images/Front%20Corners/14%20Top%20plate.png)

### 15. Fix the corner to the Z carriage

Replace the temporary bolts from step 1 with two M4×45 button heads and washers. They go down through the top plate, the spacer plate, the bottom plate and the Z carriage spacer into the Z carriage.

![Step 15](Images/Front%20Corners/15%20M4x45%20bolts.png)

### 16. Close the Chicago bolt

Screw the M4×8 ultra-thin flat head into the top of the Chicago bolt, with a drop of blue threadlocker.

![Step 16](Images/Front%20Corners/16%20Ultra-thin%20head.png)

> **Metal:** sand the head down to about 1.0 mm first, so it clears the motor by about 0.4 mm.

### 17. Top lever arm

Holding the top and bottom plates together, place the top lever arm. Carefully remove the tensioner idler bolt from the bottom lever arm, then put it back from the top: through the top arm with a washer, down through the stack, and out through the bottom arm. Secure it underneath with a washer and nut.

![Step 17](Images/Front%20Corners/17%20Top%20lever%20arm.png)

### 18. Top lever arm screw

Fix the top lever arm with an M3×10 button head and its shims.

![Step 18](Images/Front%20Corners/18%20Top%20lever%20screw.png)

### 19. Lever arm end bolt

Fit the second M5×45 at the end of the lever arms: down through the top arm with a washer under its head, through the 30 mm M5 spacer between the arms, and out through the bottom arm. Secure it underneath with a washer and nut.

![Step 19](Images/Front%20Corners/19%20End%20bolt.png)

### 20. Spin check

Before the motor goes on, turn the Chicago bolt and every bearing stack by hand. Everything should spin freely.

### 21. Motor pulley

Fit the pulley onto the motor shaft, with its set screws just loose enough to adjust later.

![Step 21](Images/Front%20Corners/21%20Motor%20pulley.png)

### 22. Fit the motor

Set the motor onto the top plate with its wires facing the side you're working on: the left motor's wires go to the left, the right motor's to the right.

![Step 22](Images/Front%20Corners/22%20Motor.png)

### 23. Secure the motor

Tighten the four shoulder bolts into the motor. They're also the motor screws: about 4.5 mm of thread goes into the motor. If your motor's holes are only 4 mm deep, trim 0.5 mm off each bolt.

### 24. Remove the tape and set the pulleys

Remove all the tape from under the corner. Set each pulley about 0.5 mm clear of the nearest bearing and line the motor pulley up with the belt, then tighten their set screws.

## Front right corner

### 25. Repeat steps 4–24 for the front right

The front right is a mirror image of the front left, but it carries the **top** belt. Check the CAD or the pictures for the order of each bearing stack before you build it (see step 9).

## Back left corner

The frame steps (1–3) have already fitted the Z carriage spacer, the bottom plate and its extrusion hardware on this corner.

### 26. Top plate bearing

On the bench, fit the motor's dual-shear bearing in the top plate and secure it with its two flat-head retainers.

![Step 26](Images/Back%20Corners/26%20Top%20plate%20bearing.png)

### 27. Shoulder bolts and motor screws

Push the two D5 M3×25 shoulder bolts and the four M3×35 motor screws down through the top plate. Hold them in place with tape while you build the next few steps.

- **No washers under the shoulder-bolt heads**, on any version. On the metal version about 1 mm of thread sticks out under the bottom plate; that's expected.
- **Motor screws:** printed and carbon fiber have no washers. **Metal:** put two M3 washers (3 × 7 × 0.5–0.6 mm) under each motor-screw head, so the screws don't bottom out in the motor.

![Step 27](Images/Back%20Corners/27%20Shoulder%20bolts%20and%20motor%20screws.png)

### 28. Standoffs and bearing stacks

- **Each motor screw** gets an M3×20 standoff (8 mm OD).
- **Each shoulder bolt** gets a stack of four 695 flanged bearings, two pairs, one for each belt: M5 washer, two bearings, M5 washer, M5 washer, two bearings, M5 washer. No spacers go on these.

![Step 28](Images/Back%20Corners/28%20Standoffs%20and%20bearing%20stacks.png)

### 29. Back spacer plate

Set the 20 mm back spacer plate on the bottom plate.

![Step 29](Images/Back%20Corners/29%20Back%20spacer%20plate.png)

### 30. Fit the top plate

Carefully lower the top plate, with everything hanging from it, onto the corner. The hardest part is keeping the bearing stacks in place, so angle them in first.

![Step 30](Images/Back%20Corners/30%20Top%20plate.png)

### 31. Tighten the shoulder bolts

Tighten the two shoulder bolts into the bottom plate, seating their shoulders firmly.

### 32. Fix the corner to the Z carriage

Replace the temporary bolts from step 1 with two M4×45 button heads and washers. They go down through the top plate, the back spacer plate, the bottom plate and the Z carriage spacer into the Z carriage.

![Step 32](Images/Back%20Corners/32%20M4x45%20bolts.png)

### 33. Top extrusion hardware

Secure the extrusions to the top plate with T-nuts, M4×10 button heads and washers, or with the through bolts and nuts.

![Step 33](Images/Back%20Corners/33%20Top%20extrusion%20hardware.png)

### 34. Spin check

Turn both bearing stacks by hand. They should spin freely.

### 35. Fit the motor

Fit the motor from below with its pulley on the shaft, set screws loose: its height gets set at the end. The motor's wires face the side you're working on (left motor's wires to the left). Tighten the four motor screws into it.

![Step 35](Images/Back%20Corners/35%20Motor.png)

### 36. Remove the tape

Remove all the tape from the top plate.

### 37. Endstop (if used)

Fit the D2F-L endstop switch on the top plate with two M2×8 screws, and route its cable.

- **Printed and carbon fiber:** the screws go into M2 nuts in the nut traps on the underside of the top plate.
- **Metal:** the screws thread straight into tapped M2 holes, so there are no nuts. Their tips stick out about 0.2 mm under the top plate; a 0.2 mm shim under the switch covers that if you want them flush.

![Step 37](Images/Back%20Corners/37%20Endstop.png)

## Back right corner

### 38. Repeat steps 26–37 for the back right

The back right is a mirror image of the back left, with the same bearing stacks. Its motor drives the **bottom** belt (the back left's drives the top belt), so its pulley sits at a different height: check the CAD or the pictures when you set it at the end.

## Coming next

The XY joints and tensioning the belts are being written up next. Tension the belts only once all the corners and both XY joints are in.

---

[Back to the build guides](README.md) · [FAQ](../FAQ.md)

<sub>Guide format modeled after the [Monolith Gantry](https://github.com/Monolith3D/Monolith_Gantry) documentation.</sub>
