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
- Read `pyrevit/**/script.py` in a code-review-only mode.
- Read `src/**`, `tools/**`, and `tests/**` in a code-review-only mode.
- Write code-review and feature-review reports under `docs/drafts/`.

Recommended first outputs:

- `docs/drafts/hermes-static-check-review.md`
- `docs/drafts/hermes-apply-csv-validation-review.md`

## Forbidden Tasks

Hermes must not:

- Edit `pyrevit/**/script.py`.
- Edit C# files under `src/`.
- Edit files under `tools/`.
- Edit files under `tests/`.
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
- Confirmation that any code conclusions are review findings only, not implementation decisions.

## Iteration Loop

Hermes work should run in a simple review loop:

1. Codex writes or updates the current task list in `docs/hermes-next-tasks.md`.
2. Hermes completes only the bounded task set.
3. Hermes reports back using the required format.
4. Codex reviews the output and either:
   - accepts selected draft material,
   - rejects unsafe or low-value output, or
   - issues the next bounded task pack.
5. Repeat. Do not let Hermes invent its own broader roadmap.

`docs/hermes-next-tasks.md` is the active task contract. If an older draft conflicts with it, follow `docs/hermes-next-tasks.md`.

## Code Review Upgrade Rule

Hermes may now perform bounded read-only code and feature review when Codex explicitly assigns it in `docs/hermes-next-tasks.md`.

This upgrade does not allow Hermes to implement fixes.

Hermes findings are advisory only:

- they may identify risks, test gaps, or user-flow problems
- they may point out inconsistencies in logs, errors, or interaction steps
- they must not be treated as implementation decisions without Codex review

Final design judgment and implementation judgment remain with Codex.

## Review Rules

Codex reviews Hermes work before merge:

- Reject changes that touch core code or scripts.
- Reject enterprise-scope expansion.
- Reject unsafe Revit instructions.
- Reject unsupported Revit API claims or speculative bug claims presented as fact.
- Accept only simple documentation that helps personal MVP use.
