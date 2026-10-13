# SV08-CF6 Carbon Fiber Gantry (6 mm)

The carbon fiber variant: every gantry plate is cut from 6 mm carbon fiber, and PEM self-clinching standoffs replace the heat-set inserts used in the printed version.

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
│   └── For Viewing/                         STL previews
│
└── Renders/                                 Auto-generated from the STEP files (always current)
```

The spacers and tensioner lever arms are the same in every version, so they live in [`Shared Components`](../Shared%20Components). Print them, or cut the lever arms from CF or metal.

## Quick links

| I want to... | Go to |
|---|---|
| Buy the hardware | [BOM.md](BOM.md) |
| Cut the plates | [Base Components](Base%20Components) |
| Print the shared parts | [Shared Components/Print Ready](../Shared%20Components/Print%20Ready) |
| Look at the assembly in 3D | [Full assembly STL](For%20Viewing/SV08-CF6%20Dual%20Shear%20Live%20Idlers%20Front%20Tensioners.stl) · [Sub-assemblies](Base%20Assemblies/For%20Viewing) |

## What's different from the printed version

- **Plates:** cut from 6 mm carbon fiber instead of printed. They are the same shapes as the printed plates, dimensioned to nominal size.
- **Threaded mounting points:** PEM self-clinching standoffs (SO-M3-3ZI and SO-M3-6ZI), pressed into the plates, replace the M3 heat-set inserts.
- **Everything else is the same:** hardware, bearings, pulleys, belts, extrusions and the shared printed parts.

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
