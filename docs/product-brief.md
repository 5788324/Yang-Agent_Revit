# YangAgent Revit Product Brief

## One Sentence

YangAgent Revit is a personal Revit AI assistant that helps YANG inspect models, generate reports, understand issues, and apply low-risk fixes only after human confirmation.

## Current Goal

The current goal is not a company platform, commercial plugin, or full automation system.

The current goal is:

- help one user work faster in Revit;
- make model information easy for AI to read;
- find common problems in rooms, doors, windows, views, sheets, title blocks, levels, and parameters;
- guide the user through safe next steps;
- apply only low-risk model changes through `preview/dry-run -> human confirmation -> apply -> log -> Undo check`.

## What The Assistant Does First

1. Export model information to JSON, CSV, and Markdown.
2. Generate human-readable health reports and AI prompts.
3. Preview common problems before any model change.
4. Let the user review proposed changes.
5. Apply only confirmed low-risk changes in a sandbox/test model first.

## What Is Delayed

These are valid future directions, but not the current one-week delivery target:

- enterprise deployment;
- commercial packaging;
- permission systems;
- full C# rewrite;
- full Revit 2022-2027 C# support;
- MCP-driven automatic model modification;
- arbitrary Python or C# execution from an AI agent.

## Long-Term Direction

Long term, the assistant may support:

- Revit 2022-2027, with pyRevit as the first multi-version route;
- selected tools from the Gemini C# toolbox after isolation review;
- MCP automatic model reading;
- MCP controlled model modification through preview/apply tools only.

## Non-Negotiable Safety Rule

No production model should be modified directly by an unverified tool.

All model-changing workflows must follow:

```text
preview / dry-run -> human confirmation -> apply -> log -> Undo check
```
