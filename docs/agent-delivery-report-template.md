# Agent Delivery Report Template

Every Hermes, Gemini, DeepSeek, or external helper delivery must include this information.

## Summary

- Task name:
- Agent:
- Date:
- Delivery version:
- Source package or folder:

## Changed Files

List every changed, added, deleted, or generated file.

| File | Change | Reason |
| --- | --- | --- |
|  |  |  |

## Checks Run

| Check | Command or action | Result |
| --- | --- | --- |
|  |  |  |

If a required check was not run, explain why.

## Model Safety

- Does this work read a Revit model?
- Does this work modify a Revit model?
- Was a production model touched?
- Was a sandbox model used?
- Does the feature have preview or dry-run?
- Does the feature require human confirmation before apply?
- Does it write a log?
- Does it explain Revit Undo?

## Implementation Notes

Explain what changed and why.

## Known Risks

List bugs, unverified behavior, fragile assumptions, and missing tests.

## Questions For Codex

Only ask questions that block review or next implementation.

## Agent Declaration

Confirm:

```text
I did not merge, push, pull, publish, or modify a production Revit model.
```
