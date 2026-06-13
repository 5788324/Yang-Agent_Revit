# Agent Task Template

Copy this file when assigning work to Hermes, Gemini, DeepSeek, or another helper.

## Task

- Task name:
- Assigned agent:
- Date:
- Requested by:
- Priority:

## Goal

Write the exact result needed.

## Allowed Work

- Allowed paths:
- Allowed file types:
- Allowed commands:
- Allowed Revit version, if any:

## Forbidden Work

- Do not change project scope.
- Do not modify production Revit models.
- Do not merge, push, pull, or publish.
- Do not run install scripts unless explicitly allowed here.
- Do not use dynamic code execution to modify a Revit model.
- Do not edit files outside the allowed paths.

## Required Behavior

For model-changing features, the result must follow:

```text
scan / preview / dry-run -> human confirmation -> apply -> log -> Undo note
```

If this task is read-only, state that clearly.

## Deliverables

- Files or folders to deliver:
- Required report file:
- Required screenshots or logs:

## Validation

The agent must record:

- commands run;
- manual checks performed;
- commands not run and why;
- whether live Revit was used;
- whether only a sandbox model was used.

## Report Format

The final response must include:

- Changed files
- Checks run
- Review or implementation summary
- Safety confirmation
- Known risks
- Questions for Codex
