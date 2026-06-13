# YangAgent Revit

YangAgent Revit is a personal Revit AI assistant project.

The goal is simple: help YANG inspect Revit models, generate AI-readable reports, understand problems, and apply only low-risk fixes after human confirmation.

This is not a company platform, commercial plugin, or enterprise deployment system.

## Current Authority Order

When documents conflict, use this order:

1. `docs/product-brief.md`
2. `docs/simple-roadmap.md`
3. `docs/project-rules.md`
4. `docs/handoff-new-chat-2026-06-07.md`
5. `docs/next-steps.md`
6. latest relevant worklog under `docs/worklogs/`

Older architecture, MCP, Bridge, company, and commercial planning documents are historical reference only unless a current authority document points to them.

## Current Focus

This week focuses on one result:

```text
pyRevit MVP usable in a sandbox model
```

That means:

- the pyRevit toolbox loads;
- report and preview buttons run in a sandbox model;
- exported JSON/CSV/Markdown can be read by AI;
- model-changing tools use `preview/dry-run -> human confirmation -> apply -> log -> Undo check`;
- the first real sandbox blocker is captured and fixed.

## Current Tools

- `System Settings`
- `Report Export Path`
- `Export Model Snapshot`
- `Model Health Report`
- `Export Regression Checklist`
- `Export AI Review Prompt`
- `Preview Missing Marks`
- `Preview Missing Room Numbers`
- `Preview Duplicate Room Numbers`
- `Preview Unplaced Views`
- `Preview View Naming Rules`
- `Apply Missing Door Window Marks`
- `Apply Missing Room Numbers`

The toolbox supports Chinese and English.

## Core Documents

- [Product brief](docs/product-brief.md)
- [Simple roadmap](docs/simple-roadmap.md)
- [Project rules](docs/project-rules.md)
- [Agent operating model](docs/agent-operating-model.md)
- [Agent development rules](docs/agent-development-rules.md)
- [Agent task template](docs/agent-task-template.md)
- [Agent delivery report template](docs/agent-delivery-report-template.md)
- [Agent review checklist](docs/agent-review-checklist.md)
- [External toolbox intake](docs/external-toolbox-intake.md)
- [Sandbox checklist](docs/sandbox-pyrevit-mvp-checklist.md)
- [Sandbox feedback template](docs/sandbox-pyrevit-mvp-feedback-template.md)
- [Current handoff](docs/handoff-new-chat-2026-06-07.md)
- [New chat startup](docs/new-chat-startup-2026-06-13.md)
- [Next steps](docs/next-steps.md)

## Install pyRevit Toolbox

```powershell
.\scripts\install-pyrevit-extension.ps1
```

If Revit loads stale buttons or cache errors, close Revit first, then run:

```powershell
.\scripts\install-pyrevit-extension.ps1 -Force -ClearCache
```

## Offline Preflight

Run before a live sandbox session:

```powershell
python tools\check_pyrevit_extension.py
python tools\run_sandbox_preflight.py --write-report
python tools\static_checks.py --write-report
```

Expected current status:

- pyRevit preflight: `0 errors`
- sandbox preflight: `7/7 PASS`
- static checks: `0 errors`, known historical warnings only

## Longer-Term Direction

Long-term goals are still allowed, but they are not this week's delivery target:

- Revit 2022-2027 support;
- Gemini C# toolbox intake and selected migration;
- MCP automatic model reading;
- MCP controlled model modification through preview/apply only.

The project should grow only from real work needs.
