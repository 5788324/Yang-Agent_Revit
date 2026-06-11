# pyRevit MVP Sandbox Runbook

Use this runbook for the first real sandbox-model validation of the current pyRevit MVP.

This file is execution guidance for a human Revit session. It is not proof that the checks already happened.

For the compact execution sheet, use `docs/sandbox-pyrevit-mvp-checklist.md`.

## Purpose

- verify that the pyRevit MVP actually loads in Revit
- verify the current report and preview buttons on a sandbox model
- verify the two low-risk apply tools with Undo in a sandbox model
- capture the first real blocking issue for Codex to fix

## Safety Rules

- Do not use a production model.
- Use only a local sandbox/test model such as `*_sandbox.rvt` or `*_test.rvt`.
- For apply testing, keep the model disposable or backed up.
- Do not mark Undo as verified unless one Revit Undo was manually tested after an apply run.

## Offline Preflight Before Opening Revit

Run from `D:\codex\Yang Agent_Revit`:

```powershell
python tools\run_sandbox_preflight.py --write-report
```

Expected:

- sandbox preflight: all steps `PASS`
- pyRevit preflight: `0 errors`
- static check: `0 errors`
- valid CSV fixtures: pass
- duplicate CSV fixtures: expected fail with `YA-APPLY-*-CSV-007`
- report written to `docs/drafts/sandbox-preflight-report.md`

If you need to troubleshoot one step manually, expand the single-command preflight into the individual commands recorded in the generated report.

## Install / Refresh the pyRevit Extension

If the extension is not already installed or you suspect stale cache:

```powershell
.\scripts\install-pyrevit-extension.ps1 -Force -ClearCache
```

Then restart Revit or reload pyRevit.

## Live Revit Validation Order

Use this exact order to reduce ambiguity when a button fails:

1. Open Revit.
2. Confirm the `pyRevit` tab is visible.
3. Confirm the `YangAgent` tab is visible.
4. Open a sandbox/test model.
5. Run `System Settings`.
6. Set language to `中文`.
7. Set or confirm the report export directory.
8. Run `Export Model Snapshot`.
9. Confirm JSON and CSV output files were created.
10. Run `Model Health Report`.
11. Confirm Markdown report output was created.
12. Run `Export Regression Checklist`.
13. Confirm checklist output was created.
14. Run `Export AI Review Prompt`.
15. Confirm prompt output was created.
16. Run `Preview Missing Marks`.
17. Confirm dry-run Markdown and CSV were created.
18. Run `Preview Missing Room Numbers`.
19. Confirm dry-run Markdown and CSV were created.
20. Run `Preview Duplicate Room Numbers`.
21. Confirm dry-run Markdown and CSV were created.
22. Run `Preview Unplaced Views`.
23. Confirm dry-run Markdown and CSV were created.
24. Run `Preview View Naming Rules`.
25. Confirm dry-run Markdown and CSV were created.
26. Run `Apply Missing Door Window Marks` on a reviewed `missing_door_window_marks_*.csv`.
27. Confirm apply log files were created.
28. Immediately test one Revit Undo.
29. Run `Apply Missing Room Numbers` on a reviewed `missing_room_numbers_*.csv`.
30. Confirm apply log files were created.
31. Immediately test one Revit Undo.
32. Reopen `System Settings`.
33. Switch language to `English`.
34. Rerun one or two report buttons and confirm English output.

## What To Record

For each failure, record:

- button name
- exact visible error message
- whether the button was gray, clickable, or failed after click
- whether any output files were created
- model name
- Revit version
- whether pyRevit reload or full restart was already tried

Use:

- `docs/sandbox-pyrevit-mvp-checklist.md`
- `docs/sandbox-pyrevit-mvp-feedback-template.md`

## First Blocker Rule

Do not branch into many fixes at once.

If the first live run fails:

1. record the first blocker clearly
2. stop expanding scope
3. give Codex the exact symptom, button name, and any output/log text

The next coding step should target that first blocker only.
