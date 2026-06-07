param(
    [ValidateSet("2024", "2025", "2026", "2027")]
    [string]$Version = "2027",

    [string]$Configuration = "Debug",

    [string]$OutputPath = ""
)

$ErrorActionPreference = "Stop"

$repoRoot = Split-Path -Parent $PSScriptRoot

$supportedTracks = @{
    "2027" = @{
        Project = "src\YangAgent.Revit2027\YangAgent.Revit2027.csproj"
        TargetFramework = "net10.0-windows"
        Status = "implemented"
    }
}

$plannedTracks = @{
    "2024" = ".NET Framework 4.8 track planned; project not created yet."
    "2025" = ".NET 8 track planned; project not created yet."
    "2026" = ".NET 8 track expected; verify SDK/API before creating project."
}

function Test-FileLocked {
    param(
        [Parameter(Mandatory = $true)]
        [string]$Path
    )

    if (-not (Test-Path -LiteralPath $Path)) {
        return $false
    }

    $stream = $null
    try {
        $stream = [System.IO.File]::Open(
            $Path,
            [System.IO.FileMode]::Open,
            [System.IO.FileAccess]::ReadWrite,
            [System.IO.FileShare]::None
        )
        return $false
    }
    catch [System.IO.IOException] {
        return $true
    }
    finally {
        if ($null -ne $stream) {
            $stream.Dispose()
        }
    }
}

function Assert-DllNotLocked {
    param(
        [Parameter(Mandatory = $true)]
        [string]$Path,

        [Parameter(Mandatory = $true)]
        [string]$Version
    )

    if (-not (Test-FileLocked -Path $Path)) {
        return
    }

    $revitProcesses = Get-Process -Name Revit -ErrorAction SilentlyContinue
    $processText = ""
    if ($revitProcesses) {
        $processText = " Locked by Revit process id(s): " + (($revitProcesses | ForEach-Object { $_.Id }) -join ",") + "."
    }

    throw "YA-CS-BUILD-LOCKED-DLL: DLL is locked and cannot be overwritten: $Path.$processText Close Revit $Version, then run this script again."
}

if (-not $supportedTracks.ContainsKey($Version)) {
    $reason = $plannedTracks[$Version]
    if (-not $reason) {
        $reason = "No build track is configured."
    }
    throw "YA-CS-VERSION-PLANNED: Revit $Version DLL build is planned but not implemented. $reason"
}

$track = $supportedTracks[$Version]
$project = Join-Path $repoRoot $track.Project

if (-not (Test-Path -LiteralPath $project)) {
    throw "YA-CS-PROJECT-MISSING: Project not found: $project"
}

$dll = Join-Path (Split-Path -Parent $project) "bin\$Configuration\$($track.TargetFramework)\YangAgent.Revit$Version.dll"

if ([string]::IsNullOrWhiteSpace($OutputPath)) {
    Assert-DllNotLocked -Path $dll -Version $Version
    dotnet build $project -c $Configuration
}
else {
    dotnet build $project -c $Configuration -o $OutputPath
}

if ($LASTEXITCODE -ne 0) {
    throw "dotnet build failed with exit code $LASTEXITCODE"
}
