# Hermes W3-005 VisibilityCopier Inventory Review

Reviewed Hermes delivery:

- `G:\Hermes Agent\YangAgent Revit\YangAgent Revit\docs\drafts\2026-06-14_hermes_W3-005_delivery`

Decision:

- `accepted with implementation direction`

What passed review:

- Hermes correctly traced the real logic into the WPF window instead of stopping at the command shell.
- The inventory correctly identified the actual copy scope:
  - category hidden state;
  - category overrides;
  - filter assignment;
  - filter visibility;
  - filter overrides;
  - workset visibility.
- The inventory also correctly identified what is not copied:
  - element-level overrides;
  - templates;
  - view range;
  - element hide/unhide state.
- Hermes correctly identified the main risk:
  - overwrite-style propagation from one source view into one or more target views;
  - no diff preview;
  - no per-target logs;
  - no safe rollback evidence beyond raw Revit Undo.

Codex direction:

- User has now explicitly removed the preview-first requirement for this personal-use project.
- This feature may proceed as a direct-apply YangAgent tool as long as:
  - the scope is reduced;
  - the confirmation is explicit;
  - the transaction is named;
  - durable logs are written;
  - Undo is clearly surfaced.

Scope reduction required for future apply:

- source view: one
- target view: one
- no multi-target batch copy in current V1

Next Hermes package:

- `HERMES-W3-006 ApplyVisibilityCopy Draft`
