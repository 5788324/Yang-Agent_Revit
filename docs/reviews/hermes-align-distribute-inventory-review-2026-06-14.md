# Hermes Align / Distribute Inventory Review - 2026-06-14

Reviewed delivery:

```text
G:\Hermes Agent\YangAgent Revit\YangAgent Revit\docs\drafts\2026-06-14_hermes_W2-008_delivery
```

## Decision

`accepted with implementation direction`

## Codex Decision

Migration order is accepted as:

1. `DistributeText`
2. `AlignTextToText`
3. `AlignTextToLine`

## Reason

`DistributeText` is the best next migration target because:

- it only uses `MoveElement`;
- it does not need rotation math;
- it has strong daily-use value;
- it fits the current no-preview direct-apply rule cleanly;
- it does not depend on `PickPoint`.

`AlignTextToText` stays second because it is still practical, but it adds source/target selection complexity and rotation logic.

`AlignTextToLine` should stay last or deferred because the `PickPoint` interaction is the worst fit for the current pyRevit migration path.

## Required Direction For Next Package

Next package:

```text
HERMES-W2-009 ApplyTextDistribute Draft
```

Must include:

- no preview;
- direct-apply;
- selection-scoped only;
- one named Transaction;
- explicit impact summary before confirmation;
- Markdown + CSV logs with old/new coordinates and deltas;
- Undo reminder.
