<#
Sanity-check a variant's flat plates (see tools\plate_check.py for what it checks).

Usage (from the repo root):
  powershell -ExecutionPolicy Bypass -File tools\plate-check.ps1 -Variant "Metal Version" -Reference "CF Version"
  powershell -ExecutionPolicy Bypass -File tools\plate-check.ps1 -Variant "Metal Version" -Reference "CF Version" -Only "Front Left Top"

Marked-up drawings of plates with findings go to %TEMP%\sv08-plate-check (not into the repo).
#>
param(
    [Parameter(Mandatory)][string]$Variant,
    [string]$Reference = "",
    [string]$Only = "",
    [double]$MinWall = 1.5,
    [switch]$ListAllChanges,
    [string]$FreeCADBin = "C:\Program Files\FreeCAD 1.0\bin"
)
$ErrorActionPreference = "Stop"
$env:PLATE_VARIANT = $Variant
$env:PLATE_REF = $Reference
$env:PLATE_ONLY = $Only
$env:PLATE_MIN_WALL = "$MinWall"
$env:PLATE_VERBOSE = $(if ($ListAllChanges) { "1" } else { "" })
$env:PLATE_OUT = Join-Path ([IO.Path]::GetTempPath()) "sv08-plate-check"
# freecadcmd prints its banner and progress noise; keep our report lines only
& (Join-Path $FreeCADBin "freecadcmd.exe") (Join-Path $PSScriptRoot "plate_check.py") 2>&1 |
    Where-Object { $_ -match '^(Checking|!|\s*$|==|   |PLATE CHECK|Traceback|\w+Error|Exception)' } | ForEach-Object { "$_" }
