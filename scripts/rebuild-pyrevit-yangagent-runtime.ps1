$ErrorActionPreference = "Stop"

$repoRoot = Split-Path -Parent $PSScriptRoot
$clearScript = Join-Path $PSScriptRoot "clear-pyrevit-yangagent-cache.ps1"
$runtimeRoot = Join-Path $env:APPDATA "pyRevit\2027"
$runtimeFiles = @(
    (Join-Path $runtimeRoot "YangAgent.cs"),
    (Join-Path $runtimeRoot "pyRevit_2027_6e209f291442d185_YangAgent.dll")
)

if (-not (Test-Path -LiteralPath $clearScript)) {
    throw "Missing cache-clear script: $clearScript"
}

$running = Get-Process -ErrorAction SilentlyContinue |
    Where-Object { $_.ProcessName -in @("Revit", "RevitWorker") }

if ($running) {
    Write-Host "Revit runtime rebuild aborted."
    Write-Host "Close Revit and RevitWorker first, then run this script again."
    $running | Select-Object ProcessName, Id | Format-Table -AutoSize
    exit 1
}

Write-Host "Clearing YangAgent pyRevit runtime cache..."
& $clearScript

$remaining = $runtimeFiles | Where-Object { Test-Path -LiteralPath $_ }

if ($remaining.Count -gt 0) {
    Write-Host "Cache rebuild preparation incomplete. These files still exist:"
    $remaining | ForEach-Object { Write-Host $_ }
    exit 2
}

Write-Host ""
Write-Host "YangAgent pyRevit runtime cache is cleared."
Write-Host "Next steps:"
Write-Host "1. Start Revit 2027."
Write-Host "2. Open the sandbox model."
Write-Host "3. Run pyRevit Reload if the ribbon is already open."
Write-Host "4. Click the YangAgent button again to trigger runtime rebuild."
