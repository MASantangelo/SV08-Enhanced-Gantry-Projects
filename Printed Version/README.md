# SV08-P6 Printed Gantry (6 mm)

The printed-plate variant: every gantry plate is 3D printed at 6 mm.

![Full gantry overview, rendered from the current STEP file](Renders/Full%20Gantry%20-%20Overview.png)

## Folder structure

```text
Printed Version/
├── BOM.md                                   Bill of materials with purchase links
├── SV08_P6_Printed_BOM_from_STEP.xlsx       BOM spreadsheet (source for BOM.md)
├── SV08-P6 Dual Shear Live Idlers Front Tensioners.step   Full assembly
├── For Viewing/                             STL preview of the full assembly (~38 MB)
│
├── Base Assemblies/                         Each corner and joint as its own assembly
│   ├── Back Left / Back Right Motor Assembly
│   ├── Front Left / Front Right Motor Assembly
│   ├── XY Joint Left / Right
│   └── For Viewing/                         STL previews
│
├── Base Components/
│   ├── Print Ready/                         ← Print these
│   │   ├── *.step                           Oriented for printing, holes enlarged ~0.3 mm; quantity in the name (4x, 2x)
│   │   ├── Printed Parts All.3mf            Every part on one plate (Creality Print)
│   │   └── For Viewing/                     STL previews
│   └── For Mockups Only/                    Plates in assembled orientation. Do not print.
│       └── For Viewing/                     STL previews
│
├── Renders/                                 Auto-generated from the STEP files (always current)
└── Screenshots/                             Fusion screenshots, belt paths, tensioner motion (GIF + MP4)
```

## Quick links

| I want to... | Go to |
|---|---|
| Buy the hardware | [BOM.md](BOM.md) |
| Print the parts | [Base Components/Print Ready](Base%20Components/Print%20Ready), or the all-in-one [3MF plate](Base%20Components/Print%20Ready/Printed%20Parts%20All.3mf) |
| Look at the assembly in 3D | [Full assembly STL](For%20Viewing/SV08-P6%20Dual%20Shear%20Live%20Idlers%20Front%20Tensioners.stl) · [Sub-assemblies](Base%20Assemblies/For%20Viewing) |
| See the tensioner move | [Front Left Tensioner Motion.gif](Screenshots/Front%20Left%20Tensioner%20Motion.gif) |
| Browse all screenshots | [Screenshots](Screenshots) |

The print-ready plates have their holes enlarged by about 0.3 mm to allow for printing tolerances. That's why they're slightly lighter than the mockup copies, which are dimensioned to nominal size.

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
| ![Front left motor assembly](Renders/Front%20Left%20Motor%20Assembly%20Printed%206mm%20-%20Iso.png) | ![Front right motor assembly](Renders/Front%20Right%20Motor%20Assembly%20Printed%206mm%20-%20Iso.png) | ![XY joint left](Renders/XY%20Joint%20Left%20Printed%206mm%20-%20Iso.png) |
| Front left motor | Front right motor | XY joint left |
| ![Back left motor assembly](Renders/Back%20Left%20Motor%20Assembly%20Printed%206mm%20-%20Iso.png) | ![Back right motor assembly](Renders/Back%20Right%20Motor%20Assembly%20Printed%206mm%20-%20Iso.png) | ![XY joint right](Renders/XY%20Joint%20Right%20Printed%206mm%20-%20Iso.png) |
| Back left motor | Back right motor | XY joint right |
