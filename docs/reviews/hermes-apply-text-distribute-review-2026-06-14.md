# Hermes Apply Text Distribute Review - 2026-06-14

Reviewed delivery:

```text
G:\Hermes Agent\YangAgent Revit\YangAgent Revit\docs\drafts\2026-06-14_hermes_W2-009_delivery
```

Files reviewed:

- `ApplyTextDistribute.pushbutton/script.py`
- `ApplyTextDistribute.pushbutton/bundle.yaml`
- `ApplyTextDistribute.pushbutton/README.md`
- `delivery-report.md`

## Decision

`accepted`

## What Is Already Correct

The overall migration direction is correct:

- direct-apply;
- selection-scoped only;
- one named Transaction;
- no text modification;
- no deletion;
- confirmation includes count, sort, direction, spacing, and alignment;
- Markdown + CSV logs exist;
- Undo reminder exists.

## Revision Follow-up

The initial delivery had one main behavioral bug.

### Descending distribution modes were implemented with the wrong direction sign

File:

```text
ApplyTextDistribute.pushbutton/script.py
```

Relevant lines:

- target coordinate computation: `335-349`

Problem:

- after sorting, the script always computes:

```python
new_x = base_x + spacing_feet * i
new_y = base_y + spacing_feet * i
```

depending on axis.

That means:

- `x_desc` still distributes to increasing X;
- `y_desc` still distributes to increasing Y.

So the resulting layout contradicts the chosen sort mode.  
Example:

- if the user chooses `x_desc`, they expect right-to-left spacing;
- current code starts from the first item and moves subsequent items further right.

This is a real behavioral bug, not a polish issue.

Accepted fix:

- the revised script now computes:
  - `step_sign = -1` for `x_desc` and `y_desc`
  - positive sign for the other modes
- target coordinates now move in the expected descending direction.

### Failure logs now preserve intended target coordinates

Current failure path writes:

- `new_x = 0.0`
- `new_y = 0.0`
- `delta_x = 0.0`
- `delta_y = 0.0`

This loses the intended move target and makes failure diagnosis weaker.

Accepted fix:

- rollback failure rows now keep intended `new_x/new_y` and intended deltas instead of zeroing them out.
