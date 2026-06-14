# Apply Dim Text Override

Replace or clear displayed text on dimension elements. Selection-scoped direct-apply tool.

## Workflow

1. Pre-select dimensions in Revit
2. Choose mode: replace or clear
3. If replace: enter the replacement text
4. Review impact summary + explicit documentation warning
5. Confirm to apply
6. Export result log
7. Use Revit Undo to reverse if needed

## Safety

- Selection-scoped only
- Replace mode shows explicit warning about documentation accuracy
- Clear mode restores original measured values
- One named Transaction for full batch reversal
- Handles both single and multi-segment dimensions
