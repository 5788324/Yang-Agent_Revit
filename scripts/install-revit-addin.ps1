param(
    [ValidateSet("2024", "2025", "2026", "2027")]
    [string]$Version = "2027",

    [string]$Configuration = "Debug"
)

$ErrorActionPreference = "Stop"

$repoRoot = Split-Path -Parent $PSScriptRoot

$supportedTracks = @{
    "2027" = @{
        Project = "src\YangAgent.Revit2027\YangAgent.Revit2027.csproj"
        TargetFramework = "net10.0-windows"
        Template = "addins\Revit2027\YangAgent.Revit2027.addin.template"
    }
}

$plannedTracks = @{
    "2024" = ".NET Framework 4.8 track planned; project and addin template not created yet."
    "2025" = ".NET 8 track planned; project and addin template not created yet."
    "2026" = ".NET 8 track expected; verify SDK/API before creating project and addin template."
}

if (-not $supportedTracks.ContainsKey($Version)) {
    $reason = $plannedTracks[$Version]
    if (-not $reason) {
        $reason = "No install track is configured."
    }
    throw "YA-CS-VERSION-PLANNED: Revit $Version DLL install is planned but not implemented. $reason"
}

$track = $supportedTracks[$Version]
$project = Join-Path $repoRoot $track.Project
$template = Join-Path $repoRoot $track.Template
$dll = Join-Path (Split-Path -Parent $project) "bin\$Configuration\$($track.TargetFramework)\YangAgent.Revit$Version.dll"
$addinDir = Join-Path $env:APPDATA "Autodesk\Revit\Addins\$Version"
$addinPath = Join-Path $addinDir "YangAgent.Revit$Version.addin"

if (-not (Test-Path -LiteralPath $template)) {
    throw "YA-CS-ADDIN-TEMPLATE-MISSING: Add-in template not found: $template"
}

& (Join-Path $PSScriptRoot "build-revit-addin.ps1") -Version $Version -Configuration $Configuration

if (-not (Test-Path -LiteralPath $dll)) {
    throw "YA-CS-DLL-MISSING: DLL was not built: $dll"
}

if (-not (Test-Path -LiteralPath $addinDir)) {
    New-Item -ItemType Directory -Path $addinDir | Out-Null
}

$escapedDll = [System.Security.SecurityElement]::Escape($dll)
$content = Get-Content -Raw -Encoding UTF8 $template
$content = $content.Replace("{{ASSEMBLY_PATH}}", $escapedDll)
Set-Content -Path $addinPath -Value $content -Encoding UTF8

Write-Host "Installed YangAgent Revit $Version add-in manifest:"
Write-Host "  $addinPath"
Write-Host ""
Write-Host "Restart Revit $Version to load the DLL add-in."
