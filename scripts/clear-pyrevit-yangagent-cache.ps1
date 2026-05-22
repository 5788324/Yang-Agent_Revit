$ErrorActionPreference = "Stop"

$candidateRoots = @(
    $env:TEMP,
    (Join-Path $env:LOCALAPPDATA "pyRevit"),
    (Join-Path $env:APPDATA "pyRevit")
)

$roots = $candidateRoots | Where-Object { $_ -and (Test-Path -LiteralPath $_) } | Select-Object -Unique

$patterns = @(
    "*YangAgent*.dll",
    "*YangAgent*.addin",
    "*yangagent*.dll",
    "*yangagent*.addin"
)

Write-Host "Close Revit before clearing the pyRevit cache."
Write-Host "Searching YangAgent pyRevit cache files..."

$removed = 0
foreach ($root in $roots) {
    foreach ($pattern in $patterns) {
        try {
            $matches = Get-ChildItem -LiteralPath $root -Recurse -Force -ErrorAction SilentlyContinue -Filter $pattern
        }
        catch {
            Write-Warning "Skipping cache root: $root"
            continue
        }

        $matches |
            Where-Object { $_.FullName -match "pyRevit" } |
            ForEach-Object {
                Write-Host "Removing: $($_.FullName)"
                Remove-Item -LiteralPath $_.FullName -Force -ErrorAction SilentlyContinue
                $script:removed += 1
            }
    }
}

Write-Host "Removed $removed cached YangAgent file(s)."
Write-Host "Restart Revit, then run pyRevit Reload if needed."
