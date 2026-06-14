# Hermes Full Execution Pack - 2026-06-14

This document is the one-shot execution contract for Hermes on YangAgent Revit V1.

Hermes does not need a new Codex prompt for every small step. Hermes should work through this queue in order, package by package, and deliver one package at a time.

Codex remains the only authority for:

- architecture;
- naming;
- theme system;
- safety rules;
- merge decisions;
- live validation closure.

## Repo Truth

Main repository:

```text
G:\Codex\YangAgent Revit\YangAgent Revit
```

Hermes working repository:

```text
G:\Hermes Agent\YangAgent Revit\YangAgent Revit
```

Gemini reference source:

```text
G:\Codex\YangAgent Revit\YangAgent Revit\Gemini 资料\YangTools_SourceCode
```

Function restoration map:

```text
docs/governance/gemini-feature-restoration-map-2026-06-14.md
```

Gemini authoring spec:

```text
docs/governance/gemini-plugin-authoring-spec-2026-06-14.md
```

Do not use:

```text
D:\codex\Yang Agent_Revit
```

## Global Rules

Hermes must obey all of these rules:

1. Do not redesign architecture.
2. Do not invent new theme tokens.
3. Do not change shared libs unless a package explicitly allows it.
4. Do not copy Gemini code directly into mainline.
5. Do not modify production Revit models.
6. Do not merge, push, pull, or publish.
7. Do not run install scripts unless the package explicitly requires it.
8. Do not add MCP write behavior or dynamic code execution.
9. Use IronPython 2.7 compatible style for pyRevit scripts.
10. Use stable English machine-readable field names.

Current execution rule for this personal-use project:

- model-changing tools default to:

```text
impact summary -> confirmation -> apply -> log -> Undo note
```

- do not add a separate preview step unless Codex explicitly asks for one.
- high-risk tools still need stronger confirmation text, clearer impact summary, and stricter all-or-nothing transaction behavior.

## Delivery Contract

Hermes must deliver exactly one package at a time.

Each delivery must include:

- changed files;
- `delivery-report.md`;
- operation log;
- checks run;
- known risks;
- explicit declaration that no production model was modified.

Each delivery folder should be created under:

```text
G:\Hermes Agent\YangAgent Revit\YangAgent Revit\docs\drafts
```

Recommended delivery folder naming:

```text
YYYY-MM-DD_hermes_<task-id>_delivery
```

## Validation Contract

For every code package, Hermes must run and report:

```powershell
python tools\check_pyrevit_extension.py
python tools\static_checks.py --write-report
```

If a package touches C#:

```powershell
dotnet build src\YangAgent.Revit2027\YangAgent.Revit2027.csproj -v:minimal
```

Hermes must not claim live Revit success.
Live Revit validation belongs to the user or Codex.

## Sequential Queue

Hermes should execute this queue in order.

| order | task id | type | priority | target | output expectation |
| --- | --- | --- | --- | --- | --- |
| 1 | HERMES-W2-004 | inventory | P0 | `MergeText*` Gemini tools | rewrite recommendation only |
| 2 | HERMES-W2-005 | code | P0 | `ApplyMergeText.pushbutton` | direct-apply merge tool with explicit delete warning |
| 3 | HERMES-W2-006 | inventory | P1 | `DimTextOverride*` Gemini tools | risk and rewrite design only |
| 4 | HERMES-W2-007 | code | P1 | `ApplyDimTextOverride.pushbutton` or equivalent | direct-apply dim text override with confirmation |
| 5 | HERMES-W2-008 | inventory | P1 | `AlignText*` and `DistributeText*` Gemini tools | rewrite recommendation only |
| 6 | HERMES-W2-009 | code | P1 | one bounded align/distribute tool | selection-scoped text layout workflow |
| 7 | HERMES-W3-001 | inventory | P1 | sheets/views/levels/visibility Gemini tools | migration map only |
| 8 | HERMES-W3-002 | code | P1 | one view/sheet naming or placement utility | one bounded workflow |
| 9 | HERMES-W0-002 | audit | P1 | theme usage gaps after new buttons | read-only compliance audit |
| 10 | HERMES-W4-001 | design | P2 | MCP safety shell | design doc only, no live write server |
| 11 | HERMES-W6-001 | audit | P2 | C# host skeleton gaps | read-only release-host audit |

Hermes may continue from one row to the next without asking for a new prompt, but only after completing the current delivery package.

## Package Details

## HERMES-W2-003

Goal:

- Build the first low-risk direct-apply text replacement tool.

Target:

```text
pyrevit\YangAgent.extension\YangAgent.tab\Reports.panel\Reports.pulldown\ApplyTextFindReplace.pushbutton
```

Rules:

- ask for find text;
- ask for replacement text;
- ask for case sensitivity;
- compute candidate count before Transaction;
- if `0`, stop;
- show one confirmation;
- run one named Transaction;
- change only `TextNote`;
- export a result log;
- remind the user about Revit Undo.

Forbidden:

