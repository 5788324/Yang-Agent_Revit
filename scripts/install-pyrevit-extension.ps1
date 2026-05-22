param(
    [string]$PyRevitExtensionsRoot = "$env:APPDATA\pyRevit\Extensions",
    [switch]$Force,
    [switch]$ClearCache
)

$ErrorActionPreference = "Stop"

$repoRoot = Split-Path -Parent $PSScriptRoot
$source = Join-Path $repoRoot "pyrevit\YangAgent.extension"
$target = Join-Path $PyRevitExtensionsRoot "YangAgent.extension"

if (-not (Get-Command pyrevit -ErrorAction SilentlyContinue)) {
    Write-Warning "pyRevit command was not found in PATH."
    Write-Warning "If the YangAgent tab does not appear in Revit, install pyRevit first and restart Revit."
    Write-Warning "Download: https://github.com/pyrevitlabs/pyRevit/releases"
    Write-Host ""
}

if (-not (Test-Path -LiteralPath $source)) {
    throw "Source extension not found: $source"
}

if (-not (Test-Path -LiteralPath $PyRevitExtensionsRoot)) {
    New-Item -ItemType Directory -Path $PyRevitExtensionsRoot | Out-Null
}

if (Test-Path -LiteralPath $target) {
    if (-not $Force) {
        Write-Host "Existing extension found: $target"
        Write-Host "Run again with -Force to replace the link."
        exit 1
    }

    $resolvedTarget = (Resolve-Path -LiteralPath $target).Path
    $resolvedRoot = (Resolve-Path -LiteralPath $PyRevitExtensionsRoot).Path
    if (-not $resolvedTarget.StartsWith($resolvedRoot, [System.StringComparison]::OrdinalIgnoreCase)) {
        throw "Refusing to remove target outside pyRevit extensions root: $resolvedTarget"
    }

    Remove-Item -LiteralPath $target -Recurse -Force
}

New-Item -ItemType Junction -Path $target -Target $source | Out-Null

if ($ClearCache) {
    & (Join-Path $PSScriptRoot "clear-pyrevit-yangagent-cache.ps1")
}

Write-Host "Installed YangAgent pyRevit extension:"
Write-Host "  Source: $source"
Write-Host "  Target: $target"
Write-Host ""
Write-Host "Restart Revit or reload pyRevit to see the YangAgent tab."
