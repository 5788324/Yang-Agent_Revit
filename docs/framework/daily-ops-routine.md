# Daily Ops Routine

This file defines the mandatory daily start and end routine for the active YangAgent Revit repository.

Active repository:

```text
G:\Codex\YangAgent Revit\YangAgent Revit
```

## Why This Exists

The project depends on long-running multi-chat and multi-agent work.

If the core docs, Git state, and handoff notes drift, the next chat loses time and the next agent starts with the wrong assumptions.

## Core Daily Documents

These are the mandatory daily-maintained files:

- `docs/worklogs/worklog-YYYY-MM-DD.md`
- `docs/next-steps.md`
- `docs/new-chat-startup-YYYY-MM-DD.md`

These are the supporting governance files that must stay aligned when the workflow changes:

- `docs/agent-development-rules.md`
- `docs/agent-task-template.md`
- `docs/agent-delivery-report-template.md`
- `docs/agent-review-checklist.md`
- `docs/agent-operating-model.md`

## Start Of Day

Run from repository root:

```powershell
git status --short --branch
git log -3 --oneline
```

If the worktree is clean, pull first:

```powershell
git pull
```

If the worktree is dirty:

- do not pull blindly;
- first inspect what is already in progress;
- record the reason in the current worklog;
- only pull after the tree is safe.

Then read and refresh:

1. `docs/new-chat-startup-YYYY-MM-DD.md`
2. `docs/next-steps.md`
3. the current `docs/worklogs/worklog-YYYY-MM-DD.md`
4. any active task or review doc related to today’s work

## During The Day

Every meaningful implementation or review step must leave a trace in documentation.

Minimum:

- update the current day worklog;
- record blocker, decision, or scope change when it happens;
- update `docs/next-steps.md` if priorities or the validation path changed;
- update the startup handoff file if a new chat would otherwise miss key context.

## End Of Day

Before ending the day or handing off to a new chat:

1. update the current `worklog`;
2. update `next-steps`;
3. update the current `new-chat-startup` prompt;
4. check `git status --short --branch`;
5. stage/commit/push if the day reached a stable checkpoint and the user wants backup or handoff safety.

Preferred rule:

- start of day: pull when safe;
- end of day: push when the checkpoint is real and reviewable.

## Agent Logging Rule

Every external helper agent must provide an operation log for each task.

Minimum required fields:

- task name
- date
- changed files
- commands run
- manual checks
- skipped checks
- current risks
- questions back to Codex

If an agent cannot provide this log, the delivery is treated as unreviewable draft material.

## Document Cleanup Rule

Not every doc is core, but every retained doc must have a reason to exist.

Rules:

- do not keep duplicated guidance with different conclusions;
- archive or delete stale drafts only after reading them once and confirming they are superseded;
- keep core docs short and current;
- put one-off evidence into worklogs, reviews, or `docs/incoming/`, not into permanent project rules.

## Current Practical Rule

For this project, the fastest safe handoff set is:

- current worklog
- current next steps
- current new chat startup prompt
- active review/task docs for unfinished work

If these four are current, a new chat can resume with minimal waste.
