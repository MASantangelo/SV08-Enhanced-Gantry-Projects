<#
Render the build-guide step images for one or more guides (Docs/steps/*.json) with FreeCAD's GUI.
A FreeCAD window opens briefly for each guide and closes itself.

Usage (from the repo root):
  powershell -ExecutionPolicy Bypass -File tools\build-steps.ps1                 # every guide
  powershell -ExecutionPolicy Bypass -File tools\build-steps.ps1 -Only "XY Joint"

The step file format is described at the top of tools\build_steps.py.
#>
param(
    [string]$Only = "",
    [string]$FreeCADBin = "C:\Program Files\FreeCAD 1.0\bin"
)
$ErrorActionPreference = "Stop"
$root = Split-Path $PSScriptRoot -Parent
$files = @(Get-ChildItem (Join-Path $root "Docs\steps") -Filter *.json | Where-Object { -not $Only -or $_.BaseName -like "*$Only*" })
if ($files.Count -eq 0) { Write-Host "No step files found."; return }

$tmp = Join-Path ([IO.Path]::GetTempPath()) "sv08-steps"
New-Item -ItemType Directory -Force $tmp | Out-Null
$log = Join-Path $tmp "steps.log"
$failed = $false
foreach ($f in $files) {
    Set-Content -Path $log -Value "" -Encoding utf8
    $env:STEPS_CONFIG = $f.FullName
    $env:STEPS_LOG = $log
    Write-Host "== $($f.BaseName)" -ForegroundColor Cyan
    $p = Start-Process (Join-Path $FreeCADBin "FreeCAD.exe") -ArgumentList "`"$(Join-Path $PSScriptRoot 'build_steps.py')`"" -PassThru
    if (-not $p.WaitForExit(900000)) { $p.Kill(); throw "FreeCAD did not finish within 15 minutes" }
    Get-Content $log | Where-Object { $_ }
    if (Select-String -Path $log -Pattern '^(ERROR|WARN)' -Quiet) { $failed = $true }
}
if ($failed) { throw "Some steps failed or matched no parts; see the log above" }
