# Next Steps

Current goal:

```text
Make the pyRevit MVP usable in a sandbox Revit model.
```

Daily handoff rule:

```text
Start safely with Git status and core-doc refresh. End with worklog, next-steps, startup prompt, and a safe Git checkpoint.
```

Primary execution rule:

```text
Finish the usable YangAgent core first. Gemini toolbox migration comes later.
```

## Current Project Position

- Personal Revit AI assistant.
- Not a company platform.
- Not a commercial plugin.
- Not an MCP-first project.
- Current implementation focus: pyRevit.
- C# DLL stays small unless there is a concrete work need.
- Long-term target includes Revit 2022-2027 and MCP controlled read/write, but not before the personal MVP is useful.

## This Week

1. Keep the project scope simple and personal.
2. Run the offline preflight.
3. Snowdon report and CSV data-quality review is complete; continue with bounded fixes from concrete findings.
4. Capture the next real blocker from actual use.
5. Fix only that next blocker.
6. Do not expand Gemini toolbox migration until the sandbox flow works.
7. Keep MCP, micro toolbox, and project asset manager as important later core features, but do not let them block the first usable pyRevit MVP.
8. Start a separate doc audit pass: read each retained doc once, mark stale duplicates, and decide keep / merge / archive / delete.
9. Run the next doc-governance pass on high-impact Chinese-facing docs that currently display garbled in terminal review.
10. Continue the governance pass on remaining active support docs until daily testing, troubleshooting, and external intake docs are all current and readable.
11. Treat the broad doc-governance cleanup as mostly complete; focus next on code review, live validation, and bounded external-agent code deliveries.
12. Continue scanning active shared libs and high-traffic button scripts for legacy garbled strings or stale behavior assumptions uncovered during the governance pass.
13. Keep separating true product-mainline directories from local environment-helper side branches so future chats do not waste time treating support scripts as product scope.
14. Treat the main `Reports.pulldown` cleanup as largely done; next scan only the still-unreviewed active UI/resource files outside that surface.
15. `ProjectInfoReport` runtime cache/registration blocker is fixed.
16. Snowdon report/preview/apply/Undo validation is complete.
17. Snowdon report/CSV data-quality review is complete; the blank-text and door/window family/type export fixes were validated on regenerated output.
18. Apply tool safety review is complete for the two current model-modifying buttons.

## Current Execution Pack

- `docs/sandbox-pyrevit-mvp-runbook.md`
- `docs/sandbox-pyrevit-mvp-checklist.md`
- `docs/sandbox-pyrevit-mvp-feedback-template.md`
- `python tools\run_sandbox_preflight.py --write-report`

## Current Validation Commands

Run from repository root:

```powershell
python tools\check_pyrevit_extension.py
python tools\run_sandbox_preflight.py --write-report
python tools\static_checks.py --write-report
```

Expected:

- `check_pyrevit_extension.py`: `0 errors`
- sandbox preflight: all steps `PASS`
- static checks: `0 errors`

## Daily Project Ops

Use:

- `docs/framework/daily-ops-routine.md`

Mandatory daily core docs:

- `docs/worklogs/worklog-YYYY-MM-DD.md`
- `docs/next-steps.md`
- `docs/new-chat-startup-YYYY-MM-DD.md`

Second-round document governance reference:

- `docs/framework/document-governance-audit-2026-06-13.md`

Current live-test support pack:

- `docs/troubleshooting.md`
- `docs/error-codes.md`
- `docs/sandbox-snowdon-live-pack-2026-06-13.md`
- `docs/worklogs/worklog-2026-06-14.md`
- `docs/new-chat-startup-2026-06-14.md`

Latest live evidence:

- pyRevit rebuilt `C:\Users\YANG\AppData\Roaming\pyRevit\2027\pyRevit_2027_6e209f291442d185_YangAgent.dll`.
- The rebuilt DLL contains `yangagent_yangagent_reports_reports_projectinforeport`.
- Snowdon sandbox generated:
  - `project_info_report_20260614_105341.md`
  - `project_info_report_20260614_105621.md`
