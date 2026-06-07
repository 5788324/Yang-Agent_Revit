$ErrorActionPreference = "Stop"

$repoRoot = Split-Path -Parent $PSScriptRoot
$project = Join-Path $repoRoot "src\YangAgent.Revit2027\YangAgent.Revit2027.csproj"
$template = Join-Path $repoRoot "addins\Revit2027\YangAgent.Revit2027.addin.template"
$dll = Join-Path $repoRoot "src\YangAgent.Revit2027\bin\Debug\net10.0-windows\YangAgent.Revit2027.dll"
$addinDir = Join-Path $env:APPDATA "Autodesk\Revit\Addins\2027"
$addinPath = Join-Path $addinDir "YangAgent.Revit2027.addin"

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

if (-not (Test-Path -LiteralPath $template)) {
    throw "Add-in template not found: $template"
}

Assert-DllNotLocked -Path $dll

dotnet build $project -c Debug
if ($LASTEXITCODE -ne 0) {
    throw "dotnet build failed with exit code $LASTEXITCODE"
}

if (-not (Test-Path -LiteralPath $dll)) {
    throw "DLL was not built: $dll"
}

if (-not (Test-Path -LiteralPath $addinDir)) {
    New-Item -ItemType Directory -Path $addinDir | Out-Null
}

$escapedDll = [System.Security.SecurityElement]::Escape($dll)
$content = Get-Content -Raw -Encoding UTF8 $template
$content = $content.Replace("{{ASSEMBLY_PATH}}", $escapedDll)
Set-Content -Path $addinPath -Value $content -Encoding UTF8

Write-Host "Installed YangAgent Revit 2027 add-in manifest:"
Write-Host "  $addinPath"
Write-Host ""
Write-Host "Restart Revit 2027 to load the DLL add-in."
