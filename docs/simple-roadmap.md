# YangAgent Revit Simple Roadmap

## Phase 1: Sandbox Usable pyRevit MVP

Target: about one week, if a real sandbox Revit run is available.

Success means:

- pyRevit extension loads;
- report and preview buttons run in a sandbox model;
- exported files can be read by AI;
- the first live blocker is captured and fixed;
- apply tools remain limited to low-risk confirmed changes.

Do not add new major feature areas before this phase is stable.

## Phase 2: Personal Daily-Use MVP

Target: about one month, depending on live feedback.

Success means:

- the assistant helps with real daily Revit checks;
- the user can ask AI to interpret generated reports;
- a small number of useful Gemini toolbox features are selected and repaired or rewritten;
- common workflows such as title blocks, levels, sheets, views, rooms, and marks have clear safe paths.

## Phase 3: Revit 2022-2027 Support

Target: after the personal MVP is useful.

Strategy:

- pyRevit is the preferred multi-version route first;
- C# DLL support is split by Revit version;
- no version is claimed supported until it is tested in a real Revit install;
- current C# DLL implementation remains Revit 2027 only until there is a concrete test need.

## Phase 4: MCP Reading And Controlled Modification

Target: after the plugin/report workflow is stable.

MCP should start with automatic reading:

- read exported JSON/CSV/Markdown;
- explain model status;
- suggest which tool to run next.

MCP model modification must remain controlled:

- `mcp_preview_*`;
- human confirmation;
- `mcp_apply_*`;
- Revit transaction;
- log output;
- Undo check in sandbox.

MCP must not execute arbitrary Python or C# against a model.

## Current One-Week Focus

Only this is the active sprint goal:

```text
pyRevit MVP usable in a sandbox model
```