- User manually confirmed all report/export/preview buttons exported successfully.
- User manually confirmed both apply tools completed successfully and Revit Undo worked.
- Regenerated Snowdon health report `model_health_report_20260614_113012.md` correctly reports `3` manually created missing room numbers.
- Regenerated Snowdon snapshot `model_snapshot_20260614_113025.json` keeps counts consistent: `67` rooms, `321` doors/windows, `507` sheets/views, `18` levels, `75` model categories.
- Regenerated `rooms_20260614_113025.csv` no longer converts blank text fields to `"0"`.
- Regenerated `doors_windows_20260614_113025.csv` has nonblank `family_name` and `type_name` for all `321` rows.
- Shared library import smoke test passed for settings, theme, report style, apply helpers, and language helpers.
- `python tools\run_sandbox_preflight.py --write-report` passed all checks.
- Hermes ModelHealthReport delivery was reviewed; Codex integrated corrected view naming and risk notes logic without copying the delivered script directly.
- Snowdon live validation passed for the enhanced `Model Health Report`: `View Naming Check`, `Risk Notes`, and updated issue count are present and internally consistent.
- Snowdon live validation passed for regenerated `Export Model Snapshot`: summary duplicate bullets are fixed and CSV/JSON counts remain consistent.
- C# WPF theme bridge added for future Gemini rewrites; `YangAgent.Revit2027` build succeeds with warnings and `0` errors.
- Hermes `HERMES-W0-001` and `HERMES-W2-001` deliveries were reviewed and accepted.
- Hermes `HERMES-W2-002 TextModifier Preview Draft` was reviewed and accepted with Codex integration fixes.
- Mainline now includes `PreviewTextFindReplace.pushbutton`; offline checks pass.
- Hermes `HERMES-W2-003 TextModifier Apply Draft` revision 1 was reviewed and accepted with Codex integration fixes.
- Mainline now includes `ApplyTextFindReplace.pushbutton`; offline checks pass.
- Hermes workspace copy of the board may be stale because automatic sync was blocked by usage-limit approval review; use the main-repo board as authority if needed.

Current repo-skeleton conclusion:

- pyRevit mainline: `pyrevit/YangAgent.extension/`
- shared libs: `pyrevit/YangAgent.extension/lib/`
- C# DLL track: `src/YangAgent.Revit2027/`
- offline validators: `tools/`
- install/build wrappers: `scripts/`
- MCP/sample dirs: placeholders, not current sprint delivery

Git rule:

- at start of day, run `git status --short --branch` and `git log -3 --oneline`;
- pull only when the tree is safe;
- at end of day, push only when the checkpoint is real and reviewable.

pyRevit runtime rule:

- after adding a new `.pushbutton` or changing button registration metadata, Codex must proactively rebuild the YangAgent pyRevit runtime cache before asking the user to click the new button;
- use `scripts\rebuild-pyrevit-yangagent-runtime.ps1` after Revit is fully closed;
- do not wait for the user to hit a `FullClassName` / `IExternalCommand` error first.

## Human Sandbox Run

Use only a test model:

- file name should include `_sandbox` or `_test`;
- do not use a production model;
- stop at the first blocker;
- fill `docs/sandbox-pyrevit-mvp-feedback-template.md`.

## Next Review Order

Use the generated Snowdon reports and CSVs from the current report directory.

1. Keep the next Revit validation focused on one new or changed button at a time.
2. Stop polishing the current report/preview/apply buttons unless a concrete blocker appears.
3. Run `Apply Text Find Replace` once in the sandbox model and verify exported log plus full Revit Undo.
4. Hermes should proceed to `HERMES-W3-006 ApplyVisibilityCopy Draft`.
5. Mainline integration has started for accepted Hermes buttons. Current integrated set now includes:
   - `ApplyTextMerge`
   - `ApplyDimTextOverride`
   - `ApplyTextDistribute`
   - `PreviewChineseContent`
