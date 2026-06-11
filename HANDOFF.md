# Handoff SOP (Legacy Reference)

This file is now a legacy handoff reference. It is no longer the top authority for current project direction.

## Current Authority Order

If this file conflicts with newer repo state, follow this order instead:

1. `docs/handoff-new-chat-2026-06-07.md`
2. `docs/next-steps.md`
3. The latest relevant section in `docs/worklogs/worklog-2026-06-07.md`
4. This file and other older documents as historical background only

## Current Direction Override

- The project is currently a personal Revit assistant, not an enterprise platform.
- The mainline target is a usable `pyRevit MVP` in a sandbox model.
- The current implemented C# DLL track is `Revit 2027` only.
- `Revit 2024/2025/2026` are planned only.
- `Revit 2011-2023` are deferred backlog only.
- `Revit 2022` is no longer part of the current first-phase mainline.
- Do not push unless the user explicitly asks.
- Hermes/DeepSeek stays on a separate branch and does docs/read-only support only.

## What This File Is Still Good For

Use this file only for stable repo conventions that still remain true:

- pyRevit folder naming must stay ASCII English.
- Model-changing tools must keep `dry-run -> human confirmation -> apply`.
- Do not commit `.rvt` files, secrets, or local `%APPDATA%` config.
- Use sandbox/test models before any model-changing validation.
- Keep worklogs and handoff docs updated when a session materially changes repo state.

## Daily Start/End Rules Replaced

Older blanket instructions in this file such as always running `git pull` at the start are no longer universal.

Current Git rules:

- Codex may continue mainline work on local `main`.
- Do not frequently pull/push unless the workflow actually requires it.
- Push only when the user explicitly asks, except for the separately confirmed daily backup rule outside this file.

## Historical Note

This file was written when the repository still framed itself as a company-internal Revit AI Agent workflow with broader multi-version and process ambitions. Keep it as archive context, not as the active project contract.
