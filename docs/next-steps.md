# Next Steps

Current goal:

```text
Make the pyRevit MVP usable in a sandbox Revit model.
```

## Current Project Position

- Personal Revit AI assistant.
- Not a company platform.
- Not a commercial plugin.
- Not an MCP-first project.
- Current implementation focus: pyRevit.
- C# DLL stays small unless there is a concrete work need.
- Long-term target includes Revit 2022-2027 and MCP controlled read/write, but not before the personal MVP is useful.

## This Week

1. Keep the project scope simple and personal.
2. Run the offline preflight.
3. Use the sandbox checklist for the first live Revit run.
4. Capture the first real blocker with the feedback template.
5. Fix only that first blocker.
6. Do not expand feature scope until the sandbox flow works.

## Current Execution Pack

- `docs/sandbox-pyrevit-mvp-runbook.md`
- `docs/sandbox-pyrevit-mvp-checklist.md`
- `docs/sandbox-pyrevit-mvp-feedback-template.md`
- `python tools\run_sandbox_preflight.py --write-report`

## Current Validation Commands

Run from repository root:

```powershell
python tools\check_pyrevit_extension.py
python tools\run_sandbox_preflight.py --write-report
python tools\static_checks.py --write-report
```

Expected:

- `check_pyrevit_extension.py`: `0 errors`
- sandbox preflight: all steps `PASS`
- static checks: `0 errors`

## Human Sandbox Run

Use only a test model:

- file name should include `_sandbox` or `_test`;
- do not use a production model;
- stop at the first blocker;
- fill `docs/sandbox-pyrevit-mvp-feedback-template.md`.

## AI Agent Work Split

Codex:

- project direction;
- task breakdown;
- final review;
- key blocker fixes;
- Git release decisions.

Hermes / Gemini / DeepSeek:

- draft docs;
- review reports;
- checklist cleanup;
- external toolbox inventory;
- bounded code, plugin, and test drafts after Codex scopes the task.

Rules:

- use `docs/agent-development-rules.md`;
- use `docs/agent-task-template.md` for assigned work;
- use `docs/agent-delivery-report-template.md` for every delivery;
- place external packages or reports under `docs/incoming/`;
- record Codex review under `docs/reviews/`;
- do not merge external work without Codex review.

If the user works in an environment without Git or Codex, Gemini/DeepSeek may deliver zip files, folders, screenshots, and Markdown reports. Every delivery still needs a `delivery-report.md`.

## Gemini Toolbox

Gemini C# toolbox path:

```text
G:\Codex\YangAgent Revit\YangAgent Revit\Gemini 资料\YangTools_SourceCode
```

Use:

- `docs/external-toolbox-intake.md`

Do not merge the toolbox directly.

First classify every tool as:

- read-only;
- low-risk model change;
- high-risk model change;
- useful idea but poor implementation;
- not needed.

Default decision: rewrite selected useful tools in YangAgent style instead of modifying the whole Gemini toolbox in place.

## Later, Not This Week

- Revit 2022-2027 support.
- MCP automatic model reading.
- MCP controlled model modification.
- Wider C# migration.
- More daily-work plugins from the Gemini toolbox.
