$ErrorActionPreference = "Stop"

& (Join-Path $PSScriptRoot "build-revit-addin.ps1") -Version 2027
