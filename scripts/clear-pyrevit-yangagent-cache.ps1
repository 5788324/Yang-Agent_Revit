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
    "*YangAgent*.cs",
    "*YangAgent*.pickle",
    "*yangagent*.dll",
    "*yangagent*.addin",
    "*yangagent*.cs",
    "*yangagent*.pickle"
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
                $path = $_.FullName
                Write-Host "Removing: $path"
                try {
                    Remove-Item -LiteralPath $path -Force -ErrorAction Stop
                    if (-not (Test-Path -LiteralPath $path)) {
                        $script:removed += 1
                    }
                    else {
                        Write-Warning "Could not remove cache file, it still exists: $path"
                    }
                }
                catch {
                    Write-Warning "Could not remove cache file. Close Revit and try again: $path"
                }
            }
    }
}

Write-Host "Removed $removed cached YangAgent file(s)."
Write-Host "Restart Revit, then run pyRevit Reload if needed."
