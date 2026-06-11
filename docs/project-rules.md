# YangAgent Revit Project Rules

## Product Rule

Build a personal Revit AI assistant first.

Do not add architecture or process just because it looks complete. Add it only when it helps YANG work in Revit.

## Safety Rule

Never modify a production Revit model directly during development.

Model-changing tools must follow:

```text
preview / dry-run -> human confirmation -> apply -> log -> Undo check
```

## Scope Rule

Current mainline:

- pyRevit MVP;
- sandbox run;
- AI-readable reports;
- low-risk confirmed apply tools;
- Gemini toolbox intake after the user provides the path.

Not current mainline:

- enterprise rollout;
- commercial packaging;
- all-version C# DLL support;
- MCP write-to-model automation;
- large platform architecture.

## Revit Version Rule

Long-term target: Revit 2022-2027.

Current implementation:

- pyRevit is the preferred multi-version path;
- C# DLL is implemented only for Revit 2027;
- each C# Revit version needs its own project and real testing.

## AI Agent Rule

Codex owns:

- project direction;
- task breakdown;
- quality review;
- key blocker fixes;
- final merge decisions.

Hermes, Gemini, and DeepSeek may help with:

- code reading;
- documentation;
- checklists;
- draft reports;
- low-risk candidate patches;
- external toolbox inventory.

They do not independently decide model-changing behavior.

## Gemini Toolbox Rule

The Gemini C# toolbox is treated as an external asset first.

Do not merge it directly.

First classify each tool by risk and value, then decide whether to keep, rewrite, or discard it.
