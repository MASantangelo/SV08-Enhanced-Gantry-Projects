# SV08-P6 Printed Gantry (6 mm)

The printed-plate variant: every gantry plate is 3D printed at 6 mm.

![Full assembled gantry overview](Screenshots/Full%20Assembled%20Gantry%20Overview.png)

## Folder structure

```text
Printed Version/
├── BOM.md                                   Bill of materials with purchase links
├── SV08_P6_Printed_BOM_from_STEP.xlsx       BOM spreadsheet (source for BOM.md)
├── SV08-P6 Dual Shear Live Idlers Front Tensioners.step   Full assembly
├── SV08-P6_..._FusionBOMExport.csv          Raw Fusion BOM export
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
│   │   ├── *.step                           Oriented for printing; quantity in the name (4x, 2x)
│   │   ├── Printed Parts All.3mf            Every part on one plate (Creality Print)
│   │   └── For Viewing/                     STL previews
│   └── For Mockups Only/                    Plates in assembled orientation. Do not print.
│       └── For Viewing/                     STL previews
│
└── Screenshots/                             Renders, belt paths, tensioner motion (GIF + MP4)
```

## Quick links

| I want to... | Go to |
|---|---|
| Buy the hardware | [BOM.md](BOM.md) |
| Print the parts | [Base Components/Print Ready](Base%20Components/Print%20Ready), or the all-in-one [3MF plate](Base%20Components/Print%20Ready/Printed%20Parts%20All.3mf) |
| Look at the assembly in 3D | [Full assembly STL](For%20Viewing/SV08-P6%20Dual%20Shear%20Live%20Idlers%20Front%20Tensioners.stl) · [Sub-assemblies](Base%20Assemblies/For%20Viewing) |
| See the tensioner move | [Front Left Tensioner Motion.gif](Screenshots/Front%20Left%20Tensioner%20Motion.gif) |
| Browse all screenshots | [Screenshots](Screenshots) |
