<#
Render a variant's main assembly (4 views) and each Base Assemblies STEP (1 view) to
<variant>\Renders\*.png, using FreeCAD's GUI. A FreeCAD window opens briefly and closes itself.

Usage (from the repo root):
  powershell -ExecutionPolicy Bypass -File tools\render.ps1 -Variant "Printed Version"

Edit $MainViews / $AssemblyViews below to change camera angles (see tools\render.py).
#>
param(
    [Parameter(Mandatory)][string]$Variant,
    [string]$FreeCADBin = "C:\Program Files\FreeCAD 1.0\bin",
    [int]$Width = 1600
)
$ErrorActionPreference = "Stop"
$root = Split-Path $PSScriptRoot -Parent
$variantDir = Join-Path $root $Variant
$outDir = Join-Path $variantDir "Renders"

$MainViews = @(
    @{ name = "Front Left";  azimuth = 315; elevation = 30 },
    @{ name = "Front Right"; azimuth = 45;  elevation = 30 },
    @{ name = "Rear Left";   azimuth = 225; elevation = 30 },
    @{ name = "Overview";    azimuth = 0;   elevation = 60 }
)
$AssemblyViews = @( @{ name = "Iso"; azimuth = "outside"; elevation = 30 } )
# Fixed angles for sub-assemblies whose file position doesn't give a consistent "outside" view.
# Mirror pairs get mirror views (45 = front right, 315 = front left). Matched on file-name substring.
$AzimuthOverrides = [ordered]@{ "XY Joint Left" = 315; "XY Joint Right" = 45 }

$jobs = @()
$main = @(Get-ChildItem $variantDir -File -Filter *.step)
if ($main.Count -gt 1) { throw "Expected at most one main .step in $Variant, found $($main.Count)" }
if ($main.Count -eq 1) {
    $jobs += @{ name = "Full Gantry"; step = $main[0].FullName; out_dir = $outDir; views = $MainViews }
} else {
    Write-Host "No main assembly STEP in $Variant yet; rendering sub-assemblies only."
}
Get-ChildItem (Join-Path $variantDir "Base Assemblies") -File -Filter *.step -ErrorAction SilentlyContinue | ForEach-Object {
    $file = $_
    $views = $AssemblyViews
    foreach ($key in $AzimuthOverrides.Keys) {
        if ($file.BaseName -like "*$key*") {
            $views = @( @{ name = "Iso"; azimuth = $AzimuthOverrides[$key]; elevation = 30 } )
            break
        }
    }
    $jobs += @{ name = $file.BaseName; step = $file.FullName; out_dir = $outDir; views = $views }
}

if ($jobs.Count -eq 0) { Write-Host "Nothing to render in $Variant."; return }

$tmp = Join-Path ([IO.Path]::GetTempPath()) "sv08-render"
New-Item -ItemType Directory -Force $tmp | Out-Null
$config = Join-Path $tmp "render.json"
$log = Join-Path $tmp "render.log"
@{ width = $Width; margin = 0.04; jobs = $jobs } | ConvertTo-Json -Depth 6 | Set-Content -Path $config -Encoding utf8
Set-Content -Path $log -Value "" -Encoding utf8

$env:RENDER_CONFIG = $config
$env:RENDER_LOG = $log
Write-Host "Rendering $($jobs.Count) STEP file(s) to $($outDir.Substring($root.Length + 1)) ..."
$p = Start-Process (Join-Path $FreeCADBin "FreeCAD.exe") -ArgumentList "`"$(Join-Path $PSScriptRoot 'render.py')`"" -PassThru
if (-not $p.WaitForExit(900000)) { $p.Kill(); throw "FreeCAD did not finish within 15 minutes" }
Get-Content $log | Where-Object { $_ }
if (Select-String -Path $log -Pattern '^ERROR' -Quiet) { throw "Rendering failed; see the log above" }

# Landing-page image: every variant's Front Right render, split on the diagonal
& (Join-Path $FreeCADBin "python.exe") (Join-Path $PSScriptRoot "landing_composite.py")
