# Agent Review Checklist

Use this checklist when Codex reviews work from Hermes, Gemini, DeepSeek, or any external helper.

## Intake

- Is there a task sheet?
- Is there a delivery report?
- Are all changed files listed?
- Is the source package or folder named with date, agent, topic, and version?
- Is the work inside the assigned scope?

## Safety

- Does the work touch Revit model data?
- If it modifies a model, does it follow preview / confirmation / apply / log / Undo note?
- Does it avoid production model instructions?
- Does it avoid dynamic script execution for model changes?
- Does it avoid automatic MCP model modification?
- Does it avoid installing or copying files into live Revit addin folders unless explicitly allowed?

## Code Quality

- Is the change small enough to review?
- Does it avoid broad unrelated refactors?
- Are errors explicit and useful to a beginner user?
- Are logs and output paths clear?
- Are file paths safe for Windows users?
- Does it avoid hardcoded personal paths unless documented as local-only?

## Validation

- Were repository checks run where possible?
- Were manual Revit checks clearly separated from offline checks?
- Is live Revit evidence present if the agent claims live behavior?
- Are skipped checks explained?

## Decision

Use exactly one outcome:

```text
accepted
needs changes
rejected
```

Record the reason in `docs/reviews/` and update the relevant worklog.
