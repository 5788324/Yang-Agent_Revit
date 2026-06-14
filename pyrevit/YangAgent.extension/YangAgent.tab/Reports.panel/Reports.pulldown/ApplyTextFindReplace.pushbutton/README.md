# Apply Text Find Replace

Find and replace text on `TextNote` elements in the active document. This is a low-risk personal-use tool.

## Workflow

1. Enter find text and replacement text.
2. Choose case sensitivity.
3. Review the impact count.
4. Confirm to apply.
5. Export the result log.
6. Use Revit Undo to reverse the batch if needed.

## Safety

- Only modifies `TextNote` elements in the active document.
- No `Transaction` is opened before confirmation.
- If 0 candidates are found, the tool stops with no changes.
- Supports Revit Undo for full batch reversal.
