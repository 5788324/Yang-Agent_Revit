# YangAgent Revit New Chat Handoff - 2026-06-07

Use this file when starting a new Codex chat after context compaction.

## Current Authority

The active project direction was simplified on 2026-06-11.

Use these documents first:

1. `docs/product-brief.md`
2. `docs/simple-roadmap.md`
3. `docs/project-rules.md`
4. `docs/agent-operating-model.md`
5. this handoff

Older company, enterprise, MCP-first, Bridge, and commercial planning material is historical reference only.

## Repository State

- Repository: `https://github.com/5788324/Yang-Agent_Revit`
- Local path: `D:\codex\Yang Agent_Revit`
- Branch: `main`
- Local status at handoff time: `main...origin/main [ahead 11]`
- Do not push unless the user explicitly asks.
- Current project goal: personal-use Revit assistant, not an enterprise/commercial plugin platform.

## Current Scope

- Product: personal Revit AI assistant.
- Current one-week target: pyRevit MVP usable in a sandbox model.
- Primary implementation layer: pyRevit.
- C# DLL: lightweight Revit 2027 skeleton only, not the current mainline.
- Long-term version target: Revit 2022-2027, with pyRevit as the first multi-version route.
- MCP: future automatic reading and controlled modification only after the plugin workflow is stable.
- Gemini C# toolbox: external asset pending isolated intake after the user provides the path.

## Recent Mainline Commits

- `686997a fix: block duplicate apply csv rows`
- `e16a95c chore: add apply csv validator`
- `7d72bc4 chore: add generic Revit addin scripts`
- `90806dd chore: add version plan and static checks`

## Key Completed Work

- Added version boundary doc: `docs/revit-version-support-plan.md`.
- Added sandbox run guidance doc: `docs/sandbox-pyrevit-mvp-runbook.md`.
- Added compact sandbox operator checklist: `docs/sandbox-pyrevit-mvp-checklist.md`.
- Added one-command offline sandbox preflight: `python tools\run_sandbox_preflight.py --write-report`.
- Added sandbox feedback template: `docs/sandbox-pyrevit-mvp-feedback-template.md`.
- Added shared apply helper module: `pyrevit/YangAgent.extension/lib/yang_agent_apply.py`.
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
- Hermes/DeepSeek review findings are advisory only and do not authorize implementation changes.

## Verified Commands

Run from `D:\codex\Yang Agent_Revit`.

```powershell
python -m py_compile tools\static_checks.py tools\validate_apply_csv.py tools\check_pyrevit_extension.py
python tools\check_pyrevit_extension.py
python tools\static_checks.py --write-report
python tools\validate_apply_csv.py --kind room --csv tests\fixtures\missing_room_numbers_valid.csv
python tools\validate_apply_csv.py --kind mark --csv tests\fixtures\missing_door_window_marks_valid.csv
python tools\validate_apply_csv.py --kind room --csv tests\fixtures\missing_room_numbers_duplicate.csv
python tools\validate_apply_csv.py --kind mark --csv tests\fixtures\missing_door_window_marks_duplicate.csv
powershell -NoProfile -ExecutionPolicy Bypass -File scripts\build-revit-addin.ps1 -Version 2027 -OutputPath C:\tmp\YangAgent_Revit2027_build_check
powershell -NoProfile -ExecutionPolicy Bypass -File scripts\build-revit-addin.ps1 -Version 2024
```

Expected:

- pyRevit preflight: `0 errors`.
- Static check: `0 errors`, currently `11 warnings`.
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

1. Keep the project scoped as a personal Revit AI assistant.
2. Run `python tools\check_pyrevit_extension.py`.
3. Run `python tools\run_sandbox_preflight.py --write-report`.
4. Use `docs/sandbox-pyrevit-mvp-checklist.md` for the first live sandbox run.
5. Use `docs/sandbox-pyrevit-mvp-feedback-template.md` to capture the first blocker.
6. Fix only that first live blocker before expanding scope.
7. When the user provides the Gemini C# toolbox path, intake it through `docs/external-toolbox-intake.md`.
8. Keep C# DLL, MCP, and Revit 2022-2027 expansion out of this week's hard target.

## Hermes / DeepSeek Tasks

Hermes should work on a separate branch, not `main`.

Recommended branch:

```powershell
git checkout -b hermes/read-only-checks
```

Allowed:

- Run `python tools\static_checks.py --write-report`.
- Run `python tools\validate_apply_csv.py` on fixture CSVs or user-provided dry-run CSVs.
- Read `pyrevit/**/script.py`, `src/**`, `tools/**`, and `tests/**` in a review-only mode.
- Write draft reports under `docs/drafts/`.
- Perform only the currently assigned bounded tasks from `docs/hermes-next-tasks.md`.

Forbidden:

- Do not edit `pyrevit/**/script.py`.
- Do not edit `src/**`.
- Do not edit `tools/**`.
- Do not edit `tests/**`.
- Do not edit `scripts/**`.
- Do not edit `addins/**`.
- Do not run install/build scripts.
- Do not run Revit.
- Do not add `.rvt` files.
- Do not merge, push, or pull.

Review note for Hermes draft output:

- Hermes draft audit tables may quote old or intentionally broken command examples as evidence.
- Treat those quoted examples as review artifacts, not as execution instructions.
- Only commands repeated in the main handoff, user guide, troubleshooting, or testing docs should be treated as active guidance.
- Hermes task iteration is controlled through `docs/hermes-next-tasks.md`; Hermes should not self-expand beyond the current task pack.
- Hermes may now perform bounded read-only code review, but its conclusions remain advisory and do not authorize implementation changes.
- Hermes Round 1 is currently `reviewed: follow-up required` because the required structured draft report files were missing and a screenshot summary is not accepted as final delivery.

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
- This is a personal Revit AI assistant, not an enterprise platform or commercial plugin.
- Prioritize getting the pyRevit MVP usable in a sandbox model.
- Do not directly modify production Revit models.
- All model-changing features must follow dry-run -> human confirmation -> apply.
- Long-term target includes Revit 2022-2027, but current C# DLL implementation is Revit 2027 only.
- MCP automatic reading and controlled modification are future goals, not this week's delivery target.
- Gemini C# toolbox should be isolated and reviewed before any migration.
- Hermes/DeepSeek handles read-only checks, draft docs, and bounded read-only code review only; Codex owns core code, implementation, and final review.

Continue mainline work from the current repo state.
```
