# SV08 Enhanced Gantry Projects

AWD conversion for the Sovol SV08 with dual-shear live XY idlers and front belt tensioners.

![Full assembled gantry overview: printed 6 mm version](Printed%20Version/Screenshots/Full%20Assembled%20Gantry%20Overview.png)

The design comes in three gantry variants:

| Variant | Plate material | Plate thickness | Folder | Status |
|---|---|---|---|---|
| Printed gantry | 3D printed | 6 mm | [`Printed Version`](Printed%20Version) | Available |
| CF gantry | Carbon fiber (CFRP) | 6 mm | *coming soon* | In progress |
| Metal gantry | Metal | 5 mm | *coming soon* | In progress |

## Printed Version (6 mm)

![Front left tensioner motion](Printed%20Version/Screenshots/Front%20Left%20Tensioner%20Motion.gif)

- `SV08-P6 Dual Shear Live Idlers Front Tensioners.step`: the full assembly
  - `For Viewing/`: STL copy of the full assembly for previewing on GitHub. It's about 38 MB, so give it a few seconds to load. Small hardware is meshed coarser to keep the size down.
- `SV08_P6_Printed_BOM_from_STEP.xlsx`: bill of materials
- `Base Assemblies/`: each corner motor assembly and XY joint as its own STEP file
  - `For Viewing/`: STL copies for previewing on GitHub
- `Base Components/Print Ready/`: parts already oriented for printing. Quantities are in the file names (for example `4x Z Carriage Spacer`).
  - `Printed Parts All.3mf`: every print-ready part laid out on one plate, ready to open in your slicer (made in Creality Print)
  - `For Viewing/`: STL copies of the print-ready STEP files, so you can preview them in 3D right on GitHub. The STEP files are the source of truth.
- `Base Components/For Mockups Only/`: plates in their assembled orientation, for reference and mockups. **Do not print these.**
  - `For Viewing/`: STL copies of the mockup STEP files, so you can preview them in 3D right on GitHub.
- [`Screenshots/`](Printed%20Version/Screenshots): renders of the assemblies and belt paths, plus an [MP4 of the tensioner motion](Printed%20Version/Screenshots/Front%20Left%20Tensioner%20Motion.mp4)

## License

[CC BY-NC-SA 4.0](LICENSE): you can share and remix with credit, but not for commercial use, and derivatives must use the same license.
