# External Toolbox Intake

Use this file when YANG provides the Gemini C# toolbox path.

The toolbox may contain useful work tools, but it must be reviewed before any code is moved into YangAgent Revit.

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

## Tool Classification

| Class | Meaning | Action |
| --- | --- | --- |
| A | Read-only and useful | Candidate for early reference |
| B | Low-risk model change, useful | Rewrite or repair with preview/confirm/apply |
| C | High-risk model change | Defer until safety design exists |
| D | Good idea, poor implementation | Keep idea, discard code |
| X | Not useful for current personal workflow | Discard |

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

## Current Status

Waiting for YANG to provide the Gemini toolbox path.
