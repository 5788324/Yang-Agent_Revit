# DLL Add-in Development Plan

> Historical reference only.
>
> The active mainline remains pyRevit sandbox usefulness. The C# DLL is a small Revit 2027 support track, not the primary delivery path.

## Current Override

Use these as current authority instead:

1. `docs/revit-version-support-plan.md`
2. `docs/simple-roadmap.md`
3. `docs/next-steps.md`
4. current relevant worklog

## Current DLL Position

- implemented track: `Revit 2027`
- `Revit 2024/2025/2026`: planned only
- DLL scope: ribbon, settings/report entry points, lightweight commands
- no broad DLL migration before a real personal-work need exists

## What Still Matters From This File

- separate version tracks are safer than pretending one DLL fits all Revit versions
- model-changing features should not move into DLL first just because DLL feels more formal
- build/install scripts must fail clearly when a version is only planned

## Use This File Only For

- historical migration ideas;
- old DLL scope reasoning;
- comparing earlier plans against current narrower execution.
