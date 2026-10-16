<#
Sanity-check a variant's flat plates: holes, fits and walls (tools\plate_check.py), then a
direct wall sweep that also covers merged pockets (tools\wall_check.py).

Usage (from the repo root):
  powershell -ExecutionPolicy Bypass -File tools\plate-check.ps1 -Variant "Metal Version" -Reference "CF Version"
  powershell -ExecutionPolicy Bypass -File tools\plate-check.ps1 -Variant "Metal Version" -Only "Front Left Top"

Printed parts (wall sweep only): 2.0 mm minimum, 3.0 mm preferred, walls beside the 4.7 mm
heat-set insert holes at least the preferred wall, heights in 0.2 mm layers:
  powershell -ExecutionPolicy Bypass -File tools\plate-check.ps1 -Variant "Printed Version" -Folder "Base Components\Print Ready" -SweepOnly -MinWall 2.0 -PreferredWall 3.0 -InsertHole 4.7 -LayerHeight 0.2
  powershell -ExecutionPolicy Bypass -File tools\plate-check.ps1 -Variant "Shared Components" -Folder "Print Ready" -SweepOnly -MinWall 2.0 -PreferredWall 3.0 -InsertHole 4.7 -LayerHeight 0.2
-WallMultiple 0.4 also flags walls off the line-width grid (exact multiples).

-SkipWallSweep runs only plate_check.py; -SweepOnly runs only wall_check.py. Marked-up drawings of
plates with plate_check findings go to %TEMP%\sv08-plate-check (not into the repo).
#>
param(
    [Parameter(Mandatory)][string]$Variant,
    [string]$Reference = "",
    [string]$Only = "",
    [double]$MinWall = 1.5,
    [string]$Folder = "Base Components",   # wall sweep only; plate_check always reads Base Components
    [double]$WallMultiple = 0,             # e.g. 0.4: walls must be multiples of the line width
    [double]$WallMax = 4.0,                # widest wall the multiple rule applies to
    [double]$PreferredWall = 0,            # e.g. 3.0: walls under this (but over -MinWall) are flagged for review
    [string]$InsertHole = "",              # e.g. "4.7": walls beside these holes must reach the preferred wall
    [double]$LayerHeight = 0,              # e.g. 0.2: heights must be multiples of the layer height
    [switch]$ListAllChanges,
    [switch]$SkipWallSweep,
    [switch]$SweepOnly,
    [string]$FreeCADBin = "C:\Program Files\FreeCAD 1.0\bin"
)
$ErrorActionPreference = "Stop"
$inv = [Globalization.CultureInfo]::InvariantCulture
$env:PLATE_VARIANT = $Variant
$env:PLATE_REF = $Reference
$env:PLATE_ONLY = $Only
$env:PLATE_MIN_WALL = $MinWall.ToString($inv)
$env:PLATE_FOLDER = $Folder
$env:PLATE_WALL_MULTIPLE = $(if ($WallMultiple -gt 0) { $WallMultiple.ToString($inv) } else { "" })
$env:PLATE_WALL_MAX = $WallMax.ToString($inv)
$env:PLATE_WALL_PREFERRED = $(if ($PreferredWall -gt 0) { $PreferredWall.ToString($inv) } else { "" })
$env:PLATE_INSERT_HOLE = $InsertHole
$env:PLATE_LAYER_HEIGHT = $(if ($LayerHeight -gt 0) { $LayerHeight.ToString($inv) } else { "" })
$env:PLATE_VERBOSE = $(if ($ListAllChanges) { "1" } else { "" })
$env:PLATE_OUT = Join-Path ([IO.Path]::GetTempPath()) "sv08-plate-check"
$freecadcmd = Join-Path $FreeCADBin "freecadcmd.exe"
# freecadcmd prints its banner and progress noise; keep our report lines only
$keep = '^(Checking|Wall sweep|!|\s*$|==|   |PLATE CHECK|WALL CHECK|Traceback|\w+Error|Exception)'
if (-not $SweepOnly) {
    & $freecadcmd (Join-Path $PSScriptRoot "plate_check.py") 2>&1 | Where-Object { $_ -match $keep } | ForEach-Object { "$_" }
    ""
}
if (-not $SkipWallSweep) {
    & $freecadcmd (Join-Path $PSScriptRoot "wall_check.py") 2>&1 | Where-Object { $_ -match $keep } | ForEach-Object { "$_" }
}
