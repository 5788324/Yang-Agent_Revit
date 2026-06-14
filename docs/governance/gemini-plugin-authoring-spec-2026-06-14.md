# Gemini Plugin Authoring Spec For Future YangAgent Migration - 2026-06-14

## Purpose

This document is written for Gemini.

Goal:

- Gemini may continue to help write plugins;
- future Gemini outputs must already be structured for YangAgent migration;
- Codex remains the only architecture owner, reviewer, and merge authority.

## Authority

Gemini is not allowed to define:

- project architecture;
- theme system;
- naming system;
- MCP runtime policy;
- release policy;
- merge readiness.

Gemini is allowed to do:

- tool implementation inside an assigned task package;
- inventory and analysis;
- low-risk drafts;
- README and delivery report writing;
- offline self-checks.

## Mandatory Repo Truth

Main repository:

```text
G:\Codex\YangAgent Revit\YangAgent Revit
```

Gemini reference toolbox:

```text
G:\Codex\YangAgent Revit\YangAgent Revit\Gemini 资料\YangTools_SourceCode
```

Forbidden old path:

```text
D:\codex\Yang Agent_Revit
```

## Core Rule

Do not write code as if Gemini is building an independent product.

Write code as if the output will be absorbed into YangAgent with minimal rewrite.

That means:

- stable names;
- narrow scope;
- explicit inputs and outputs;
- no hidden runtime behavior;
- no dynamic execution;
- no hard-coded visual system;
- no giant all-in-one manager windows by default.

## Required Delivery Shape

Every Gemini task must produce one self-contained delivery folder with:

- feature folder or script folder;
- `README.md`;
- `delivery-report.md`;
- icons if required;
- any sample output schema if CSV/Markdown is generated.

Every delivery report must include:

- task id;
- date;
- goal;
- source paths inspected;
- changed files;
- model read or model write;
- risk tier;
- confirmation rule;
- logging output;
- Undo note;
- offline checks run;
- known limitations;
- whether Codex decision is needed.

## Required Tool Metadata

Every proposed tool must declare these fields:

| field | requirement |
| --- | --- |
| `tool_id` | stable English id, e.g. `yangagent.text_find_replace.apply` |
| `source_tool` | original Gemini command name if applicable |
| `target_panel` | intended YangAgent panel |
| `target_feature` | intended YangAgent feature family |
| `risk_tier` | `low_risk`, `high_risk`, or `blocked` |
| `model_access` | `read_only` / `write_text` / `write_view` / `write_family` etc. |
| `input_mode` | user input, selection, CSV, active view, current doc |
| `output_mode` | dialog, markdown, csv, report |
| `undo_expectation` | how user can undo |
| `theme_usage` | which shared theme/report helper is used |
| `lang_mode` | zh/en or machine-readable fields |

## UI And Theme Rules

Rules:

- No hard-coded color system in new UI.
- pyRevit UI/report output must reuse YangAgent shared helpers where available.
- C# WPF UI must be token-ready and separated from business logic.
- Theme selection must use `theme_id`.
- User-visible strings must support Chinese and English where the current feature family already expects it.

Current shared helpers:

- `pyrevit/YangAgent.extension/lib/yang_agent_theme.py`
- `pyrevit/YangAgent.extension/lib/yang_agent_settings.py`
- `pyrevit/YangAgent.extension/lib/yang_agent_report_style.py`
- `pyrevit/YangAgent.extension/lib/yang_agent_lang.py`
- `src/YangAgent.Revit2027/DesignSystem/YangAgentTheme.cs`

Gemini may use them.
Gemini may not redesign them without Codex approval.

## Safety And Workflow Rules

Gemini must classify every tool before writing code.

### Low-Risk Personal-Use Tools

Allowed pattern:

```text
impact summary -> confirmation -> apply -> log -> Undo note
```

Use this only when all are true:

- scope is narrow;
- target element type is explicit;
- no deletion;
- no external file ingestion;
- no broad batch document operations;
- user can reasonably inspect the impact summary immediately.

### High-Risk Tools

Required pattern:

```text
preview -> confirmation -> apply -> log -> Undo note
```

This is mandatory for:

- delete behavior;
- family operations;
- geometry creation or conversion;
- visibility propagation;
- sheet batch workflows;
- level movement;
- external input;
- multi-view or multi-document changes.

### Blocked Categories

Do not write these unless Codex explicitly reopens them:

- dynamic Python execution;
- arbitrary code execution;
- auto-start MCP write server;
- hidden background automation;
- unrestricted batch task engine;
- silent deployment into live Revit addins folders.

## pyRevit Authoring Rules

If Gemini writes a pyRevit button:

- keep IronPython 2.7 compatibility;
- no f-strings;
- no type hints;
- no walrus operator;
- encode CSV and visible text explicitly;
- use stable English machine fields;
- keep `bundle.yaml` title ASCII-safe;
- do not assume pyRevit runtime cache will refresh automatically.

Required post-change note:

- if a new `.pushbutton` is added or renamed, Codex must rebuild the pyRevit runtime cache before live click testing.

## C# Authoring Rules

If Gemini writes a C# Revit command:

- one command class per business tool;
- separate command entry, UI, and business logic;
- no automatic Revit Addins deployment in build steps;
- no background server startup in `OnStartup`;
- no hidden IPC, HTTP listener, or dynamic loader;
- keep command metadata explicit and stable.

## Logging Rules

Every write-capable tool must produce a human-readable log.

Minimum log fields:

- timestamp;
- document title;
- tool id;
- affected element ids;
- old value;
- new value;
- result;
- warning or limitation if any.

Preferred outputs:

- Markdown summary for humans;
- CSV for machine reuse when row-level results matter.

## Required Checks Before Delivery

If the delivery is pyRevit-related:

```text
python tools\check_pyrevit_extension.py
python tools\static_checks.py --write-report
```

If the delivery is C#-related:

```text
dotnet build src\YangAgent.Revit2027\YangAgent.Revit2027.csproj -v:minimal
```

## Stop And Ask Codex

Gemini must stop immediately if the task requires:

- shared lib changes;
- settings schema changes;
- new theme tokens;
- MCP behavior;
- auto deployment;
- multi-tool redesign;
- new architecture decisions;
- new background process behavior;
- changes to safety policy.
