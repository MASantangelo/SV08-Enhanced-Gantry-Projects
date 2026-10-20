<#
Mechanical analysis of the three gantry versions (see "Mechanical Analysis.md" in the repo root).

Usage (from the repo root):
  powershell -ExecutionPolicy Bypass -File tools\analysis\analysis.ps1
  powershell -ExecutionPolicy Bypass -File tools\analysis\analysis.ps1 -From frame   # rerun from a later step

Steps: geometry (STEP -> plates, corners, XY joint, belt loads), plates (plate FEA), corners (corner joint FEA),
xyjoint (predicted XY joint bench test), frame (gantry-level models), figures (Renders\Analysis\*.png).
Takes about 15 minutes, mostly FEA.
Work files go to %TEMP%\sv08fea, a short path on purpose: CalculiX fails past Windows' 260-character limit.
#>
param(
    [ValidateSet("geometry", "plates", "corners", "xyjoint", "frame", "figures")][string]$From = "geometry",
    [string]$FreeCADBin = "C:\Program Files\FreeCAD 1.0\bin"
)
$ErrorActionPreference = "Stop"
$env:SV08_ANALYSIS_DIR = Join-Path ([IO.Path]::GetTempPath()) "sv08fea"
$env:SV08_FREECAD_BIN = $FreeCADBin
New-Item -ItemType Directory -Force $env:SV08_ANALYSIS_DIR | Out-Null
$python = Join-Path $FreeCADBin "python.exe"
$steps = "geometry", "plates", "corners", "xyjoint", "frame", "figures"
foreach ($step in $steps[$steps.IndexOf($From)..($steps.Count - 1)]) {
    "== $step"
    $script = Join-Path $PSScriptRoot "$step.py"
    if ($step -eq "geometry") {
        # freecadcmd prints its banner and progress noise; keep our report lines only
        & (Join-Path $FreeCADBin "freecadcmd.exe") $script 2>&1 | Where-Object { $_ -match '^(GEOMETRY|Traceback|\w+Error|  )' } | ForEach-Object { "$_" }
    } else {
        & $python $script
    }
    if ($LASTEXITCODE) { throw "$step failed" }
}