- no external CSV input;
- no shared lib edits;
- no deletion;
- no multi-document behavior.

## HERMES-W2-004

Goal:

- Inventory MergeText-related Gemini tools and propose the smallest YangAgent rewrite.
- The proposal must align with `docs/governance/gemini-feature-restoration-map-2026-06-14.md`.

Output:

- one Markdown inventory doc;
- no code.

Must cover:

- business purpose;
- whether it changes model;
- selection pattern;
- Transaction pattern;
- safe low-risk subset that can be rewritten first.

## HERMES-W2-005

Goal:

- Build the direct-apply merge tool after W2-004.
- Keep user-facing naming recognisable against the Gemini `文本工具区`.

Scope:

- direct-apply only;
- one named Transaction around the actual write/delete phase;
- selection-scoped;
- explicit impact summary before confirmation;
- explicit keep/delete element roles in confirmation and logs;
- show separator behavior explicitly;
- output Markdown + CSV.

Mandatory warning:

- `MergeText` deletes elements.
- The confirmation and final log must state this clearly.
- The final output must explicitly remind the user that Revit Undo can revert the whole Transaction.

## HERMES-W2-006

Goal:

- Inventory dimension text override tools.

Output:

- one Markdown risk inventory;
- no code.

Must identify:

- whether the behavior is annotation-only or can mislead production documentation;
- whether a direct-apply personal-use version is acceptable.

## HERMES-W2-008

Goal:

- Inventory `AlignTextToText`, `AlignTextToLine`, and `DistributeText` for bounded YangAgent rewrite.

Output:

- one Markdown inventory doc;
- no code.

Must cover:

- selection pattern;
- whether direct-apply is acceptable;
- whether one shared selection helper is likely needed;
- the safest first candidate among the three tools.

## HERMES-W2-009

Goal:

- Build one bounded align or distribute text tool after W2-008.

Rules:

- selection-scoped only;
- explicit impact count;
- one confirmation;
- one Transaction only around writes;
- export a result log;
- explain Undo.

## HERMES-W2-007

Goal:

- Build one bounded dimension text override tool if W2-006 shows a safe subset.

Rules:

- selection-scoped if possible;
- explicit impact count;
- one confirmation;
- one Transaction;
- write result log;
- explain Undo.

## HERMES-W3-001

Goal:

- Inventory Gemini tools for sheets, views, levels, and visibility.

Output:

- one migration map;
- no code.

Must rank:

- fastest daily-work payoff;
- lowest migration risk;
- whether preview-first is required.

## HERMES-W3-002

Goal:

- Build one bounded sheet/view/level workflow after W3-001.

Preferred direction:

- one naming, placement, or visibility cleanup with narrow scope.

## HERMES-W0-002

Goal:

- Re-audit theme compliance after new text tools land.

Output:

- one read-only audit;
- list only real remaining gaps.

## HERMES-W4-001

Goal:

- Write the MCP safety-shell design package only.

Output:

- one design doc;
- no code that opens a write-capable MCP server.

Must define:

- read-only first;
- explicit trust boundary;
- no arbitrary code execution;
- future write path gate.

## HERMES-W6-001

Goal:

- Audit the C# host skeleton only where it helps future WPF or release packaging.

Output:

- one audit doc;
- no project-wide refactor.

## Stop Conditions

Hermes must stop and ask Codex if any of these happen:

- shared lib edits are required;
- task scope expands beyond one feature package;
- the tool needs new settings fields;
- the tool needs MCP behavior;
- the tool appears destructive;
- the tool needs preview-first instead of low-risk direct-apply;
- the tool touches elements beyond the package scope;
- offline checks fail and the fix would require architecture changes.

## Hermes Response Format

For every delivery, Hermes should reply with:

1. task id
2. delivery path
3. changed files
4. checks run
5. model safety summary
6. known risks
7. exact questions for Codex, if blocked

## Direct Prompt For Hermes

Use this exact prompt when launching Hermes:

```text
Continue YangAgent Revit work from:
G:\Codex\YangAgent Revit\YangAgent Revit

Reply in Chinese.

You are not the architect. Codex owns architecture, naming, theme, safety, merge, and live validation.

Read and follow these files first:
1. docs/governance/codex-hermes-v1-migration-board-2026-06-14.md
2. docs/governance/hermes-full-execution-pack-2026-06-14.md
3. docs/governance/gemini-feature-restoration-map-2026-06-14.md
4. docs/governance/gemini-plugin-authoring-spec-2026-06-14.md
5. docs/agent-task-template.md
6. docs/agent-delivery-report-template.md

Then execute the sequential queue without asking for a new prompt each time.
Work on one package at a time.
After each package, stop and deliver a folder under:
G:\Hermes Agent\YangAgent Revit\YangAgent Revit\docs\drafts

Do not merge, push, pull, publish, or touch a production model.
Do not modify shared libs unless the current package explicitly allows it.
Do not copy Gemini code directly.
Do not claim live Revit success.

Start with HERMES-W2-005 after reading the Codex review for HERMES-W2-004.
```
