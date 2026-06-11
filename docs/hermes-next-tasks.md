# Hermes Next Tasks

Hermes/DeepSeek is now enabled for bounded read-only code review, but still not for implementation.

This file is the active task contract. If any older draft conflicts with it, follow this file.

## Task Status

- Round 1 status: accepted by Codex on 2026-06-11
- Round 1 review result: accepted with low-risk follow-up backlog
- Hermes screenshot summaries are not accepted as final delivery; the structured draft files are now present

## Round 1 Accepted Files

Accepted Round 1 reports:

- `docs/drafts/hermes-code-review-apply-tools.md`
- `docs/drafts/hermes-feature-review-sandbox-runbook.md`

Remaining code-review follow-ups are low risk and do not block the sandbox MVP:

- Marks `wrong_csv_name` can optionally add duplicate-CSV guidance.
- `is_applicable_row` style can optionally be normalized.
- Markdown detail output can optionally be made more symmetric.

Do not start broad Round 2 implementation work until Codex assigns a new bounded task.

## Current Direction

- Project position: personal Revit assistant, optionally shareable with friends
- Mainline owner: Codex
- Hermes role: docs support, read-only checks, read-only code review, feature review summaries
- Do not use Hermes for core implementation, install/build flow, or Revit execution

## Branch

Hermes must work on a separate branch:

```powershell
git checkout -b hermes/read-only-checks
```

Do not work on `main`.

## Hard Boundaries

Hermes must not:

- edit `pyrevit/**/script.py`
- edit `src/**`
- edit `tools/**`
- edit `tests/**`
- edit `scripts/**`
- edit `addins/**`
- run Revit
- run install/build scripts
- merge, push, or pull
- add `.rvt`, `.rfa`, client data, or local config exports
- reintroduce enterprise/company-platform wording into current mainline docs

Hermes may:

- run `python tools\static_checks.py --write-report`
- run `python tools\validate_apply_csv.py` on fixture CSVs or user-provided dry-run CSVs
- read `pyrevit/**/script.py`, `src/**`, `tools/**`, and `tests/**` in a review-only mode
- edit or add `docs/drafts/*.md`
- prepare Codex-review notes for documentation cleanup, code review, or feature review

## Task Template: Code Review Task

Every Hermes code review task must include:

- review subject
- allowed read paths
- review goals
- output file
- forbidden actions
- report-back format

Output naming:

- Code review reports use the form `docs/drafts/hermes-code-review-apply-tools.md`.
- Feature review reports use the form `docs/drafts/hermes-feature-review-sandbox-runbook.md`.
- For future rounds, keep the same prefix and replace only the final slug with a short lowercase topic name.

## Round 1 Tasks

Hermes must complete only the two tasks below in this round.

### Task 1: Apply Tools Code Review

Review subject:

- `pyrevit/**/ApplyMissingDoorWindowMarks.pushbutton/script.py`
- `pyrevit/**/ApplyMissingRoomNumbers.pushbutton/script.py`

Allowed read paths:

- `pyrevit/YangAgent.extension/**/ApplyMissingDoorWindowMarks.pushbutton/*`
- `pyrevit/YangAgent.extension/**/ApplyMissingRoomNumbers.pushbutton/*`
- `docs/error-codes.md`
- `docs/testing-and-qa.md`
- `docs/safety-rules.md`

Review goals:

- confirm whether the `dry-run -> confirm -> apply` flow is consistent across both tools
- identify user-misoperation risks
- identify inconsistencies in errors, logs, or Undo/rollback wording
- identify any obvious review-only bug risks that do not require live Revit to notice
- identify which questions cannot be answered without live Revit

Output file:

- `docs/drafts/hermes-code-review-apply-tools.md`

Forbidden actions:

- do not suggest direct code patches as if they are approved fixes
- do not claim Revit API behavior unless it is supported by the current code or current docs
- do not edit any mainline code files

### Task 2: Sandbox Runbook Feature Review

Review subject:

- `docs/sandbox-pyrevit-mvp-runbook.md`

Allowed read paths:

- `docs/sandbox-pyrevit-mvp-runbook.md`
- `docs/next-steps.md`
- `docs/testing-and-qa.md`
- `docs/troubleshooting.md`
- `docs/handoff-new-chat-2026-06-07.md`

Review goals:

- check whether the live sandbox sequence is clear for a human operator
- identify missing feedback fields needed after a failed live run
- identify steps that may be easy to misunderstand or skip
- suggest where a compact human checklist would help
- if a compact checklist is clearly derivable now, include it only as an appendix inside the draft review report, not as a replacement for the main runbook
- identify which parts still depend on live Revit evidence

Output file:

- `docs/drafts/hermes-feature-review-sandbox-runbook.md`

Forbidden actions:

- do not rewrite the main runbook directly
- do not invent new recovery steps that are not grounded in current docs
- do not mark any live Revit step as already verified

## Required Report Back

Hermes must report back in this format:

```text
Branch:
- hermes/read-only-checks

Changed files:
- ...

Summary:
- ...

Checks run:
- ...

Review conclusions:
- ...

Safety confirmation:
- I did not edit pyRevit scripts.
- I did not edit C# files.
- I did not edit tools, tests, scripts, or addin templates.
- I did not run install/build scripts.
- I did not run Revit.
- I did not add .rvt or .rfa files.
- I did not run git merge / push / pull.
- My code conclusions are review findings only, not implementation decisions.

Questions for Codex:
- ...
```

## Codex Review Standard

Codex should accept Hermes output only when it contains:

- clear bug risk or user-flow risk
- clear test gaps
- clear inconsistency findings in logs, errors, or instructions
- clear separation between code facts and live-Revit unknowns

Codex should reject Hermes output that:

- touches implementation files
- reintroduces enterprise/platform scope
- gives unsafe Revit execution advice
- treats audit evidence as copy/paste instructions
- makes unsupported Revit API claims
- drifts into approved-fix language instead of review language
