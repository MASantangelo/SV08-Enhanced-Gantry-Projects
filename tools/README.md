# tools

Scripts that generate the viewable files in this repo. You only need them if you're maintaining the repo; they're not needed to build the printer.

**Requirement:** [FreeCAD 1.0](https://www.freecad.org/) installed at the default location. The scripts run on FreeCAD's own Python, so nothing else needs installing.

## Refresh a variant

From the repo root:

```powershell
powershell -ExecutionPolicy Bypass -File tools\update-previews.ps1 -Variant "Printed Version" -Title "SV08-P6 Printed Gantry (6 mm)"
```

The titles in use are `SV08-P6 Printed Gantry (6 mm)`, `SV08-CF6 Carbon Fiber Gantry (6 mm)` and `SV08-M5 Aluminum Gantry (5 mm)`.

This:

1. Converts every STEP file into `For Viewing\<name>.stl`, in each of these folders that exists: the variant folder itself, `Base Assemblies`, `Base Components\Print Ready` and `Base Components\For Mockups Only`.
2. Rebuilds `<variant>\BOM.md` from the variant's `*BOM*.xlsx` file.

Add `-SkipStl` or `-SkipBom` to run only one of the two steps. Close the spreadsheet in Excel first, because Excel blocks other programs from reading it.

The output is deterministic: if a STEP file hasn't changed, its STL comes out byte-for-byte identical, so git only shows files that actually changed.

## Renders

`update-previews.ps1` also renders PNGs into `<variant>\Renders\`. You can run that step on its own:

```powershell
powershell -ExecutionPolicy Bypass -File tools\render.ps1 -Variant "Printed Version"
```

- **What it renders:** the main assembly from 4 angles (front left, front right, rear left, overview), plus each `Base Assemblies` STEP from its outside corner. The CAD colours are kept, shaded without edge lines.
- **How:** it uses FreeCAD's full interface, so a FreeCAD window opens for about a minute and then closes itself. Images are rendered at 2× size, cropped to the parts and scaled down.
- **Changing angles:** edit `$MainViews` and `$AssemblyViews` in `render.ps1`. An angle is an azimuth (0 = front, 45 = front right, 315 = front left) and an elevation in degrees above the horizon. Avoid 90 (straight down), because the light washes out faces seen head-on.
- **No noise in git:** a render is only rewritten when its pixels change, so an unchanged model leaves the files byte-identical. FreeCAD's embedded metadata, which includes a timestamp and the local file path, is stripped out.
- **Not covered:** motion. Animations like the tensioner GIF still come from Fusion.
- **Landing image:** after rendering, `landing_composite.py` combines each version's `Full Gantry - Front Right` render into `Renders/Landing - Front Right.png`. With three versions it's a "Y" split from the centre (seams to the top-left corner, the top-right corner and the bottom middle): printed on the left, metal at the top, CF on the right, each with a label. Edit `REGIONS` in the script to change the order or labels.

## Check flat plates (CF, metal)

```powershell
powershell -ExecutionPolicy Bypass -File tools\plate-check.ps1 -Variant "Metal Version" -Reference "CF Version"
```

This runs two checks on each plate in `<variant>\Base Components`: `plate_check.py` (holes, fits and walls between features), then `wall_check.py` (a direct wall sweep, below). Add `-SkipWallSweep` to run only the first.

`plate_check.py` checks:

- **Thickness:** must match the number in the file name (`Metal5mm` → 5.00 mm).
- **Position:** the plate must sit on 0,0,0.
- **Holes by role:** M2 and M3 tap drills (1.6 and 2.5), close-fit clearance holes (3.2, 4.3, 5.3) and Ø5.00 locating fits. A hole that's close to one of these sizes but not on it is flagged as a near-miss. Inside corner radii of the outline aren't counted as holes.
- **Metal only:** every plate except spacers needs at least one tapped hole.
- **Minimum wall:** the thinnest strip of material between two features, or between a feature and the edge, at every depth. Anything under 1.5 mm is flagged (change it with `-MinWall`). Each one is labelled as a through-wall (full plate depth) or a lip (a rim around a pocket).
- **With `-Reference`:** each hole is matched by position to the same plate in the reference version. It flags precision fits that changed (Ø5.00 shoulder holes, Ø13.00 bearing bores, Ø22.00 motor boss) and holes that exist on only one of the two plates. Intentional changes like PEM → tap are only counted. Add `-ListAllChanges` to list them.

`wall_check.py` measures material directly on the solid, so it also catches walls `plate_check.py` can't see: material between pockets that merge into one opening, such as knife-edge tips and thin tongues where a bearing step overlaps a motor-boss recess.

- **In-plane walls:** each plate is sectioned at every distinct depth (and every 0.1 mm through countersinks and chamfers). Anywhere two boundary edges come closer than the minimum across solid material, it reports a `THIN WALL` at the thinnest point, with the depth of that section.
- **Floors:** every pocket floor or ceiling is checked against the opposite face (`THIN FLOOR`).
- It uses the same `-MinWall` and `-Only` options and the same `plate_accepted.json` (kinds `wall` and `floor`).

**Printed parts:** the sweep can also check that walls and heights suit your slicer settings. Use `-SweepOnly`, because the hole sizes `plate_check.py` expects don't apply to print-tolerance holes, and point `-Folder` at the print-ready parts:

```powershell
powershell -ExecutionPolicy Bypass -File tools\plate-check.ps1 -Variant "Printed Version" -Folder "Base Components\Print Ready" -SweepOnly -MinWall 2.0 -PreferredWall 3.0 -InsertHole 4.7 -LayerHeight 0.2
powershell -ExecutionPolicy Bypass -File tools\plate-check.ps1 -Variant "Shared Components" -Folder "Print Ready" -SweepOnly -MinWall 2.0 -PreferredWall 3.0 -InsertHole 4.7 -LayerHeight 0.2
```

These are the project's printed rules: 2.0 mm minimum and 3.0 mm preferred. 3 mm of printed plastic is enough for most loads in this motion system, and the shared outline can reach it in most places.

- **`-PreferredWall`**: a second tier. Walls from `-MinWall` up to this are `BELOW-PREFERRED WALL`s. They're listed for review like thin walls, so you either fix them or accept them.
- **`-InsertHole`** (heat-set insert hole diameters, comma-separated, e.g. `4.7`): any wall touching one of these holes and thinner than the preferred wall (or `-MinWall`, without one) is an `INSERT WALL`. Heat-setting pushes melted plastic outward, so a thin wall beside an insert bulges into the next hole or cracks.
- **`-LayerHeight`** (e.g. `0.2`, `0.15`): the thickness and every flat level (pocket floors, steps) must sit on a layer boundary, otherwise it's an `OFF-LAYER HEIGHT`. In this mode the file's own Z is the build direction, since print-ready files are already oriented for printing.
- **`-WallMultiple`** (your line width, e.g. `0.4`), optional: every wall up to `-WallMax` (default 4 mm) must be an exact multiple of it, otherwise it's an `OFF-GRID WALL` with the two nearest multiples. The project doesn't use this rule, because the shared outline can't keep every wall on the grid.
- Accepted entries use the kinds `preferred`, `insert`, `grid` and `layer`.

Use `-Only "Front Left Top"` to check a single plate. Plates with findings get a marked-up drawing in `%TEMP%\sv08-plate-check`.

**Accepting a finding on purpose:** add an entry to `plate_accepted.json`, giving the plate, the kind (`wall`, `floor`, `near-miss` or `fit`), x/y and the measured value, plus a note. A matching finding then prints as `~ accepted` and doesn't count against the plate. If the geometry changes, it's reported as a normal finding again: that means a move of more than 1 mm, or a value change of more than 0.05 mm.

## Check the BOM against the STEP file

Run this before committing a new assembly STEP. It reads every part and how many times it's used from the STEP file, then compares those counts with the spreadsheet.

```powershell
& "C:\Program Files\FreeCAD 1.0\bin\python.exe" tools\step_bom.py check "Printed Version"
```

- **check**: reports quantity differences, parts in the CAD that aren't in the BOM, and BOM rows that are no longer in the CAD. It also fails on duplicate components (see `dupes`). It ends with `CHECK PASSED` (exit code 0) or `CHECK FAILED` (exit code 1), and never writes anything.
- **dupes**: checks the main STEP and every `Base Assemblies` STEP for duplicate components. When a component is copied and pasted instead of inserted as another instance, Fusion names the copy `Name (1)`, `Name (2)` and so on. The BOM still counts them correctly, but each copy is a separate component to keep in sync, so the check names each one and its parent so you can replace it with an instance of the original. Copies inside the stock Sovol `SV08 … Z Carriage` models are listed but don't fail the check.
- **update**: writes the CAD quantities into the spreadsheet's Qty column, then rebuilds `BOM.md`. Links, notes and formatting are left alone. New CAD parts are only reported unless you add `--add-new`, which appends them under a "New from CAD (sort these)" section. Close the spreadsheet in Excel first.
- **tree**: prints the assembly structure, showing each sub-assembly once. It's useful when writing rules.

Needs openpyxl in FreeCAD's Python. This is a one-time install: `& "C:\Program Files\FreeCAD 1.0\bin\python.exe" -m pip install --user openpyxl`

### Rules (`bom_rules.json`)

CAD names don't always match BOM names, so `bom_rules.json` translates them. Fusion's copy and mirror suffixes (`(2)`, `(Mirror)`, `_1`, `.f3d`, ` x2`) are removed automatically first.

| Rule | What it does | Example |
|---|---|---|
| `exclude_assemblies` | Skips a sub-assembly and everything inside it | The stock SV08 Z carriages |
| `unit_assemblies` | Counts a sub-assembly as one BOM item. Add `"descend": true` to also count the parts inside it. | A D2F-L switch is 1 item, not 5 pieces |
| `category_by_assembly` | Puts parts under a sub-assembly into a specific BOM category | Xol hardware goes into "Xol Toolhead Hardware" |
| `rename` | Maps an exact CAD name to a BOM name | `T-Nut M4` becomes `M4 T-Nut` |
| `rename_patterns` | Regex renames, used when no exact rename matches | `M3x8mm SHCS` becomes `M3 x 8mm SHCS` |
| `ignore_parts` | CAD parts that never belong in the BOM | |
| `bom_only` | BOM rows that are expected to be missing from the CAD | |

`common` rules apply to every variant. Rules under `variants` → `"<folder name>"` add to them for one variant.

## Files

| File | What it does |
|---|---|
| `update-previews.ps1` | Runs both steps for one variant |
| `step2stl.py` | STEP to STL using size-based meshing: small hardware coarse, plates and large parts fine. This keeps full assemblies small enough for GitHub's viewer. |
| `make_bom_md.py` | Spreadsheet to `BOM.md`: sectioned tables, Amazon/AliExpress/Mouser/McMaster buy links, and printed parts and plates linked to their STL previews |
| `render.ps1` / `render.py` | Renders PNGs of the assemblies using FreeCAD's full interface |
| `landing_composite.py` | Builds the split landing-page image from each version's render |
| `plate-check.ps1` / `plate_check.py` | Sanity-checks flat plates: thickness, holes, thin walls, changes from a reference version |
| `wall_check.py` | Direct minimum-wall and floor sweep of flat plates, including merged pockets (run by `plate-check.ps1`) |
| `plate_accepted.json` | Findings accepted on purpose, shared by both plate checks |
| `step_bom.py` | Checks or updates the BOM spreadsheet against the assembly STEP |
| `bom_rules.json` | Rules that translate CAD names into BOM lines |
| `read_xlsx.py` | Minimal `.xlsx` reader using only the Python standard library, used by `make_bom_md.py` |

## Spreadsheet layout `make_bom_md.py` expects

- Header row: `Category | Qty Needed | Description | Purchase Link | Notes`
- Section rows: only the first column filled in, for example `Fasteners - Screws`
- Rows in a section called `Printed Parts`, or one ending in `Plates` (`CF Plates`, `Metal Plates`), are linked to the STL preview with the matching name in the variant's `Base Components` or in `Shared Components`. A leading `4x` and a trailing `- For Printing` are ignored when matching.
