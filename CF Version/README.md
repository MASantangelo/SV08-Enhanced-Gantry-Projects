# SV08-CF6 Carbon Fiber Gantry (6 mm)

The carbon fiber variant: every gantry plate is cut from 6 mm carbon fiber, and standard M3 hex nuts in hex pockets replace the heat-set inserts used in the printed version.

![Full gantry overview, rendered from the current STEP file](Renders/Full%20Gantry%20-%20Overview.png)

## Folder structure

```text
CF Version/
├── BOM.md                                   Bill of materials with purchase links
├── SV08_CF6_BOM_from_STEP.xlsx              BOM spreadsheet (source for BOM.md)
├── SV08-CF6 Dual Shear Live Idlers Front Tensioners.step   Full assembly
├── For Viewing/                             STL preview of the full assembly (~34 MB)
│
├── Base Assemblies/                         Each corner and joint as its own assembly
│   ├── Back Left / Back Right Motor Assembly
│   ├── Front Left / Front Right Motor Assembly
│   ├── XY Joint Left / Right
│   └── For Viewing/                         STL previews
│
├── Base Components/                         ← Cut these from 6 mm carbon fiber
│   ├── *.step                               12 gantry plates + the 5 mm XY idler spacers
│   ├── CF Printed Parts.3mf                 The shared printed parts a CF build needs, on one plate (OrcaSlicer)
│   └── For Viewing/                         STL previews
│
├── Photos/                                  Photos of real builds
└── Renders/                                 Auto-generated from the STEP files (always current)
```

The spacers and tensioner lever arms are the same in every version, so they live in [`Shared Components`](../Shared%20Components). Print them, or cut the lever arms from CF or metal.

## Quick links

| I want to... | Go to |
|---|---|
| Buy the hardware | [BOM.md](BOM.md) |
| Install it | [Installation guide](../Docs/Installation.md) |
| Cut the plates | [Base Components](Base%20Components) |
| Print the shared parts | [Shared Components/Print Ready](../Shared%20Components/Print%20Ready), or all at once from the [CF Printed Parts 3MF](Base%20Components/CF%20Printed%20Parts.3mf) |
| Look at the assembly in 3D | [Full assembly STL](For%20Viewing/SV08-CF6%20Dual%20Shear%20Live%20Idlers%20Front%20Tensioners.stl) · [Sub-assemblies](Base%20Assemblies/For%20Viewing) |

## What's different from the printed version

- **Plates:** cut from 6 mm carbon fiber instead of printed. The layout matches the printed plates, with machining tolerances built in (see the hole guide below) and a few outlines grown slightly to keep at least 1.5 mm of material around the bearing-retainer screws.
- **Threaded mounting points:** standard M3 hex nuts (ISO 4032), seated in hex pockets, replace the M3 heat-set inserts. The pockets are 5.9 mm across the flats, so a nut drops in and can't turn. A dab of glue (CA or epoxy) keeps each nut in its pocket until its screw is in. Every screw that goes into a nut gets its full thread, apart from the lever-arm screws (about 2.1 of 2.4 mm), which is plenty for a pivot.
- **Everything else is the same:** hardware, bearings, pulleys, belts, extrusions and the shared printed parts.

## Cutting the plates

| Hole | Size | Notes |
|---|---|---|
| **M3 / M4 / M5 clearance** | Ø3.2 / Ø4.3 / Ø5.3 | Close fit. The tensioner slot is 5.3 mm wide. |
| **M3 nut pockets** | 5.9 mm across the flats, R1 corners, 2.5 mm deep (2.4 mm at the bearing retainers on the front bottom plates), with a 1 mm lead-in chamfer | For standard M3 hex nuts; the M3 hole through the rest of the plate is Ø3.2. The 2.4 mm pockets leave a thicker floor at the front bottom retainers. |
| **Shoulder-bolt holes** | Ø5.00 | Locating fit for the D5 shoulder bolts; head counterbores Ø8.3. |
| **Bearing seats** | Ø13.00 bore, Ø16.20 step | Locating fit for the F695 flanged bearings. Step depth: 2.0 mm on the XY plates, 2.6 mm on the front bottoms, 1.4 mm on the front tops, 1.0 mm on the back tops. The XY and front depths set the bearing spans for the Chicago bolt idler shafts. |
| **Bearing-retainer counterbores** | Ø6.2, as deep as the bearing step beside them (1.4–2.6 mm) | For the M3 flat heads that clamp the bearing flanges |
| **Motor boss** | Ø22.00 | Front top plates; merged with the bearing bore, so there's no thin web between them |

- **The pockets need a mill.** Bearing steps, counterbores and the hex nut pockets are partial-depth features, so a waterjet or laser alone can't cut them.
- **Left plates are flipped copies of the right ones.** Each left plate is its right-hand plate turned over, so its pockets are on the opposite face of the file. Machine each plate pocket-side up as it's drawn.
- **XY live idler spacers:** cut from the same 6 mm sheet and machined down to 5 mm, so you don't need a separate 5 mm sheet.
- A few walls and floors are under 1.5 mm on purpose: mostly the floors between the nut pockets and the bearing-retainer counterbores (1.0 mm on the front bottoms), plus a few rims beside the nut pockets and shoulder-bolt holes. They're listed, with the reasons, in [`tools/plate_accepted.json`](../tools/plate_accepted.json).

## Build photos

The first CF XY joint (left), cut from 6 mm carbon fiber and fitted with its Chicago bolt live idler, bearings and pulleys.

| Front | Side |
|---|---|
| ![The left CF XY joint on the printer: the toothed pulley and the bearing stack on the shoulder bolt between the carbon fiber plates, with the orange printed spacer and both belts below](Photos/XY%20Joint%20Left%20CF%20-%20Front.jpg) | ![The left CF XY joint from the side: the bearing stack and the toothed pulley on the Chicago bolt between the two carbon fiber plates](Photos/XY%20Joint%20Left%20CF%20-%20Side.jpg) |

## Renders

Generated automatically from the current STEP files whenever the repo is refreshed (see [tools](../tools)), so they always show the latest design.

| | |
|---|---|
| ![Full gantry, front left](Renders/Full%20Gantry%20-%20Front%20Left.png) | ![Full gantry, front right](Renders/Full%20Gantry%20-%20Front%20Right.png) |
| Front left | Front right |
| ![Full gantry, rear left](Renders/Full%20Gantry%20-%20Rear%20Left.png) | ![Full gantry, overview](Renders/Full%20Gantry%20-%20Overview.png) |
| Rear left | Overview |

### Sub-assemblies

| | | |
|---|---|---|
| ![Front left motor assembly](Renders/Front%20Left%20Motor%20Assembly%20CF6mm%20-%20Iso.png) | ![Front right motor assembly](Renders/Front%20Right%20Motor%20Assembly%20CF6mm%20-%20Iso.png) | ![XY joint left](Renders/XY%20Joint%20Left%20CF6mm%20-%20Iso.png) |
| Front left motor | Front right motor | XY joint left |
| ![Back left motor assembly](Renders/Back%20Left%20Motor%20Assembly%20CF6mm%20-%20Iso.png) | ![Back right motor assembly](Renders/Back%20Right%20Motor%20Assembly%20CF6mm%20-%20Iso.png) | ![XY joint right](Renders/XY%20Joint%20Right%20CF6mm%20-%20Iso.png) |
| Back left motor | Back right motor | XY joint right |
