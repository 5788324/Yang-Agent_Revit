# Hermes W3-003 ViewGraphicCleaner Inventory Review

Reviewed Hermes delivery:

- `G:\Hermes Agent\YangAgent Revit\YangAgent Revit\docs\drafts\2026-06-14_hermes_W3-003_delivery`

Decision:

- `accepted with direction correction`

What passed review:

- Hermes read through the thin command shell and the real WPF window logic instead of stopping at the command entry point.
- The inventory correctly identified the core business operation:
  - inspect per-element overrides in a view;
  - clear them with `view.SetElementOverrides(id, new OverrideGraphicSettings())`.
- The inventory also correctly separated the true complexity from the core tool logic:
  - current-view override clearing is simple;
  - the heavy part is the Gemini multi-view WPF manager, search UI, selection UX, and grouped transaction orchestration.
- The inventory correctly states that the Gemini implementation does not touch:
  - category-level VG overrides;
  - filter overrides;
  - view templates;
  - element hide/unhide state;
  - element deletion.

Direction correction from Codex:

- Do **not** proceed with a preview-plus-apply split for V1.
- Current YangAgent product rule is already fixed by user decision:
  - no preview by default for future migration work;
  - direct-apply is allowed for personal-use tools when the impact is local, the confirmation is explicit, the transaction is named, logs are exported, and Undo is clear.
- Therefore the V1 migration target for this feature is:
  - one direct-apply current-view tool only.

Approved V1 shape:

- Target button name:
  - `ApplyViewGraphicClean`
- Scope:
  - active view only;
  - clear element-level overrides only;
  - no batch multi-view manager;
  - no WPF shell migration.
- Required confirmation content:
  - document title;
  - active view name;
  - override count to be cleared;
  - explicit warning that element-level graphic overrides in the active view will be reset.
- Required logging:
  - Markdown + CSV;
  - include at least `view_name`, `view_id`, `element_id`, `category`, `result`, `message`.

Deferred scope:

- Gemini-style multi-view manager remains out of current V1.
- Any future batch cleaning across views should be reconsidered separately after the single-view direct-apply path is stable.

Next Hermes package:

- `HERMES-W3-004 ApplyViewGraphicClean Draft`
