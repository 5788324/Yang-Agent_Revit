# Apply Text Merge

Merge multiple TextNote elements into one. Selection-scoped direct-apply tool.

## Workflow

1. Pre-select 2+ TextNotes in Revit
2. Choose sort order and separator
3. Review impact summary (merged text preview, keep element, delete elements)
4. Confirm to execute merge + delete
5. Export result log
6. Use Revit Undo to reverse if needed

## Safety

- Selection-scoped only
- Impact summary shows exact merged text and element IDs before any changes
- All-or-nothing Transaction: any failure aborts the whole batch
- One named Transaction for full batch reversal
- Explicit delete warning in confirmation dialog
