# SV08-P6 Printed Gantry (6 mm)

The printed-plate variant: every gantry plate is 3D printed at 6 mm.

> [!NOTE]
> **This is the v2 printed design:** the plates, sub-assemblies, full gantry assembly, BOM, 3MF and renders. The original v1 files are in the [Printed v1 release](https://github.com/MASantangelo/SV08-Enhanced-Gantry-Projects/releases/tag/printed-v1).

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
│   └── Print Ready/                         ← Print these (plus ../Shared Components/Print Ready)
│       ├── *.step                           Printed plates, holes enlarged ~0.3 mm for printing
│       ├── Printed Parts All.3mf            Every printed part, shared ones included, on one plate (OrcaSlicer)
│       └── For Viewing/                     STL previews
│
├── Photos/                                  Photos of real builds
├── Renders/                                 Auto-generated from the STEP files (always current)
└── Screenshots/                             Fusion screenshots, belt paths, tensioner motion (GIF + MP4)
```

## Quick links

| I want to... | Go to |
|---|---|
| Buy the hardware | [BOM.md](BOM.md) |
| Install it | [Installation guide](../Docs/Installation.md) |
| Print the parts | The plates in [Base Components/Print Ready](Base%20Components/Print%20Ready) and the spacers and levers in [Shared Components/Print Ready](../Shared%20Components/Print%20Ready). Or print everything from the all-in-one [3MF plate](Base%20Components/Print%20Ready/Printed%20Parts%20All.3mf). |
| Look at the assembly in 3D | [Full assembly STL](For%20Viewing/SV08-P6%20Dual%20Shear%20Live%20Idlers%20Front%20Tensioners.stl) · [Sub-assemblies](Base%20Assemblies/For%20Viewing) |
| See the tensioner move | [Front Left Tensioner Motion.gif](Screenshots/Front%20Left%20Tensioner%20Motion.gif) |
| Browse all screenshots | [Screenshots](Screenshots) |

The print-ready plates have their holes enlarged by about 0.3 mm to allow for printing tolerances. The same files are used in the assemblies, so what you see in the CAD is exactly what you print.

## Build photos

The first v2 test build, printed with no supports.

**Fully assembled on an SV08**

![The full v2 printed gantry installed on an SV08, seen from above: all four motor corners, both XY joints and the orange tensioner lever arms at the front](Photos/Full%20Gantry%20v2%20-%20Top.jpg)

| Front left corner and XY joint | XY joint (left) |
|---|---|
| ![The front left motor corner with its orange tensioner lever, the left XY joint and the back left corner of the v2 printed gantry](Photos/Full%20Gantry%20v2%20-%20Front%20Left.jpg) | ![Close-up of the left XY joint v2: the live idler pulley on its shaft between the top and bottom bearing plates, with both belts running past](Photos/XY%20Joint%20Left%20v2%20-%20Angle.jpg) |

**Front left motor assembly** (before the motors were fitted)

| Side | Top | Angle |
|---|---|---|
| ![Front left motor assembly v2, side view showing the bearing stacks and motor pulley between the plates](Photos/Front%20Left%20Motor%20Assembly%20v2%20-%20Side.jpg) | ![Front left motor assembly v2 from the motor side, with the tensioner lever](Photos/Front%20Left%20Motor%20Assembly%20v2%20-%20Top.jpg) | ![Front left motor assembly v2 at an angle, showing the tensioner lever arm and idler](Photos/Front%20Left%20Motor%20Assembly%20v2%20-%20Angle.jpg) |

**Back left motor assembly** (here with printed motor standoffs and the printed back spacer plate, in orange)

| Side | End |
|---|---|
| ![Back left motor assembly v2 from the side, showing the standoffs and the bearing stack between the plates](Photos/Back%20Left%20Motor%20Assembly%20v2%20-%20Side.jpg) | ![Back left motor assembly v2 from the end, showing the bearing stack and the orange back spacer plate](Photos/Back%20Left%20Motor%20Assembly%20v2%20-%20End.jpg) |

## Installing the heat-set inserts

The M3 heat-set inserts go in from the bed side of each plate. Several sit close to a bearing bore, so take them one at a time:

1. **Press the bearings in first.** With the bearing already seated, it backs up the thin wall between the insert and the bore, so the softened plastic can't bulge into the bore.
2. **Start the insert straight with a screw.** Thread an M3 screw into the insert from the other side of the plate, through the screw hole, and pull the insert's leading edge into its seat. That lines it up before you heat it, so it goes in square. Don't skip this: an insert that goes in crooked will cross-thread its screw, and a screw stuck in a crooked insert usually can't be removed without ruining the plate.
3. **No bearing in that seat yet? Push the plastic back.** Without a bearing to back it up, the wall flexes inward as the insert goes in. While it's still warm, push it back into place with a spudger so the bore stays round.
4. **Set it flush or slightly deep, never proud.** It's fine for the insert to sink a little below the surface, but one left sticking out holds the next part off the plate, so the joint won't sit flat or clamp properly.
5. **Trim any plastic pushed up around the insert.** Pay attention to the screw path and the edges. A raised lip looks untidy, and plastic in the screw path can make the screw cross-thread.
6. **Chase the threads before assembly, from the opposite side.** Once the insert has cooled, run an M3 screw through it from the side the real screw *doesn't* come in from, all the way through. That pushes any melted plastic out of the side where the assembly screw enters. Going in from the screw's side would just push the plastic deeper into the threads.

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
