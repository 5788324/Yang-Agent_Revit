# Hermes Capability Assessment

Date: 2026-06-07

## Verdict

Hermes/DeepSeek can continue as a docs-only helper agent.

It should work independently on bounded documentation tasks, then Codex reviews and imports selected output into the main repository.

## Evidence

Hermes completed:

- Personal quickstart draft.
- Button inventory.
- Troubleshooting summary.
- Button inventory audit.
- Troubleshooting audit.
- Install command audit.
- README improvement notes.
- Personal user guide outline.
- Error code cheatsheet.
- Cross-document consistency audit.

Observed strengths:

- Follows branch and scope instructions.
- Avoids pyRevit script, C#, install script, addin, and `.rvt` changes.
- Can compare docs against repo structure.
- Can identify copy/paste command issues.
- Can distinguish real issues from acceptable context differences.

Observed limitations:

- May reintroduce older wording from its own workspace if the main repo has moved ahead.
- Needs Codex review for safety phrasing.
- Sometimes states code-level behavior too strongly, especially Undo and model-modification guarantees.
- Should not modify core code or make Revit API decisions.

## Allowed Work

Hermes may work on:

- `docs/drafts/*.md`
- Documentation audits.
- Beginner-friendly guides.
- Button inventories.
- Troubleshooting summaries.
- README improvement notes.
- Error-code explanations.
- Cross-document consistency checks.

## Forbidden Work

Hermes must not:

- Edit `pyrevit/**/script.py`.
- Edit `src/**`.
- Edit `scripts/**`.
- Edit `addins/**`.
- Run Revit.
- Run install/build scripts.
- Add `.rvt` files.
- Run git merge/push/pull.
- Claim Revit behavior was manually verified unless the user explicitly tested it.

## Review Rule

Hermes output is accepted only after Codex review. Drafts can be imported, but final user-facing docs should be promoted selectively.
