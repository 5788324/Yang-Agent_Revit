# Hermes Agent Task Brief

Hermes/DeepSeek is assigned only low-risk support work. Core development stays on `main`.

## Branch

Hermes must work on a separate branch:

```powershell
git checkout -b hermes/read-only-checks
```

Do not commit directly to `main`.

## Allowed Tasks

Hermes may do:

- Draft personal-user documentation.
- Summarize existing docs.
- Create button inventory tables.
- Simplify troubleshooting text for a beginner.
- Run read-only helper checks.
- Summarize `tools\static_checks.py` results.
- Summarize `tools\validate_apply_csv.py` results.

Recommended first outputs:

- `docs/drafts/hermes-static-check-review.md`
- `docs/drafts/hermes-apply-csv-validation-review.md`

## Forbidden Tasks

Hermes must not:

- Edit `pyrevit/**/script.py`.
- Edit C# files under `src/`.
- Edit `.addin` templates.
- Edit build or install scripts.
- Run install/build scripts.
- Operate Revit models.
- Commit `.rvt` files.
- Merge, push, or pull.
- Design MCP write-to-model flows.
- Add enterprise/commercial workflow documents.

## Required Report Back

When finished, Hermes must provide:

- Branch name.
- Changed files.
- One-line summary for each file.
- Confirmation that no code, install scripts, `.addin`, or `.rvt` files were changed.
- Confirmation that only read-only checks were run.
- Any unclear items that need review.

## Review Rules

Codex reviews Hermes work before merge:

- Reject changes that touch core code or scripts.
- Reject enterprise-scope expansion.
- Reject unsafe Revit instructions.
- Accept only simple documentation that helps personal MVP use.
