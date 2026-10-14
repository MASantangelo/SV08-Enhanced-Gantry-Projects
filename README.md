# SV08 Enhanced Gantry Projects

**Three styles of parts, one unified system.**

AWD conversion for the Sovol SV08 with dual-shear live XY idlers and front belt tensioners. Build the gantry plates printed, in carbon fiber or in aluminium: every version shares the same layout, hardware, bearings, belts and printed parts, so you can pick the material that suits your tools and budget, or upgrade later without starting over.

> **Built on the work of [Stanciu-Andrei](https://github.com/Stanciu-Andrei).** This project started from the original [Sovol SV08 AWD Mod](https://github.com/Stanciu-Andrei/SovolSV08_AWD_Mod). The working parts here began as those designs before being reworked into the variants below. If you find this useful, go star the original repo and consider [supporting Stanciu on Ko-fi](https://ko-fi.com/C0C510OWNY).

![The gantry split on the diagonal: printed 6 mm plates (upper left) and carbon fiber 6 mm plates (lower right)](Renders/Landing%20-%20Front%20Right.png)

The design comes in three gantry variants:

| Variant | Plate material | Plate thickness | Folder | Status | Bill of materials |
|---|---|---|---|---|---|
| Printed gantry | 3D printed | 6 mm | [`Printed Version`](Printed%20Version) | Available | [BOM](Printed%20Version/BOM.md) · [XLSX](Printed%20Version/SV08_P6_Printed_BOM_from_STEP.xlsx) |
| CF gantry | Carbon fiber (CFRP) | 6 mm | [`CF Version`](CF%20Version) | Available | [BOM](CF%20Version/BOM.md) · [XLSX](CF%20Version/SV08_CF6_BOM_from_STEP.xlsx) |
| Metal gantry | 6061 aluminium | 5 mm | [`Metal Version`](Metal%20Version) | Work in progress (plates available) | — |

Parts that are the same in every version (the spacers and the tensioner lever arm) live in [`Shared Components`](Shared%20Components), and each version's BOM links there for them.

## Printed Version (6 mm)

![Front left tensioner motion](Printed%20Version/Screenshots/Front%20Left%20Tensioner%20Motion.gif)

- `SV08-P6 Dual Shear Live Idlers Front Tensioners.step`: the full assembly
  - `For Viewing/`: STL copy of the full assembly for previewing on GitHub. It's about 38 MB, so give it a few seconds to load. Small hardware is meshed coarser to keep the size down.
- **[Bill of Materials](Printed%20Version/BOM.md)**: every part with quantities, purchase links and notes. It's generated from `SV08_P6_Printed_BOM_from_STEP.xlsx`, which you can also download.
- `Base Assemblies/`: each corner motor assembly and XY joint as its own STEP file
  - `For Viewing/`: STL copies for previewing on GitHub
- `Base Components/Print Ready/`: the printed plates, oriented for printing, with holes enlarged by about 0.3 mm for printing tolerance. The spacers and lever arms are in [`Shared Components/Print Ready`](Shared%20Components/Print%20Ready), with quantities in their file names (for example `4x Z Carriage Spacer`).
  - `Printed Parts All.3mf`: every printed part (plates and shared parts) laid out on one plate, ready to open in your slicer (made in Creality Print)
  - `For Viewing/`: STL copies of the print-ready STEP files, so you can preview them in 3D right on GitHub. The STEP files are the source of truth.
- `Base Components/For Mockups Only/`: plates in their assembled orientation, for reference and mockups. **Do not print these.**
  - `For Viewing/`: STL copies of the mockup STEP files, so you can preview them in 3D right on GitHub.
- [`Renders/`](Printed%20Version/Renders): images of the full gantry and each sub-assembly, generated automatically from the STEP files so they always match the current design
- [`Screenshots/`](Printed%20Version/Screenshots): Fusion screenshots of the assemblies and belt paths, plus an [MP4 of the tensioner motion](Printed%20Version/Screenshots/Front%20Left%20Tensioner%20Motion.mp4)

## Build notes

- **Threadlock the ultra-thin flat heads.** The M3 × 10 ultra-thin flat-head screws thread into the ends of the M3 internally threaded spacers that act as the live idler shafts (2 per front motor assembly, 2 per XY joint). Those shafts spin with the pulleys, so add threadlocker. **Blue (medium strength)** is recommended because you can still remove it with hand tools. Use **red (high strength)** only for a permanent build: removing it takes heat, which can damage the bearings and printed parts nearby.
- **Leave a gap between each pulley and its bearing.** The GT2 pulleys are held by set screws, so you set their height by hand. Leave about 0.5 mm between the pulley face and the nearest bearing; a feeler gauge or a folded piece of paper makes a good shim while you tighten the set screws. The pulley turns with the shaft but the bearing's outer ring doesn't, so a pulley pushed against the bearing will rub. The toothed part of the pulley is 7 mm wide for a 6 mm belt, so this small offset doesn't affect belt tracking.

## Changes from the original

Compared with [Stanciu-Andrei's Sovol SV08 AWD Mod](https://github.com/Stanciu-Andrei/SovolSV08_AWD_Mod):

| | Original | This project |
|---|---|---|
| **Belt tensioning** | At the rear, with dedicated rear tensioner parts | At the front motor mounts, with lever arms. Rear tensioners removed, and the gantry X extrusion shortened to 342 mm. |
| **XY joints** | Standard (non-live) idlers: the pulleys spin freely on fixed shafts | **Live idlers**, in dual shear: GT2 20-tooth pulleys fixed to a shaft that turns on bearing stacks, supported top and bottom. An M3 internally threaded standoff replaces the M5×40 dowel. |
| **Shear support** | Double shear optional, at the rear motors only | Dual shear at every corner and both XY joints. Motors need a 37 mm shaft. |
| **Construction** | Chunky printed corner housings | Flat top and bottom plates held apart by standoffs. One plate design produces the printed (6 mm), carbon fiber (6 mm) and metal (5 mm) versions. |
| **Hardware** | Mostly printed structure | Moving toward a mostly metal design: aluminium standoffs, threaded spacers, shoulder bolts in three lengths, 48 flanged 695-2RS bearings, T-nut mounting, Voron-spec heat-set inserts and D2F-L endstops. Printed alternatives remain for the standoffs. |
| **Files** | STLs, a Fusion `.f3d`, beta CNC plate DXFs | STEP files for every part and sub-assembly, print-oriented parts, an all-in-one 3MF, 3D previews and a full [BOM](Printed%20Version/BOM.md) with purchase links |

## Maintaining this repo

The STL previews and `BOM.md` files are generated by the scripts in [`tools/`](tools), which need FreeCAD. See [tools/README.md](tools/README.md).

## License

Licensed under the [GNU General Public License v3.0](LICENSE), the same license as the original project.

This is a modified version of [Sovol SV08 AWD Mod](https://github.com/Stanciu-Andrei/SovolSV08_AWD_Mod) by Stanciu-Andrei, substantially reworked. See [Changes from the original](#changes-from-the-original) above.

You're free to use, modify, share and sell this design. If you distribute it or anything based on it, you must release it under GPL-3.0 as well, include the design files, and keep these credits.

- Original design © Stanciu-Andrei
- Modifications © 2026 Michael Santangelo