6. After each new batch lands in `Reports.pulldown`, rerun `python tools\check_pyrevit_extension.py` before live Revit validation.
5. Review any Hermes/DeepSeek delivery only when it appears under `docs/incoming/` or the assigned Hermes drafts path with a delivery report.
6. Continue code-diff review only as needed to protect a Git checkpoint.
7. Fix concrete bugs only; do not expand feature scope.
8. Use `docs/governance/gemini-feature-restoration-map-2026-06-14.md` as the current product target for Gemini capability restoration.
9. Require future Gemini-origin drafts to follow `docs/governance/gemini-plugin-authoring-spec-2026-06-14.md`.

## Immediate Pivot

Reason:

- The current report/preview/apply button set has consumed too much time.
- The user urgently needs Gemini/MCP-style working capabilities for real Revit work.
- Gemini's existing implementation is not trusted enough to merge directly.
- The user wants controlled full migration over time, not isolated one-off copies.

Next practical target:

1. Finish wave 0 theme/design-system guardrails so both pyRevit and C# rewrites use shared `theme_id`.
2. Start wave 2 with the text and annotation tool family because it has the fastest daily-work payoff.
3. Keep MCP in wave 4 until the safety shell is explicit.
4. Rebuild Gemini tools under YangAgent standards instead of preserving Gemini's architecture.
5. Validate each migrated tool in Snowdon sandbox before moving to the next.

## AI Agent Work Split

Codex:

- project direction;
- task package authoring;
- architecture, theme, safety, MCP boundary decisions;
- final review;
- merge decisions;
- key blocker fixes only;
- live Revit validation records;
- Git release decisions.

Hermes / Gemini / DeepSeek:

- execute assigned task packages;
- inventory and audit;
- draft low-risk code;
- delivery reports;
- checklist cleanup;
- offline self-checks.

Rules:

- use `docs/governance/codex-hermes-v1-migration-board-2026-06-14.md` as the active task board;
- use `docs/agent-development-rules.md`;
- use `docs/agent-task-template.md` for assigned work;
- use `docs/agent-delivery-report-template.md` for every delivery;
- place external packages or reports under `docs/incoming/`;
- record Codex review under `docs/reviews/`;
- do not merge external work without Codex review.
- do not let Hermes redesign architecture, theme, safety rules, MCP behavior, or product naming.

If the user works in an environment without Git or Codex, Gemini/DeepSeek may deliver zip files, folders, screenshots, and Markdown reports. Every delivery still needs a `delivery-report.md`.

## Gemini Toolbox

Gemini C# toolbox path:

```text
G:\Codex\YangAgent Revit\YangAgent Revit\Gemini 资料\YangTools_SourceCode
```

Use:

- `docs/external-toolbox-intake.md`
- `docs/reviews/gemini-toolbox-initial-inventory-2026-06-13.md`

Do not merge the toolbox directly.

First classify every tool as:

- read-only;
- low-risk model change;
- high-risk model change;
- useful idea but poor implementation;
- not needed.

Default decision: rewrite selected useful tools in YangAgent style instead of modifying the whole Gemini toolbox in place.

Current intake status:

- Initial inventory completed.
- High-risk areas identified: auto-start MCP server, dynamic Python execution, auto-deploy build target, broad family/delete/batch operations.
- User confirmed the Gemini toolbox functions are important for daily work.
- MCP, micro toolbox, and project asset manager are important later core features.
- Current decision: defer Gemini feature migration until the YangAgent core is usable in sandbox.

## Later, Not This Week

- Revit 2022-2027 support.
- MCP automatic model reading.
- MCP controlled model modification.
- Wider C# migration.
- More daily-work plugins from the Gemini toolbox.
