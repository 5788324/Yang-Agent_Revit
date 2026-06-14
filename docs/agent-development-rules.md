# Agent Development Rules

This file is mandatory for Hermes, Gemini, DeepSeek, and any other AI or human helper working on YangAgent Revit.

The project is a personal Revit AI assistant. The current priority is a pyRevit MVP that can work in a sandbox model.

The only accepted mainline product identity is YangAgent. External toolboxes are reference sources until rewritten into YangAgent boundaries.

## Roles

| Role | Authority |
| --- | --- |
| Codex | Project direction, architecture, safety rules, final review, merge, release, and critical blocker fixes |
| Hermes / Gemini / DeepSeek | Bounded implementation, review, documentation, tests, draft plugins, and delivery reports |
| User | Real work priority, Revit feedback, sandbox evidence, and final decision on what is useful |

Non-Codex agents may write code only inside a clearly assigned task.

## Hard Rules

- Do not change project direction or roadmap unless the task explicitly asks for a draft proposal.
- Do not work without a task sheet.
- Do not claim a feature is usable without listing the exact validation environment.
- Do not modify production Revit models.
- Do not add `.rvt`, `.rfa`, customer data, secrets, local app config, or generated exports to Git.
- Do not merge, push, pull, publish, or release.
- Do not run install scripts unless the task explicitly allows it.
- Do not introduce automatic model modification as the default behavior.
- Do not use MCP, dynamic script execution, or AI-generated code execution to modify a model unless Codex has approved a specific safety design.
- Do not perform broad refactors unless the task explicitly says so.
- Do not define a new architecture, theme system, naming system, or UI grouping without Codex approval.
- Do not hardcode a new independent UI color scheme in a feature window.
- Do not copy external toolbox UI styling directly into YangAgent as-is.

## Model-Changing Tool Rule

Every model-changing feature must follow this flow:

```text
scan / preview / dry-run -> human confirmation -> apply -> log -> Undo note
```

The implementation must show:

- what will change;
- how many elements are affected;
- which model or document was used;
- what the user must confirm;
- where the output log is written;
- what to do if it fails;
- whether Revit Undo was actually tested.

If any of these are missing, the feature is not accepted.

## Required Delivery Package

Every non-Codex delivery must include a `delivery-report.md` or equivalent Markdown report with:

- task name;
- agent name;
- date;
- changed files;
- why the files changed;
- validation commands or manual checks;
- whether model changes are involved;
- whether the dry-run / confirmation / apply rule is satisfied;
- known risks;
- next-step recommendation.

If there is no delivery report, Codex treats the work as unreviewable.

Every non-Codex delivery must also include an operation log section or separate note that records:

- commands run;
- manual actions taken;
- files read before editing;
- checks not run and why.

If the helper cannot reconstruct its own actions, Codex assumes the delivery is unreliable.

## No-Git Work Environment

If the user is working in an environment without Codex or Git, agents may deliver:

- zip files;
- source folders;
- screenshots;
- Markdown reports;
- copied command output.

Use this naming pattern:

```text
YYYY-MM-DD_agent-topic_vN.zip
YYYY-MM-DD_agent-topic_delivery-report.md
```

Example:

```text
2026-06-14_gemini_titleblock-tool_v1.zip
2026-06-14_gemini_titleblock-tool_delivery-report.md
```

The user should place these files under `docs/incoming/` or provide them to Codex for intake.

## Codex Review Outcomes

Codex reviews every external delivery as one of:

| Outcome | Meaning |
| --- | --- |
| accepted | Safe to merge or continue |
| needs changes | Useful, but must be revised |
| rejected | Wrong direction, unsafe, or too costly |

Accepted work still must pass the normal repository checks before commit.

## Theme and UI Rule

All new YangAgent UI must use the shared theme engine.

Required:

- use shared theme tokens
- use YangAgent naming
- keep external rewrite UI visually subordinate to YangAgent

Forbidden:

- per-window ad-hoc color systems
- copied Gemini visual identity as a parallel product brand
