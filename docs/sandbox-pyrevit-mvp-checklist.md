# pyRevit MVP Sandbox Checklist

Use this page as the compact operator checklist for the first real sandbox-model run.

This file is the short execution sheet.
For explanation and context, use `docs/sandbox-pyrevit-mvp-runbook.md`.

## Before Revit

1. Action: run `python tools\check_pyrevit_extension.py`
   Expected: `Summary: 0 errors, 0 warnings`
   If it fails: stop and check pyRevit bundle structure or syntax output first.

2. Action: run `python tools\run_sandbox_preflight.py --write-report`
   Expected: all 7 steps show `PASS`
   If it fails: open `docs/drafts/sandbox-preflight-report.md` and stop at the first failed step.

3. Action: confirm the latest preflight report path
   Expected: `docs/drafts/sandbox-preflight-report.md`
   If it is missing: rerun the preflight command before opening Revit.

## Install / Refresh

4. Action: if `YangAgent` is missing or stale, run `.\scripts\install-pyrevit-extension.ps1 -Force -ClearCache`
   Expected: extension is refreshed
   If it fails: stop and capture the exact script error text.

5. Action: restart Revit or reload pyRevit
   Expected: `pyRevit` tab and `YangAgent` tab are both visible
   If either tab is missing: stop and fill the feedback template.

## Live Button Order

6. Action: open a local `*_sandbox.rvt` or `*_test.rvt` model
   Expected: disposable sandbox model is open
   If not: stop and do not use a production model.

7. Action: run buttons in this order
   Expected: each step produces the expected file or visible result before moving on
   If one step fails: stop at the first blocker and fill the feedback template

   1. `System Settings`
   2. `Export Model Snapshot`
   3. `Model Health Report`
   4. `Export Regression Checklist`
   5. `Export AI Review Prompt`
   6. `Preview Missing Marks`
   7. `Preview Missing Room Numbers`
   8. `Preview Duplicate Room Numbers`
   9. `Preview Unplaced Views`
   10. `Preview View Naming Rules`
   11. `Apply Missing Door Window Marks`
   12. test one Revit Undo
   13. `Apply Missing Room Numbers`
   14. test one Revit Undo
   15. switch language to `English`
   16. rerun one or two report buttons

## If Something Fails

8. Action: fill `docs/sandbox-pyrevit-mvp-feedback-template.md`
   Expected: one record for one first blocker
   If multiple things fail: record only the first blocking issue first.

9. Action: include the runbook step number in the report
   Expected: Codex can map the failure back to the exact sequence point
   If the step number is unclear: use the order in `docs/sandbox-pyrevit-mvp-runbook.md`.

10. Action: stop after the first blocker
    Expected: no scope expansion before Codex triage
    If you keep testing anyway: later failures are secondary and should not replace the first blocker report.
