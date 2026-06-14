# Architecture Design

> Historical reference only.
>
> This repository no longer uses this file as an active architecture contract.

## Current Override

Follow these files first:

1. `README.md`
2. `docs/product-brief.md`
3. `docs/project-rules.md`
4. `docs/framework/daily-ops-routine.md`
5. `docs/next-steps.md`

## Why This File Was Downgraded

This file came from an earlier architecture-first phase with broader platform assumptions, including:

- larger MCP and bridge planning;
- heavier multi-layer architecture wording;
- a more company/platform-oriented framing.

The current project is intentionally narrower:

- personal Revit assistant first;
- pyRevit MVP first;
- sandbox validation first;
- controlled preview/apply workflow first.

## What Still Remains True

- pyRevit is the fastest iteration layer.
- C# DLL should stay small until there is a concrete need.
- MCP should not be allowed to execute arbitrary code or uncontrolled model writes.
- Model-changing tools must keep preview, confirmation, log, and Undo checks.

## How To Use This File Now

Use it only for:

- idea mining;
- old architecture vocabulary lookup;
- historical context when reading older planning material.

Do not use it to define current implementation scope.
