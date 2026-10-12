# tools

Scripts that generate the viewable files in this repo. You only need them if you're maintaining the repo; they're not needed to build the printer.

**Requirement:** [FreeCAD 1.0](https://www.freecad.org/) installed at the default location. The scripts run on FreeCAD's own Python, so nothing else needs installing.

## Refresh a variant

From the repo root:

```powershell
powershell -ExecutionPolicy Bypass -File tools\update-previews.ps1 -Variant "Printed Version" -Title "SV08-P6 Printed Gantry (6 mm)"
```

This:

1. Converts every STEP file into `For Viewing\<name>.stl`, in each of these folders that exists: the variant folder itself, `Base Assemblies`, `Base Components\Print Ready` and `Base Components\For Mockups Only`.
2. Rebuilds `<variant>\BOM.md` from the variant's `*BOM*.xlsx` file.

Add `-SkipStl` or `-SkipBom` to run only one of the two steps. Close the spreadsheet in Excel first, because Excel blocks other programs from reading it.

The output is deterministic: if a STEP file hasn't changed, its STL comes out byte-for-byte identical, so git only shows files that actually changed.

## Files

| File | What it does |
|---|---|
| `update-previews.ps1` | Runs both steps for one variant |
| `step2stl.py` | STEP to STL using size-based meshing: small hardware coarse, plates and large parts fine. This keeps full assemblies small enough for GitHub's viewer. |
| `make_bom_md.py` | Spreadsheet to `BOM.md`: sectioned tables, Amazon/AliExpress buy links, and printed parts linked to their STL previews |
| `read_xlsx.py` | Minimal `.xlsx` reader using only the Python standard library, used by `make_bom_md.py` |

## Spreadsheet layout `make_bom_md.py` expects

- Header row: `Category | Qty Needed | Description | Purchase Link | Notes`
- Section rows: only the first column filled in, for example `Fasteners - Screws`
- Rows in a section called `Printed Parts` are linked to the STL in `Base Components\Print Ready\For Viewing` with the matching name. A leading `4x` and a trailing `- For Printing` are ignored when matching.
