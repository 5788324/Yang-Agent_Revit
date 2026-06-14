# Apply Text Distribute

Evenly distribute TextNote elements along X or Y axis with specified spacing. Selection-scoped direct-apply tool.

## Workflow

1. Pre-select 2+ TextNotes in Revit
2. Choose sort order, distribution direction, spacing, and alignment
3. Review impact summary
4. Confirm to apply
5. Export result log with coordinate deltas
6. Use Revit Undo to reverse if needed

## Safety

- Selection-scoped only
- Position-only changes (MoveElement)
- No text content modification
- No element deletion
- One named Transaction for full batch reversal
