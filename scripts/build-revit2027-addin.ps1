$ErrorActionPreference = "Stop"

$repoRoot = Split-Path -Parent $PSScriptRoot
$project = Join-Path $repoRoot "src\YangAgent.Revit2027\YangAgent.Revit2027.csproj"
$dll = Join-Path $repoRoot "src\YangAgent.Revit2027\bin\Debug\net10.0-windows\YangAgent.Revit2027.dll"

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
        [string]$Path
    )

    if (-not (Test-FileLocked -Path $Path)) {
        return
    }

    $revitProcesses = Get-Process -Name Revit -ErrorAction SilentlyContinue
    $processText = ""
    if ($revitProcesses) {
        $processText = " Locked by Revit process id(s): " + (($revitProcesses | ForEach-Object { $_.Id }) -join ",") + "."
    }

    throw "YA-CS-BUILD-LOCKED-DLL: DLL is locked and cannot be overwritten: $Path.$processText Close Revit 2027, then run this script again."
}

if (-not (Test-Path -LiteralPath $project)) {
    throw "Project not found: $project"
}

Assert-DllNotLocked -Path $dll

dotnet build $project -c Debug
if ($LASTEXITCODE -ne 0) {
    throw "dotnet build failed with exit code $LASTEXITCODE"
}
