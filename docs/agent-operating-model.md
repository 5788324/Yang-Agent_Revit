# Agent Operating Model

## Purpose

This file defines how Codex, Hermes, Gemini, DeepSeek, and the user work together on YangAgent Revit.

The goal is speed with quality control.

## Codex

Codex is the project manager and technical owner.

Codex owns:

- current priorities;
- task packs for other agents;
- safety rules;
- theme engine and design system;
- external toolbox rewrite boundaries;
- final review;
- key implementation when a blocker is risky or unclear;
- Git commit and release decisions.

Codex should avoid spending time on bulk documentation or mechanical review when another agent can do it safely.

## Hermes / Gemini / DeepSeek

These agents are treated as controlled external development models.

They may do:

- read code;
- write draft documentation;
- prepare review reports;
- classify issues;
- write bounded code or plugin drafts from a Codex-approved task sheet;
- propose low-risk patches inside the assigned scope;
- organize checklists;
- inspect external toolboxes.

They must not independently:

- change production model logic;
- approve model-changing behavior;
- claim live Revit behavior without evidence;
- merge or push;
- expand project scope.

They must follow:

- `docs/agent-development-rules.md`
- `docs/agent-task-template.md`
- `docs/agent-delivery-report-template.md`
- `docs/agent-review-checklist.md`
- `docs/daily-agent-log-template.md`

If they deliver work without a task sheet and delivery report, Codex treats it as unreviewable.

They must also leave an operation log for every task so Codex can audit what was actually done instead of only reading the final summary.

## User

The user provides:

- real Revit context;
- sandbox run feedback;
- Gemini toolbox path;
- judgment about which tools are useful for actual work.

The user does not need to understand all implementation details.

## Review Flow

1. Codex writes a bounded task.
2. Auxiliary agent completes the task in a draft, source package, or candidate patch.
3. Auxiliary agent provides a delivery report.
4. Codex reviews and marks the result as `accepted`, `needs changes`, or `rejected`.
5. Only accepted work becomes part of the mainline.

When the user works without Git or Codex, the agent may deliver a zip, folder, screenshot, or Markdown report. The delivery must still include a `delivery-report.md` and a date / agent / topic / version name.

## Review Records

Use `docs/incoming/` for external deliveries and `docs/reviews/` for Codex review records.

Use `docs/agent-review-checklist.md` before accepting any external work.

Use the current day worklog and the daily ops routine to keep handoff context live:

- `docs/worklogs/worklog-YYYY-MM-DD.md`
- `docs/next-steps.md`
- `docs/new-chat-startup-YYYY-MM-DD.md`
- `docs/framework/daily-ops-routine.md`

## Live Revit Rule

No agent can replace real Revit sandbox validation.

If a behavior depends on Revit UI, Revit transactions, Undo, loaded addins, or project model state, it remains unverified until a live sandbox run confirms it.
