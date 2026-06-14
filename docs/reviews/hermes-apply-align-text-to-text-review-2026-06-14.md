# Hermes W2-010 ApplyAlignTextToText Review

Reviewed Hermes delivery:

- `G:\Hermes Agent\YangAgent Revit\YangAgent Revit\docs\drafts\2026-06-14_hermes_W2-010_delivery`

Decision:

- `needs changes`

Main blocker:

- The alignment-mode chooser currently treats cancel as a silent fallback to `left`.
- In `choose_mode(lang)`, `forms.CommandSwitchWindow.show(...)` may return no selection, but the function then falls through to `return "left"`.
- For a direct-apply model-changing tool, cancel must stop the workflow instead of quietly picking a default alignment mode.

Required changes:

1. If the user cancels the alignment-mode picker, exit immediately with no model change.
2. Add explicit user-facing cancel output for the canceled mode-selection path, consistent with the rest of the direct-apply tools.
3. Do not use any implicit default mode after user cancellation.

Recommended same-pass correction:

- If a target `TextNote` has no bounding box in the active view, do not log it as a normal successful move with `OK`.
- Either:
  - fail the run before transaction; or
  - log that row as skipped/failed with a truthful message.

Why this is not accepted yet:

- Silent fallback from cancel to `left` can produce unintended model changes.
- That is a direct violation of the current YangAgent direct-apply confirmation standard.

Next Hermes package after revision:

- `HERMES-W2-010 revision 1`
