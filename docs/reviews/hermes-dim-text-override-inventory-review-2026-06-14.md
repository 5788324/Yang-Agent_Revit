# Hermes DimTextOverride Inventory Review - 2026-06-14

Reviewed delivery:

```text
G:\Hermes Agent\YangAgent Revit\YangAgent Revit\docs\drafts\2026-06-14_hermes_W2-006_delivery
```

Files reviewed:

- `hermes-dim-text-override-inventory.md`
- `delivery-report.md`
- Gemini source `Commands/DimTextOverrideCommand.cs`
- Gemini source `Commands/DimensionSelectionFilter.cs`

## Decision

`accepted with implementation direction`

## Accepted Conclusions

The inventory's main judgment is acceptable:

- `DimTextOverride` can stay direct-apply under the current no-preview project rule;
- it still needs stronger warning text than normal text tools because it can mislead production documentation;
- `clear` mode is lower risk than `replace` mode;
- logging must include row-level override details;
- one named Transaction plus Undo reminder is the correct transaction shape.

## Codex Decisions For Next Package

### 1. Direct-apply is acceptable

Decision:

- `yes`

Reason:

- the user explicitly authors the replacement text;
- the workflow is selection-scoped;
- no elements are deleted;
- one Transaction + Undo is sufficient for this personal-use project.

### 2. Replace and clear should stay in one button

Decision:

- `yes`

Target shape:

- one `ApplyDimTextOverride.pushbutton`
- mode switch inside the tool:
  - `replace`
  - `clear`

Reason:

- they are the same business workflow on the same target element type;
- splitting them would add friction without improving safety enough to justify it;
- `clear` is the natural recovery path for `replace`.

## Mandatory Requirements For HERMES-W2-007

The next implementation must include all of these:

1. No preview step.
2. Direct-apply only.
3. Selection-scoped dimensions only.
4. One named Transaction.
5. Explicit operation mode in confirmation: `replace` or `clear`.
6. Explicit warning in confirmation for replace mode:
   `标注替换会改变显示测量值，可能导致出图错误。`
7. For replace mode, show the exact replacement text in confirmation.
8. For clear mode, skip text-entry and go straight to confirmation.
9. Markdown + CSV logs with at least:
   - `element_id`
   - `category`
   - `mode`
   - `old_override`
   - `new_override`
   - `segments_count`
   - `result`
   - `message`
10. Final output must remind the user that one Revit Undo reverses the whole batch.

## Extra Implementation Note

Multi-segment dimensions are part of the required implementation scope.

Hermes must document in the delivery report:

- whether IronPython/pyRevit successfully handled `Dimension.Segments`;
- what clear behavior was used:
  - empty string;
  - or another API-compatible value.
