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
6. `docs/new-chat-startup-2026-06-13.md`

Older company, enterprise, MCP-first, Bridge, and commercial planning material is historical reference only.

## Repository State

- Repository: `https://github.com/5788324/Yang-Agent_Revit`
- Current local path: `G:\Codex\YangAgent Revit\YangAgent Revit`
- Previous local path: `D:\codex\Yang Agent_Revit`
- Migration status: completed on 2026-06-13. The G path is now a Git repository on `main...origin/main`.
- Deletion warning: do not delete the previous D path unless the user explicitly confirms deletion after checking the G path.
- Branch: `main`
- Latest confirmed status on 2026-06-13: `main...origin/main`
- Do not push unless the user explicitly asks.
- Current project goal: personal-use Revit assistant, not an enterprise/commercial plugin platform.

## Current Scope

- Product: personal Revit AI assistant.
- Current one-week target: pyRevit MVP usable in a sandbox model.
- Primary implementation layer: pyRevit.
- C# DLL: lightweight Revit 2027 skeleton only, not the current mainline.
- Long-term version target: Revit 2022-2027, with pyRevit as the first multi-version route.
- MCP: future automatic reading and controlled modification only after the plugin workflow is stable.
- Gemini C# toolbox: external asset at `G:\Codex\YangAgent Revit\YangAgent Revit\Gemini 资料\YangTools_SourceCode`; use isolated intake before any migration.
- Gemini feature priority: the toolbox functions are important, especially MCP, micro toolbox, and project asset manager, but migration is deferred until the YangAgent core is usable in sandbox.
- Hermes/Gemini/DeepSeek: may do bounded code/plugin/test drafts only from task sheets, with delivery reports and Codex review.

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
- Hermes/Gemini/DeepSeek code deliveries require a task sheet and delivery report before Codex review.
- External deliveries should go through `docs/incoming/` and `docs/reviews/`.

## Verified Commands

Run from current repository root:

```text
G:\Codex\YangAgent Revit\YangAgent Revit
```

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
7. Intake the Gemini C# toolbox through `docs/external-toolbox-intake.md`.
8. Keep C# DLL, MCP, micro toolbox, project asset manager, and Revit 2022-2027 expansion out of this week's hard target.
9. Keep the G path as the active development path.

## Hermes / Gemini / DeepSeek Tasks

External agents may now do bounded implementation drafts, but only with a task sheet and delivery report.

Use these documents:

- `docs/agent-development-rules.md`
- `docs/agent-task-template.md`
- `docs/agent-delivery-report-template.md`
- `docs/agent-review-checklist.md`
- `docs/daily-agent-log-template.md`

When Git is available, Hermes should work on a separate branch, not `main`.

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
- Write bounded candidate code only when a Codex task sheet explicitly allows it.
- Deliver zip/folder/Markdown reports when the user environment has no Git.

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
- Do not modify production Revit models.
- Do not introduce MCP or dynamic script execution as a model-changing default.

Review note for Hermes draft output:

- Hermes draft audit tables may quote old or intentionally broken command examples as evidence.
- Treat those quoted examples as review artifacts, not as execution instructions.
- Only commands repeated in the main handoff, user guide, troubleshooting, or testing docs should be treated as active guidance.
- Hermes task iteration is controlled through `docs/hermes-next-tasks.md`; Hermes should not self-expand beyond the current task pack.
- Hermes/Gemini/DeepSeek may now perform bounded code or plugin drafts when assigned, but their conclusions and patches remain advisory until Codex accepts them.
- Hermes Round 1 is currently `reviewed: follow-up required` because the required structured draft report files were missing and a screenshot summary is not accepted as final delivery.

## New Chat Startup Prompt

Copy this into the next Codex chat:

```text
We are continuing the YangAgent Revit project.

Repository: https://github.com/5788324/Yang-Agent_Revit
Current local path: G:\Codex\YangAgent Revit\YangAgent Revit
Previous local path: D:\codex\Yang Agent_Revit

Important: do not delete the previous D path unless the user explicitly confirms deletion.

Please start by running:
1. git status --short --branch
2. Read docs/handoff-new-chat-2026-06-07.md
3. Read docs/next-steps.md
4. Read docs/worklogs/worklog-2026-06-13.md from the latest relevant section
5. Read docs/new-chat-startup-2026-06-13.md

Current state:
- main is synced with origin unless `git status` says otherwise.
- This is a personal Revit AI assistant, not an enterprise platform or commercial plugin.
- Prioritize getting the pyRevit MVP usable in a sandbox model.
- Do not directly modify production Revit models.
- All model-changing features must follow dry-run -> human confirmation -> apply.
- Long-term target includes Revit 2022-2027, but current C# DLL implementation is Revit 2027 only.
- MCP automatic reading and controlled modification are future goals, not this week's delivery target.
- Gemini C# toolbox is at G:\Codex\YangAgent Revit\YangAgent Revit\Gemini 资料\YangTools_SourceCode and should be isolated, inventoried, and selectively rewritten rather than directly merged.
- Gemini toolbox functions are important but should not delay the first usable YangAgent core.
- Hermes/Gemini/DeepSeek may do bounded code/plugin drafts only with task sheets and delivery reports; Codex owns final review, merge, and quality gates.

Continue mainline work from the current repo state.
```
