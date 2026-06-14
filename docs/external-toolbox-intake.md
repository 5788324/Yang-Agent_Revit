# External Toolbox Intake

Use this file for the Gemini C# toolbox and any future external Revit plugin/toolbox source.

The toolbox may contain useful work tools, but it must be reviewed before any code is moved into YangAgent Revit.

Current known Gemini toolbox path:

```text
G:\Codex\YangAgent Revit\YangAgent Revit\Gemini 资料\YangTools_SourceCode
```

This source is a local external asset. Do not merge it directly.

Primary governance artifacts:

- `docs/governance/tool-registry.md`
- `docs/governance/rewrite-spec-template.md`
- `docs/governance/acceptance-gate-template.md`
- `docs/governance/delegation-pack-template.md`

## Intake Steps

1. Record the local path.
2. Identify project type:
   - C# Revit addin;
   - pyRevit extension;
   - loose scripts;
   - mixed project.
3. Identify target Revit versions.
4. List every command/button/tool.
5. Classify each tool by value and model-change risk.
6. Decide whether to keep, rewrite, defer, or discard.
7. Register the tool status in `docs/governance/tool-registry.md`.
8. Create a rewrite spec before any implementation starts.
9. Create a delivery report under `docs/incoming/` or provide one with the source package.
10. Codex records the review under `docs/reviews/`.

## Tool Classification

| Class | Meaning | Action |
| --- | --- | --- |
| A | Read-only and useful | Candidate for early rewrite or direct reference |
| B | Low-risk model change, useful | Rewrite with preview / confirm / apply |
| C | High-risk model change | Defer until safety design exists |
| D | Good idea, poor implementation | Keep idea, discard code |
| X | Unsafe, not useful, or too costly | Discard |

## Review Fields

For each tool, record:

- tool name;
- purpose;
- Revit version target;
- read-only or model-changing;
- transaction use;
- human confirmation;
- dry-run or preview support;
- logging;
- Undo expectation;
- known bugs;
- migration recommendation.

## Safety Rule

No Gemini toolbox command is merged directly into the mainline.

Model-changing tools must be adapted to:

```text
preview / dry-run -> human confirmation -> apply -> log -> Undo check
```

Do not preserve risky architecture by default:

- no automatic MCP write access;
- no dynamic Python or generated code execution for model changes;
- no automatic deployment into live Revit Addins folders;
- no production model testing;
- no broad C# framework migration before a concrete work tool needs it.

The default recommendation is to rewrite selected useful tools in YangAgent style instead of modifying the whole external toolbox in place.

## Current Status

Gemini C# toolbox path has been provided. Initial inspection shows it should be treated as a reference toolbox, not a mainline base.

Next intake step:

1. Inventory all commands/buttons.
2. Classify each tool as A/B/C/D/X.
3. Select the top one to three personal work tools.
4. Rebuild selected tools safely in YangAgent.
