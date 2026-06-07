# Revit Version Support Plan

This file records the YangAgent Revit version strategy so future AI agents do not confuse planned support with verified support.

## Current Decision

- First phase: Revit 2024-2027.
- Existing C# DLL skeleton: Revit 2027.
- Revit 2011-2023: deferred backlog only.
- pyRevit remains the main MVP layer; DLL remains a lightweight official entry point.

## Why Not 2011-2027 Now

Revit version support is not only an API naming issue. It also involves .NET runtime changes, SDK references, addin manifests, installer paths, and pyRevit compatibility.

This is a personal-use project, so the short path is to make recent versions useful first and avoid turning the repository into a large multi-version platform too early.

## DLL Track Plan

| Revit version | Runtime direction | Current status | Notes |
| --- | --- | --- | --- |
| 2024 | .NET Framework 4.8 | Planned | Record now, implement later |
| 2025 | .NET 8 | Planned | Verify local SDK/API before implementation |
| 2026 | .NET 8 expected | Planned | Must verify before implementation |
| 2027 | .NET 10 | Skeleton exists | Keep ribbon and folder entry points only |

Current script behavior:

- `scripts\build-revit-addin.ps1 -Version 2027` builds the current DLL skeleton.
- `scripts\install-revit-addin.ps1 -Version 2027` installs the current DLL skeleton manifest.
- `2024`, `2025`, and `2026` are accepted as planned version names, but the scripts stop with `YA-CS-VERSION-PLANNED` until those projects exist.
- `scripts\build-revit2027-addin.ps1` and `scripts\install-revit2027-addin.ps1` remain as beginner-friendly wrappers for Revit 2027.

## 2011-2023 Backlog

Revit 2011-2023 are backlog targets:

- Do not describe them as currently supported.
- Do not ask Hermes to implement compatibility code for them.
- Do not add DLL projects for them until the user provides a real installed version and a concrete testing need.
- Keep notes only, then revisit after the personal MVP is stable.

## Implementation Rules

- Keep pyRevit scripts conservative and compatible with the current pyRevit runtime.
- Do not create a single C# binary for all Revit versions.
- Use one C# project and one `.addin` template per supported Revit runtime track.
- Extract shared business logic only after the MVP proves which code is stable.
- Any version not manually tested inside Revit must be marked planned or unverified.

## Documentation Wording Rules

Allowed wording:

- "First phase targets Revit 2024-2027."
- "Revit 2027 DLL skeleton exists and still needs manual Revit button validation."
- "Revit 2011-2023 are deferred compatibility targets."

Forbidden wording:

- Do not write full-range support claims before validation.
- Do not write that all Revit versions are supported.
- Do not write that one Undo is verified unless it was manually tested in a sandbox model.
