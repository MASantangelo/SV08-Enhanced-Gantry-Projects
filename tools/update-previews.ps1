<#
Regenerate everything derived for one gantry variant:
  - STL previews (<folder>\For Viewing\*.stl) for every STEP folder
  - BOM.md from the variant's BOM spreadsheet
  - PNG renders (<variant>\Renders\*.png) of the main assembly and each base assembly

Usage (from the repo root):
  powershell -ExecutionPolicy Bypass -File tools\update-previews.ps1 -Variant "Printed Version" -Title "SV08-P6 Printed Gantry (6 mm)"

Add -SkipStl, -SkipBom or -SkipRenders to leave out a step. Rendering opens a FreeCAD
window for about a minute.
#>
param(
    [Parameter(Mandatory)][string]$Variant,
    [string]$Title = $Variant,
    [string]$FreeCADBin = "C:\Program Files\FreeCAD 1.0\bin",
    [switch]$SkipStl,
    [switch]$SkipBom,
    [switch]$SkipRenders
)
$ErrorActionPreference = "Stop"
$root = Split-Path $PSScriptRoot -Parent
$variantDir = Join-Path $root $Variant
if (-not (Test-Path $variantDir)) { throw "Variant folder not found: $variantDir" }
$freecadcmd = Join-Path $FreeCADBin "freecadcmd.exe"
$python = Join-Path $FreeCADBin "python.exe"

if (-not $SkipStl) {
    $folders = @(
        $variantDir,
        (Join-Path $variantDir "Base Assemblies"),
        (Join-Path $variantDir "Base Components\Print Ready"),
        (Join-Path $variantDir "Base Components\For Mockups Only")
    ) | Where-Object { (Test-Path $_) -and (Get-ChildItem $_ -File -Include *.step, *.stp -Name -Path "$_\*") }

    Remove-Item Env:STEP2STL_ONLY -ErrorAction SilentlyContinue
    foreach ($f in $folders) {
        Write-Host "== $($f.Substring($root.Length + 1))" -ForegroundColor Cyan
        $env:STEP2STL_DIR = $f
        # freecadcmd prints a wall of progress percentages; keep only our result lines
        & $freecadcmd (Join-Path $PSScriptRoot "step2stl.py") | Select-String -Pattern '(OK|FAIL|DONE)\s' | ForEach-Object { $_.Line.Trim() }
    }
}

if (-not $SkipBom) {
    $xlsx = Get-ChildItem $variantDir -File -Filter *BOM*.xlsx | Where-Object { $_.Name -notlike '~$*' }
    if ($xlsx.Count -eq 1) {
        Write-Host "== BOM.md from $($xlsx.Name)" -ForegroundColor Cyan
        & $python -I (Join-Path $PSScriptRoot "make_bom_md.py") $variantDir $xlsx.Name $Title
    } elseif ($xlsx.Count -gt 1) {
        Write-Warning "Several BOM spreadsheets in $Variant; skipping BOM.md: $($xlsx.Name -join ', ')"
    } else {
        Write-Host "No *BOM*.xlsx in $Variant; skipping BOM.md"
    }
}

if (-not $SkipRenders) {
    if (Get-ChildItem $variantDir -File -Filter *.step) {
        Write-Host "== Renders" -ForegroundColor Cyan
        & (Join-Path $PSScriptRoot "render.ps1") -Variant $Variant -FreeCADBin $FreeCADBin
    } else {
        Write-Host "No main assembly STEP in $Variant; skipping renders"
    }
}
