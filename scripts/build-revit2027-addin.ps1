$ErrorActionPreference = "Stop"

$repoRoot = Split-Path -Parent $PSScriptRoot
$project = Join-Path $repoRoot "src\YangAgent.Revit2027\YangAgent.Revit2027.csproj"

if (-not (Test-Path -LiteralPath $project)) {
    throw "Project not found: $project"
}

dotnet build $project -c Debug
if ($LASTEXITCODE -ne 0) {
    throw "dotnet build failed with exit code $LASTEXITCODE"
}
