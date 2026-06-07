# YangAgent Revit New Chat Handoff - 2026-06-07

Use this file when starting a new Codex chat after context compaction.

## Repository State

- Repository: `https://github.com/5788324/Yang-Agent_Revit`
- Local path: `D:\codex\Yang Agent_Revit`
- Branch: `main`
- Local status at handoff time: `main...origin/main [ahead 11]`
- Do not push unless the user explicitly asks.
- Current project goal: personal-use Revit assistant, not an enterprise/commercial plugin platform.

## Current Scope

- Primary implementation layer: pyRevit MVP.
- Official plugin layer: lightweight C# DLL skeleton.
- First Revit version phase: Revit 2024-2027.
- Current implemented C# DLL track: Revit 2027 only.
- Revit 2011-2023: deferred compatibility backlog only.
- MCP / Bridge / skills: deferred until the export/report workflow is stable.

## Recent Mainline Commits

- `686997a fix: block duplicate apply csv rows`
- `e16a95c chore: add apply csv validator`
- `7d72bc4 chore: add generic Revit addin scripts`
- `90806dd chore: add version plan and static checks`

## Key Completed Work

- Added version boundary doc: `docs/revit-version-support-plan.md`.
- Added static repo checker: `tools/static_checks.py`.
- Added offline apply CSV validator: `tools/validate_apply_csv.py`.
- Added valid and duplicate CSV fixtures under `tests/fixtures/`.
- Added generic C# DLL scripts:
  - `scripts\build-revit-addin.ps1`
  - `scripts\install-revit-addin.ps1`
- Kept beginner wrappers:
  - `scripts\build-revit2027-addin.ps1`
  - `scripts\install-revit2027-addin.ps1`
- Made Revit 2024/2025/2026 DLL scripts fail clearly with `YA-CS-VERSION-PLANNED`.
- Hardened both apply tools:
  - wrong CSV name is blocked;
  - missing fields are blocked;
  - duplicate `element_id` is blocked before user confirmation;
  - logs include Undo / rollback notes.

## Safety Rules

- Do not directly modify production Revit models.
- Use only sandbox/test Revit models for apply testing.
- All model-changing features must follow: dry-run -> human confirmation -> apply.
- Do not claim Revit Undo is verified unless it was manually tested in a sandbox model.
- Do not commit `.rvt`, `.rfa`, customer data, API keys, `%APPDATA%` config, or generated local exports.
- Hermes/DeepSeek output is draft until Codex reviews it.

## Verified Commands

Run from `D:\codex\Yang Agent_Revit`.

```powershell
python -m py_compile tools\static_checks.py tools\validate_apply_csv.py
python tools\static_checks.py --write-report
python tools\validate_apply_csv.py --kind room --csv tests\fixtures\missing_room_numbers_valid.csv
python tools\validate_apply_csv.py --kind mark --csv tests\fixtures\missing_door_window_marks_valid.csv
python tools\validate_apply_csv.py --kind room --csv tests\fixtures\missing_room_numbers_duplicate.csv
python tools\validate_apply_csv.py --kind mark --csv tests\fixtures\missing_door_window_marks_duplicate.csv
powershell -NoProfile -ExecutionPolicy Bypass -File scripts\build-revit-addin.ps1 -Version 2027 -OutputPath C:\tmp\YangAgent_Revit2027_build_check
powershell -NoProfile -ExecutionPolicy Bypass -File scripts\build-revit-addin.ps1 -Version 2024
```

Expected:

- Static check: `0 errors`, currently `15 warnings`.
- Valid CSV fixtures: pass.
- Duplicate CSV fixtures: fail with `YA-APPLY-*-CSV-007`.
- Revit 2027 temp build: succeeds with known `MSB3277` warnings.
- Revit 2024 build: stops with `YA-CS-VERSION-PLANNED`.

## Known Not Yet Verified

- Revit UI button clicks in a live Revit session.
- Revit 2027 DLL load after restart.
- Revit Undo for apply tools in a sandbox model.
- Full pyRevit regression checklist in a real sandbox model.

Do not mark these as verified until the user or a live Revit session confirms them.

## Next Codex Tasks

1. Help the user run pyRevit MVP on a sandbox Revit model.
2. Fix the first blocking real-use issue found from that run.
3. Keep C# DLL small: Ribbon, About, config folder, reports folder, placeholders only.
4. Continue hardening apply safety and logs.
5. Promote useful Hermes docs into main docs only after review.

## Hermes / DeepSeek Tasks

Hermes should work on a separate branch, not `main`.

Recommended branch:

```powershell
git checkout -b hermes/read-only-checks
```

Allowed:

- Run `python tools\static_checks.py --write-report`.
- Run `python tools\validate_apply_csv.py` on fixture CSVs or user-provided dry-run CSVs.
- Write draft reports under `docs/drafts/`.
- Classify the 15 static-check warnings into:
  - old/historical docs to ignore;
  - docs that should be fixed;
  - items that need Codex decision.

Forbidden:

- Do not edit `pyrevit/**/script.py`.
- Do not edit `src/**`.
- Do not edit `scripts/**`.
- Do not edit `addins/**`.
- Do not run install/build scripts.
- Do not run Revit.
- Do not add `.rvt` files.
- Do not merge, push, or pull.

## New Chat Startup Prompt

Copy this into the next Codex chat:

```text
We are continuing the YangAgent Revit project.

Repository: https://github.com/5788324/Yang-Agent_Revit
Local path: D:\codex\Yang Agent_Revit

Please start by running:
1. git status --short --branch
2. Read docs/handoff-new-chat-2026-06-07.md
3. Read docs/next-steps.md
4. Read docs/worklogs/worklog-2026-06-07.md from the latest relevant section

Current state:
- main is ahead of origin locally; do not push unless I explicitly ask.
- This is a personal Revit assistant, not an enterprise platform.
- Prioritize getting the pyRevit MVP usable in a sandbox model.
- Do not directly modify production Revit models.
- All model-changing features must follow dry-run -> human confirmation -> apply.
- Current C# DLL implemented track is Revit 2027 only.
- Revit 2024/2025/2026 are planned tracks; Revit 2011-2023 are deferred backlog.
- Hermes/DeepSeek handles read-only checks and draft docs only; Codex owns core code and review.

Continue mainline work from the current repo state.
```
