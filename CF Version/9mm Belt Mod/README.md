# SV08-CF6 Carbon Fiber Gantry for 9 mm Belts

The [CF version](..) set up for 9 mm GT2 belts. The 12 carbon fiber plates are unchanged. The corners open up from a 20 mm to a 30 mm gap to fit two 9 mm idler stacks, and the spacers, bolts, pulleys, belts and motor shafts change to suit.

> [!NOTE]
> **Not just for carbon fiber.** The 9 mm belt mod doesn't need the CF plates. It's modelled on them here as a template, and the same build works with the [aluminum](../../Metal%20Version) and [printed](../../Printed%20Version) versions. Use that version's plates and BOM, and swap in the 9 mm parts from [this BOM](BOM.md): the riser spacers, 30 mm spacer plates, 35 mm XY live idler spacer, shims, 9 mm idlers, pulleys and belts, longer hardware and motor shafts. The differences come from the plate material:
>
> - **Threaded mounting points:** where the CF plates take M3 nuts in hex pockets, printed plates use M3 heat-set inserts and aluminum plates use tapped M3 holes.
> - **Screw lengths:** check any screw that passes through a plate against that version's BOM, since the aluminum plates are 5 mm thick rather than 6.

![Full gantry overview, rendered from the current STEP file](Renders/Full%20Gantry%20-%20Overview.png)

## Where the files are

The 9 mm parts sit in `9mm Belt Mod` folders next to the standard CF files, so everything that hasn't changed is shared with the standard build.

```text
CF Version/
├── 9mm Belt Mod/                              ← You are here
│   ├── BOM.md                                 Bill of materials for the 9 mm build
│   ├── SV08_CF6_9mm_BOM_from_STEP.xlsx        BOM spreadsheet (source for BOM.md)
│   ├── SV08-CF6 Dual Shear Live Idlers Front Tensioners (for 9mm Belts).step   Full assembly
│   ├── For Viewing/                           STL preview of the full assembly (~33 MB)
│   └── Renders/                               Auto-generated from the STEP files
│
├── Base Assemblies/9mm Belt Mod/              Each corner and joint as its own assembly
├── Base Components/9mm Belt Mod/              The three 5 mm riser spacers (cut from CF or print)
└── Base Components/                           The 12 CF plates, same as the standard build

Shared Components/Print Ready/
├── 2x Back Spacer Plate 30mm - For Printing
├── 2x Front Spacer Plate 30mm - For Printing
└── 2x XY Live Idler Spacer 35mm - For Printing
```

## Quick links

| I want to... | Go to |
|---|---|
| Buy the hardware | [BOM.md](BOM.md) |
| Cut the plates | [Base Components](../Base%20Components) (unchanged) and the risers in [Base Components/9mm Belt Mod](../Base%20Components/9mm%20Belt%20Mod) (CF, or print them) |
| Print the shared parts | [Shared Components/Print Ready](../../Shared%20Components/Print%20Ready): the 30 mm spacer plates and the 35 mm XY live idler spacer replace the 20 mm and standard ones |
| Look at the assembly in 3D | [Full assembly STL](For%20Viewing/SV08-CF6%20Dual%20Shear%20Live%20Idlers%20Front%20Tensioners%20%28for%209mm%20Belts%29.stl) · [Sub-assemblies](../Base%20Assemblies/9mm%20Belt%20Mod/For%20Viewing) |

## What's different from the standard CF build

- **Plates:** the same 12 CF plates.
- **Corner gap:** 30 mm instead of 20 mm. A 5 mm riser spacer goes under and over each Y and X extrusion end (the three `5mm Spacer` parts), so the belts stay level with the toolhead's belt clamps.
- **Idlers:** each idler is a flanged 695, a plain 695 and another flanged 695 (12 mm tall, 10 mm between the flanges). Thin 7 mm OD M5 shims, which touch only the inner race, set each idler's height in place of the M5 washers.
- **Belt heights:** at the corners the lower belt runs 8.5 mm above the top face of the bottom plate and the upper belt 21.5 mm, 13 mm apart. The pulleys on the back left and front right motors are flipped to carry the upper belt.
- **XY joints:** the joint gap grows from 30 to 35 mm, with a third 5 mm CF spacer above the X beam, the 35 mm printed live idler spacer, M5 x 45 mm Chicago bolt idler shafts and 9 mm live idler pulleys.
- **Toolhead:** needs 9 mm belt clamps. The CAD uses the Xol 9 mm clamps.
- **Longer hardware:** M3 x 45 back motor screws on 30 mm standoffs, M4 x 55 Z carriage bolts, M4 x 16 extrusion bolts, M5 x 60 tensioner lever bolts, D5 M3 x 40 shoulder bolts, M5 x 40 Chicago bolts in the fronts, and motors with 42–47 mm shafts. The [BOM](BOM.md) lists every change.
- **Everything else is the same:** the plates, cutting tolerances, M3 nut pockets and build order. The [CF README](..) and the [installation guide](../../Docs/Installation.md) still apply.

## Renders

Generated automatically from the current STEP files whenever the repo is refreshed (see [tools](../../tools)).

| | |
|---|---|
| ![Full gantry, front left](Renders/Full%20Gantry%20-%20Front%20Left.png) | ![Full gantry, front right](Renders/Full%20Gantry%20-%20Front%20Right.png) |
| Front left | Front right |
| ![Full gantry, rear left](Renders/Full%20Gantry%20-%20Rear%20Left.png) | ![Full gantry, overview](Renders/Full%20Gantry%20-%20Overview.png) |
| Rear left | Overview |

### Sub-assemblies

| | | |
|---|---|---|
| ![Front left motor assembly](Renders/Front%20Left%20Motor%20Assembly%20CF6mm%20%28For%209mm%20Belts%29%20-%20Iso.png) | ![Front right motor assembly](Renders/Front%20Right%20Motor%20Assembly%20CF6mm%20%28For%209mm%20Belts%29%20-%20Iso.png) | ![XY joint left](Renders/XY%20Joint%20Left%20CF6mm%20%28For%209mm%20Belts%29%20-%20Iso.png) |
| Front left motor | Front right motor | XY joint left |
| ![Back left motor assembly](Renders/Back%20Left%20Motor%20Assembly%20CF6mm%20%28For%209mm%20Belts%29%20-%20Iso.png) | ![Back right motor assembly](Renders/Back%20Right%20Motor%20Assembly%20CF6mm%20%28For%209mm%20Belts%29%20-%20Iso.png) | ![XY joint right](Renders/XY%20Joint%20Right%20CF6mm%20%28For%209mm%20Belts%29%20-%20Iso.png) |
| Back left motor | Back right motor | XY joint right |
