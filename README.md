# SV08 Enhanced Gantry Projects

**Three styles of parts, one unified system.**

AWD conversion for the Sovol SV08 with dual-shear live XY idlers and front belt tensioners. Build the gantry plates in carbon fiber, in aluminium or printed: every version shares the same layout, hardware, bearings, belts and printed parts, so you can pick the material that suits your tools and budget, or upgrade later without starting over.

> **Built on the work of [Stanciu-Andrei](https://github.com/Stanciu-Andrei).** This project started from the original [Sovol SV08 AWD Mod](https://github.com/Stanciu-Andrei/SovolSV08_AWD_Mod). The working parts here began as those designs before being reworked into the variants below. If you find this useful, go star the original repo and consider [supporting Stanciu on Ko-fi](https://ko-fi.com/C0C510OWNY).

![The gantry split three ways from the centre: printed 6 mm on the left, aluminium 5 mm at the top and carbon fiber 6 mm on the right](Renders/Landing%20-%20Front%20Right.png)

## Pick your version

| Version | Plate material | Plate thickness | Threaded mounting points | Folder | Bill of materials |
|---|---|---|---|---|---|
| **[Carbon fiber](#carbon-fiber-version-6-mm)** | Carbon fiber (CFRP) | 6 mm | PEM self-clinching standoffs | [`CF Version`](CF%20Version) | [BOM](CF%20Version/BOM.md) · [XLSX](CF%20Version/SV08_CF6_BOM_from_STEP.xlsx) |
| **[Metal](#metal-version-5-mm)** | 6061 aluminium | 5 mm | Tapped M3 / M2 holes | [`Metal Version`](Metal%20Version) | [BOM](Metal%20Version/BOM.md) · [XLSX](Metal%20Version/SV08_M5_BOM_from_STEP.xlsx) |
| **[Printed](#printed-version-6-mm)** | 3D printed | 6 mm | Heat-set inserts | [`Printed Version`](Printed%20Version) | [BOM](Printed%20Version/BOM.md) · [XLSX](Printed%20Version/SV08_P6_Printed_BOM_from_STEP.xlsx) |

The project was designed around the 6 mm carbon fiber plates; the metal and printed versions use the same layout. Parts that are the same in every version (the spacers and the shared tensioner lever arm) live in [`Shared Components`](Shared%20Components), and each version's BOM links there for them.

Every version folder has the same layout:

- the **full assembly** as a STEP file, with an STL preview in `For Viewing/`
- **`BOM.md`** and the spreadsheet it's generated from
- **`Base Assemblies/`**: each corner motor assembly and XY joint as its own STEP file, with STL previews
- **`Base Components/`**: the plates, with STL previews
- **`Renders/`**: images of the full gantry and each sub-assembly, generated from the STEP files so they always match the current design

## Carbon fiber version (6 mm)

![Carbon fiber front right motor assembly](CF%20Version/Renders/Front%20Right%20Motor%20Assembly%20CF6mm%20-%20Iso.png)

The 12 gantry plates are cut from 6 mm carbon fiber, with PEM self-clinching standoffs (SO-M3-3ZI and SO-M3-6ZI) in place of heat-set inserts. Full details are in the [CF README](CF%20Version/README.md).

**CF build notes**

- **Cut the plates with a mill.** The bearing steps, counterbores and hex PEM pockets are partial-depth features, so a waterjet or laser alone can't make them. Hole sizes and tolerances are in the CF README's [hole guide](CF%20Version/README.md#cutting-the-plates).
- **Epoxy the PEM standoffs.** Carbon fiber doesn't flow around a self-clinching standoff the way sheet metal does, so lock each one in its hex pocket with epoxy. We've used [this epoxy](https://amazon.com/dp/B0CTB8GHYP).
- **Left plates are flipped copies of the right ones**, so their pockets are on the opposite face of the file. Machine each plate pocket-side up as it's drawn.
- **XY live idler spacers** are cut from the same 6 mm sheet and machined down to 5 mm.

## Metal version (5 mm)

![Metal front right motor assembly](Metal%20Version/Renders/Front%20Right%20Motor%20Assembly%20Metal5mm%20-%20Iso.png)

The 12 gantry plates, the XY spacers and the 4 tensioner lever arms are machined from 5 mm 6061 aluminium. The M3 and M2 holes are tapped, so there are no inserts, standoffs or M2 nuts. Full details are in the [Metal README](Metal%20Version/README.md).

**Metal build notes**

- **Machine and tap the plates.** The pockets need a mill; the tap drills, close-fit clearances and locating fits are in the Metal README's [hole guide](Metal%20Version/README.md#hole-guide-for-machining).
- **Front corners: shim or trim the shoulder bolts.** The D5 M3 × 30 shoulder bolts are also the motor screws. With the 5 mm plates, put two 1 mm M5 washers under each head, or trim the thread to 4 mm, so they don't bottom out in the motor ([details](Metal%20Version/README.md#build-note-front-corner-shoulder-bolts-thread-into-the-motor)).
- **Back corners: shim or trim the motor screws.** The M3 × 35 screws that hold each back motor would put almost 5 mm of thread into the motor with the 5 mm plates. Put two M3 washers under each head, or trim 1–2 mm off each screw ([details](Metal%20Version/README.md#build-note-back-corner-motor-screws-need-washers-or-a-trim)).
- **XY joints and back corners: about 1 mm of shoulder-bolt thread sticks out** under the bottom plates. That's expected. Trim it if you like, but don't add a washer under the head ([details](Metal%20Version/README.md#build-note-shoulder-bolt-tips-stick-out-1-mm)).
- **Use the metal tensioner lever arm** (`Tensioner Lever Arm Revised - 5mm Metal Only`), not the shared one.

## Printed version (6 mm)

![Front left tensioner motion](Printed%20Version/Screenshots/Front%20Left%20Tensioner%20Motion.gif)

The plates are 3D printed at 6 mm with M3 heat-set inserts. This is the easiest version to build if you have a printer and no access to a mill.

> [!NOTE]
> **These are the v2 printed parts.** v2 reworks every printed plate:
> - support-free printing, with every pocket on one face
> - thicker walls, checked against printed-part rules
> - revised bearing seats and fits
> - a single 10 mm XY idler spacer in place of two 5 mm ones
> - stainless Chicago bolt live idler shafts that clamp both bearings over their full width
> - XY joint bolt holes that line up with the stock SV08 toolhead extrusion
>
> The original v1 printed files are still available in the [Printed v1 release](https://github.com/MASantangelo/SV08-Enhanced-Gantry-Projects/releases/tag/printed-v1).

**Printed build notes**

- **Print the parts from `Base Components/Print Ready/`.** They're oriented for printing, with holes enlarged by about 0.3 mm for printing tolerance. The spacers and lever arms are in [`Shared Components/Print Ready`](Shared%20Components/Print%20Ready), with quantities in their file names (for example `4x Z Carriage Spacer`).
- **Fit the heat-set inserts carefully.** Press the bearings in first so they back up the thin walls beside some inserts. Start each insert straight by pulling it into its seat with an M3 screw through the screw hole. Set each insert flush or slightly deep, never proud. Push any plastic that bulges into an empty bearing seat back with a spudger, trim plastic pushed up around the insert, and chase each insert with an M3 screw from the side opposite the real screw, so loose plastic gets pushed out rather than into the threads. A crooked or plastic-filled insert cross-threads its screw, and a stuck screw can ruin the plate. Step-by-step in the [Printed README](Printed%20Version/README.md#installing-the-heat-set-inserts).
- **Drill out the shoulder-bolt holes.** They're modelled at Ø5.1 so they print close to 5 mm. Run a 5 mm drill bit through each one by hand for a snug, consistent fit on the D5 shoulder bolts.
- **The live idler shafts are Chicago bolts.** Each one is a 304 stainless Chicago bolt base (5 mm barrel, 40 mm in the XY joints, 30 mm at the fronts) with its head on one bearing and an M4 × 8 ultra-thin flat head on the other, so both bearings are clamped and the idler can't float. At the fronts, put the base head at the bottom and the ultra-thin head at the top, where it sits 0.4 mm under the motor. Don't use the M4 × 4 screws that come with the Chicago bolts: their 2 mm heads don't clear the front motors.
- **`Printed Parts All.3mf`** has every printed part (plates and shared parts) laid out on one plate, ready to open in your slicer (made in OrcaSlicer).
- [`Screenshots/`](Printed%20Version/Screenshots) has Fusion screenshots of the assemblies and belt paths, plus an [MP4 of the tensioner motion](Printed%20Version/Screenshots/Front%20Left%20Tensioner%20Motion.mp4).

## Build notes for every version

- **Threadlock the ultra-thin flat heads.** The live idler shafts (one per front motor assembly, one per XY joint) are held by ultra-thin flat-head screws. On the printed version, each shaft is a 304 stainless Chicago bolt (5 mm barrel, 30 mm at the fronts and 40 mm at the XY joints) with an M4 × 8 ultra-thin flat head in one end. On the CF and metal versions, it's an M3 internally threaded spacer with an M3 × 10 ultra-thin flat head in each end. Those shafts spin with the pulleys, so add threadlocker. **Blue (medium strength)** is recommended because you can still remove it with hand tools. Use **red (high strength)** only for a permanent build: removing it takes heat, which can damage the bearings and printed parts nearby.
- **Check your motors' screw-hole depth (front corners, CF and printed).** On each front motor corner, the four D5 M3 × 30 shoulder bolts are also the motor screws: they pass up through both plates and thread into the motor. On the carbon fiber and printed versions, about 4.5 mm of thread goes into the motor, which suits the usual 4.5 mm-deep NEMA 17 holes. Some motors only have 4 mm-deep holes; on those, the bolts can bottom out before the motor is clamped. If yours are 4 mm, trim 0.5 mm off the end of each bolt's thread, then run an M3 nut off over the cut to clean up the thread. The metal version has its own note above.
- **Reuse your stock extrusions.** The front and back motor mounts line up with the existing M4 holes in the stock SV08 gantry Y (469 mm) and gantry X extrusions. The gantry X is shortened to 342 mm; to keep the stock 345 mm one uncut, use a 6 mm OD (or smaller) M3 × 20 mm spacer in the spot nearest each end of it, one per back corner. If you do cut it, take 1.5 mm off each end so the holes still line up. The printed XY joints also line up with the stock toolhead extrusion's holes. On the CF and metal versions they don't yet, so mount those XY joints with M4 T-nuts in the slots, or use a toolhead extrusion drilled to match. Hole positions are in the [Stock Parts](Shared%20Components/README.md#stock-parts) models.
- **Leave a gap between each pulley and its bearing.** The GT2 pulleys are held by set screws, so you set their height by hand. Leave about 0.5 mm between the pulley face and the nearest bearing; a feeler gauge or a folded piece of paper makes a good shim while you tighten the set screws. The pulley turns with the shaft but the bearing's outer ring doesn't, so a pulley pushed against the bearing will rub. The toothed part of the pulley is 7 mm wide for a 6 mm belt, so this small offset doesn't affect belt tracking.

## Changes from the original

Compared with [Stanciu-Andrei's Sovol SV08 AWD Mod](https://github.com/Stanciu-Andrei/SovolSV08_AWD_Mod):

| | Original | This project |
|---|---|---|
| **Belt tensioning** | At the rear, with dedicated rear tensioner parts | At the front motor mounts, with lever arms. Rear tensioners removed, and the gantry X extrusion shortened to 342 mm. |
| **XY joints** | Standard (non-live) idlers: the pulleys spin freely on fixed shafts | **Live idlers**, in dual shear: GT2 20-tooth pulleys fixed to a shaft that turns on bearing stacks, supported top and bottom. A stainless Chicago bolt (printed) or an M3 internally threaded standoff (CF and metal) replaces the M5×40 dowel. |
| **Shear support** | Double shear optional, at the rear motors only | Dual shear at every corner and both XY joints. Motors need a 37 mm shaft. |
| **Construction** | Chunky printed corner housings | Flat top and bottom plates held apart by standoffs. One plate design produces the carbon fiber (6 mm), metal (5 mm) and printed (6 mm) versions. |
| **Hardware** | Mostly printed structure | Moving toward a mostly metal design: aluminium standoffs, Chicago bolt or threaded-spacer idler shafts, shoulder bolts in three lengths, 48 flanged 695-2RS bearings, T-nut mounting and D2F-L endstops, with PEM standoffs (CF), tapped holes (metal) or Voron-spec heat-set inserts (printed). Printed alternatives remain for the standoffs. |
| **Files** | STLs, a Fusion `.f3d`, beta CNC plate DXFs | STEP files for every part and sub-assembly in all three versions, print-oriented parts and an all-in-one 3MF, 3D previews, renders and a full BOM with purchase links for each version |

## Maintaining this repo

The STL previews, renders and `BOM.md` files are generated by the scripts in [`tools/`](tools), which need FreeCAD. The plate checks (hole sizes, minimum walls, mirror pairs) are there too. See [tools/README.md](tools/README.md).

## License

Licensed under the [GNU General Public License v3.0](LICENSE), the same license as the original project.

This is a modified version of [Sovol SV08 AWD Mod](https://github.com/Stanciu-Andrei/SovolSV08_AWD_Mod) by Stanciu-Andrei, substantially reworked. See [Changes from the original](#changes-from-the-original) above.

You're free to use, modify, share and sell this design. If you distribute it or anything based on it, you must release it under GPL-3.0 as well, include the design files, and keep these credits.

- Original design © Stanciu-Andrei
- Modifications © 2026 Michael Santangelo
