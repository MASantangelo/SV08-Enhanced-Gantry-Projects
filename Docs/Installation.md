# Installing the gantry

This guide builds the gantry in place on the printer, corner by corner. It covers everything from the bare printer to tensioned belts: the frame, all four motor corners, the XY joints, routing the belts, setting the pulleys and tensioning.

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

### Hardware for one back corner

| Qty | Part |
|---:|---|
| 1 | Bottom plate, top plate, back spacer plate (20 mm, printed), Z carriage spacer (printed) and printed back motor spacer |
| 1 | F695-2RS flanged bearing (the motor's dual-shear bearing, in the top plate) |
| 8 | 695-2RS flanged bearings, in two stacks of four |
| 2 | D5 M3×25 shoulder bolts |
| 4 | M3×35 SHCS (motor screws), plus 8 M3 washers on metal (two under each head) |
| 4 | M3×20 standoffs, 8 mm OD |
| 2 | M3×6 FHCS bearing retainers (M3×4 on metal) |
| 8 | M5 washers |
| 1 | GT2 20-tooth pulley (on the motor) |
| 8 | M4×10 BHCS and 8 M4 T-nuts (if using T-nuts): four on the bottom plate, four on the top |
| 2 | M4×45 BHCS (into the Z carriage) |
| 9 | M4 washers: three under the bottom-plate bolts (the printed back motor spacer replaces the fourth), four on the top plate, two under the M4×45 heads |
| 4 | M3 heat-set inserts (printed) or M3 nuts (carbon fiber); tapped holes on metal |
| 1 | D2F-L endstop switch with 2 M2×8 SHCS, plus 2 M2 nuts on printed and carbon fiber (optional) |
| 1 | Motor with a 5 mm × ~37 mm shaft |

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

## XY joints

The pictures show the left joint of the printed version.

### Hardware for one XY joint

| Qty | Part |
|---:|---|
| 1 | Bottom plate and top plate |
| 1 | 10 mm XY idler spacer (printed version; CF and metal use two 5 mm cut spacers) |
| 1 | 30 mm XY live idler spacer, printed, from [`Shared Components/Print Ready`](../Shared%20Components/Print%20Ready) (all versions) |
| 2 | F695-2RS flanged bearings (one in each plate) |
| 2 | 695-2RS flanged bearings (the idler stack) |
| 1 | M5×40 Chicago bolt base and 1 M4×8 ultra-thin flat head |
| 1 | GT2 20-tooth pulley |
| 2 | D5 M3×35 shoulder bolts |
| 4 | M3×6 FHCS bearing retainers (M3×5 on metal) |
| 4 | M3×10 BHCS and 4 M3 washers (Y carriage) |
| 2 | M4×20 BHCS, 2 M4×10 BHCS, 4 M4 washers and 4 M4 T-nuts (if using T-nuts) |
| 2 | M5 washers, plus M5 spacers (10 mm OD): one 20 mm on the left joint, two 10 mm on the right |
| 6 | M3 heat-set inserts (printed) or M3 nuts (carbon fiber); tapped holes on metal |

### 39. Y rails and carriages

Fit the linear rails to the Y extrusions, with their carriages, if they aren't on already. They're reused from the stock printer.

### 40. Bottom plate bearing

Fit the live idler's bearing in each XY bottom plate and secure it with its two flat-head retainers (M3×6, or M3×5 on metal).

![Step 40](Images/XY%20Joints/40%20Bottom%20plate%20bearing.png)

### 41. Mount the bottom plates to the Y carriages

Fix the left and right bottom plates to their Y carriages with four M3×10 button heads, each with an M3 washer. These are hard to reach later, so tighten them now.

![Step 41](Images/XY%20Joints/41%20Y%20carriage.png)

### 42. Extrusion spacer

Set the extrusion spacer on each bottom plate: the printed 10 mm spacer, or two 5 mm cut spacers on the carbon fiber and metal versions.

![Step 42](Images/XY%20Joints/42%20Extrusion%20spacer.png)

### 43. Bottom extrusion bolts

**If you're using T-nuts:** fit two M4×20 button heads with washers up through the bottom plate and spacer, with a T-nut on each. They're longer than the top bolts because they also pass through the spacer.

![Step 43](Images/XY%20Joints/43%20Bottom%20extrusion%20bolts.png)

### 44. Fit the toolhead extrusion

Fix the toolhead (X) extrusion to both bottom plates, with its X rail and carriage already on (reused from the stock printer). Use the T-nuts, or the extrusion's through holes and through bolts.

### 45. Chicago bolt base

Push the 40 mm Chicago bolt base up through each bottom plate's bearing, and hold it with tape.

![Step 45](Images/XY%20Joints/45%20Chicago%20bolt%20base.png)

### 46. Pulley

Slide the pulley onto the Chicago bolt and leave its set screws loose; its height gets set at the end.

![Step 46](Images/XY%20Joints/46%20Pulley.png)

### 47. Top plate bearing

On the bench, fit the live idler's bearing in each top plate and secure it with its two flat-head retainers.

![Step 47](Images/XY%20Joints/47%20Top%20plate%20bearing.png)

### 48. Top extrusion bolts

**If you're using T-nuts:** fit two M4×10 button heads with washers through the top plate, with a T-nut on each.

![Step 48](Images/XY%20Joints/48%20Top%20extrusion%20bolts.png)

### 49. Shoulder bolts

Push the two D5 M3×35 shoulder bolts down through the top plate.

![Step 49](Images/XY%20Joints/49%20Shoulder%20bolts.png)

### 50. Idler stack

On the shoulder bolt nearest the pulley, fit the spacers and bearing stack.

- **Left joint:** a 20 mm M5 spacer, then an M5 washer, two 695 flanged bearings and an M5 washer.
- **Right joint:** a 10 mm M5 spacer, an M5 washer, two 695 flanged bearings, an M5 washer and another 10 mm spacer.

![Step 50](Images/XY%20Joints/50%20Bearing%20stack.png)

> **The left and right joints are built differently, so check the CAD or this guide's pictures for the stack order and pulley height of the joint you're building.** The left joint's bearings and pulley sit lower than the right's, so each belt runs at its own height.

### 51. Printed spacer

Fit the printed 30 mm XY live idler spacer over the second shoulder bolt.

![Step 51](Images/XY%20Joints/51%20Printed%20spacer.png)

### 52. Fit the top plate

Lower the top plate onto the extrusion, making sure the Chicago bolt slides into the top bearing.

![Step 52](Images/XY%20Joints/52%20Top%20plate.png)

### 53. Tighten the shoulder bolts

Tighten the two shoulder bolts into the bottom plate, seating their shoulders firmly.

### 54. Lock the plates to the extrusion

Tighten the T-nut bolts, or the through bolts, to lock the plates to the toolhead extrusion.

### 55. Close the Chicago bolt

Screw the M4×8 ultra-thin flat head into the top of the Chicago bolt, with a drop of blue threadlocker.

![Step 55](Images/XY%20Joints/55%20Ultra-thin%20head.png)

### 56. Spin check

Turn the Chicago bolt and the bearing stack by hand. Both should spin freely.

### 57. Remove the tape

Remove the tape from under the Chicago bolt.

### 58. The other joint

Steps 40–57 cover both joints. Build the second one the same way, but with its own stack order (step 50).

## Routing the belts

Route the **bottom belt first**, then the top belt. Each belt's ends were already fitted into its front corner (step 13): the front left carries the bottom belt and the front right carries the top belt.

The pictures show each belt in orange, seen from above with the front of the printer at the bottom. The top plates and motors are hidden so you can see the pulleys. The [Fusion screenshots](../Printed%20Version/Screenshots) also have a `Top Belt Path` and a `Bottom Belt Path` image.

### 59. Fit the toolhead

Fit your toolhead to the X rail's carriage. A printed belt helper that holds the belt ends in place of the toolhead, like [this SV08 belt helper for the X carriage](https://www.printables.com/model/1027579-sovol-sv08-belt-helper-for-x-carriage), makes routing and tensioning easier.

### The bottom belt

![The bottom belt path](Images/Belts/59%20Bottom%20belt.png)

#### 60. Front left to the left XY joint

Take the end of the bottom belt that leaves the front left's live idler, and guide it to the toothed pulley on the left XY joint.

#### 61. Into the toolhead

From that toothed pulley, fit the belt into the toolhead or the belt helper.

#### 62. Front left to the back left

Take the other end of the belt from the front left, and guide it past the left XY joint to the back left corner.

#### 63. Around the back left

At the back left, the bottom belt only goes around the 695 bearing stacks; it doesn't go near the motor. Route it on toward the back right corner.

#### 64. Around the back right motor

At the back right, the bottom belt goes around the first smooth idler, wraps around the motor's toothed pulley, then loops back around the second smooth idler and heads toward the right XY joint.

#### 65. Around the right XY joint

At the right XY joint, the bottom belt goes around the smooth idler, at bottom-belt height, and turns toward the toolhead.

#### 66. Into the toolhead

Fit this end of the bottom belt into the toolhead or the belt helper.

### The top belt

![The top belt path](Images/Belts/67%20Top%20belt.png)

#### 67. Front right to the right XY joint

Take the end of the top belt that leaves the front right's live idler, guide it to the right XY joint, wrap it around the toothed pulley there and on toward the toolhead.

#### 68. Into the toolhead

Fit it into the toolhead or the belt helper.

#### 69. Front right to the back right

Take the other end of the belt from the front right, and guide it to the back right corner. There it goes around the corner without going near the motor, and on toward the back left corner.

#### 70. Around the back left motor

At the back left, the top belt goes smooth idler, then around the motor's toothed pulley, then the second smooth idler.

#### 71. Toward the left XY joint

After the second smooth idler, it heads toward the left XY joint.

#### 72. Around the left XY joint

At the left XY joint, it goes around the smooth idler and turns toward the toolhead.

#### 73. Into the toolhead

Fit this end of the top belt into the toolhead or the belt helper.

## Setting the pulleys

### 74. Set the pulley heights

Now that the belts are routed, set each toothed pulley's final height and tighten its set screws. Measure from the pulley to the plate face next to it; stacked sheets of printer paper (about 0.1 mm each) make a handy gauge.

| Corner | Pulley | Gap |
|---|---|---|
| Front left | Both toothed pulleys (motor and live idler) | 0.25–0.35 mm from the bottom face of the pulley to the top face of the bottom plate (about 3 sheets of paper) |
| Back right | Motor pulley | 0.25–0.35 mm from the bottom face of the pulley to the top face of the bottom plate |
| Left XY joint | Live idler pulley | 10.25–10.3 mm from the bottom face of the pulley to the top face of the bottom plate |
| Front right | Both toothed pulleys (motor and live idler) | About 1 mm from the top face of the pulley to the bottom face of the top plate |
| Back left | Motor pulley | About 1 mm from the top face of the pulley to the bottom face of the top plate |
| Right XY joint | Live idler pulley | About 0.5 mm from the top face of the pulley to the bottom face of the top plate |

The bottom belt's pulleys (front left, back right, left XY joint) are measured up from the bottom plate; the top belt's (front right, back left, right XY joint) are measured down from the top plate.

## Tensioning the belts

Check the tension as soon as both belts are fitted into the toolhead (or the belt helper), and set it with the lever arms on the two front corners: the front left tensions the bottom belt, the front right the top belt.

### What to aim for

Aim for **6–8 lb (26.7–35.6 N) on each belt span**, with both belts the same. Measure it by plucking a free span and reading its frequency with a phone app or Klipper's tools. The frequency depends on the span's length, measured between the points where the belt leaves its pulleys:

| Free span | 6 lb (26.7 N) | 7 lb (31.1 N) | 8 lb (35.6 N) |
|---|---|---|---|
| 100 mm | 289 Hz | 312 Hz | 334 Hz |
| 150 mm | 193 Hz | 208 Hz | 222 Hz |
| 200 mm | 144 Hz | 156 Hz | 167 Hz |

These assume about 8 g/m for a 6 mm GT2 belt; a different belt shifts them by a few hertz. Don't go past the top of the range: over-tensioning can break a belt.

### 75. Tighten the lever arm's fixed points

Tighten the lever arm end bolt (the M5 with the long 30 mm spacer) and the two M3 screws the lever arms pivot on.

### 76. Ready the tensioner idler bolt

Put the hex key in the head of the tensioner idler bolt: the M5 that carries the idler bearings. Loosen it just enough that the idler can slide.

### 77. Pull the lever

Pull the tensioner lever arm to the side. The idler, which floats in its slot, moves the opposite way and takes up the belt.

### 78. Hold the nut

With a pair of slip-joint pliers, grip the nut on the bottom of the tensioner idler bolt. Push one leg of the pliers against the end bolt's nut next to it: that holds the lever and the idler in place.

| Hex key in the idler bolt, pliers on the nut | From below: one jaw on the idler nut, the other braced on the end bolt's nut |
|---|---|
| ![Tensioning a front corner: hex key in the top of the tensioner idler bolt, slip-joint pliers holding the nut underneath](Images/Tensioning/78%20Hex%20key%20and%20pliers.jpg) | ![The slip-joint pliers seen from below, gripping the tensioner idler nut with one jaw braced against the lever arm end bolt's nut](Images/Tensioning/78%20Pliers%20from%20below.jpg) |

### 79. Lock it

While the pliers hold everything, tighten the tensioner idler bolt with the hex key.

### 80. Measure and even out

Measure each belt, then repeat steps 76–79 on either corner until both belts are within the target range and match each other. Check the tension again after the first few hours of printing.

---

[Back to the build guides](README.md) · [FAQ](../FAQ.md)

<sub>Guide format modeled after the [Monolith Gantry](https://github.com/Monolith3D/Monolith_Gantry) documentation.</sub>
