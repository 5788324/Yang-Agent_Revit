# Codex / Hermes YangAgent V1 Migration Board - 2026-06-14

This document is the active task board and handoff contract for Hermes / DeepSeek work on YangAgent Revit.

## Authority

Codex owns:

- project direction;
- architecture boundaries;
- theme and design system;
- safety rules;
- task package scope;
- final review;
- merge decisions;
- live Revit validation records.

Hermes / DeepSeek only own:

- implementation drafts inside assigned task packages;
- offline inventory;
- low-risk code drafts;
- delivery reports;
- checklist cleanup;
- self-check evidence.

Hermes must not decide architecture, product naming, theme tokens, safety policy, MCP policy, or merge readiness.

## Current Repo Truth

Main repository:

```text
G:\Codex\YangAgent Revit\YangAgent Revit
```

Hermes working repository:

```text
G:\Hermes Agent\YangAgent Revit\YangAgent Revit
```

Gemini reference toolbox:

```text
G:\Codex\YangAgent Revit\YangAgent Revit\Gemini 资料\YangTools_SourceCode
```

Do not use or write to the old path:

```text
D:\codex\Yang Agent_Revit
```

Gemini restoration target:

```text
docs/governance/gemini-feature-restoration-map-2026-06-14.md
```

Gemini authoring spec:

```text
docs/governance/gemini-plugin-authoring-spec-2026-06-14.md
```

## V1 Completion Modules

V1 target: a usable personal Revit assistant that helps daily work. V1 is not the full Gemini toolbox migration.

| module | remaining tasks | status | notes |
| --- | ---: | --- | --- |
| 0. Governance and handoff | 4 | in_progress | This board, delivery log, review log, merge gates |
| 1. Theme and design system Wave 0 | 5 | in_progress | Shared theme for pyRevit, reports, and future C# WPF windows |
| 2. Current pyRevit MVP closeout | 4 | in_progress | Only blocker fixes and Git checkpoint |
| 3. Gemini text / annotation tools Wave 2 | 8 | in_progress | First TextModifier preview integrated; live preview validation pending |
| 4. Sheets / views / levels / visibility Wave 3 | 7 | planned | Higher risk; one workflow at a time |
| 5. MCP safety shell Wave 4 | 5 | planned | Read-only first; no dynamic code execution |
| 6. C# host and release skeleton | 3 | planned | Only where C# / WPF is actually needed |
| 7. V1 acceptance and release | 4 | planned | Snowdon validation, Undo, docs, Git checkpoint |

Backlog outside V1:

- broad ProjectAssetManager migration;
- family manager full migration;
- geometry generation;
- Boolean tools;
- batch task engine;
- dynamic Copilot panel;
- unrestricted MCP write server.

## Migration Rules

Gemini code is a reference source, not a mainline base.

Rules:

- Do not copy Gemini tools directly into YangAgent.
- Do not preserve Gemini architecture by default.
- Do not hard-code colors in new UI.
- New UI must use shared `theme_id` or documented theme tokens.
- pyRevit reports must use shared report helpers when applicable.
- Model-changing tools default to `impact summary -> confirmation -> apply -> log -> Undo note`.
- Do not add a separate preview step unless Codex explicitly requests it.
- High-risk tools still require stronger confirmation, clearer impact summary, and strict all-or-nothing transaction behavior.
- Apply tools must validate source CSV prefix, required fields, and duplicate `element_id`.
- No automatic deployment into live Revit Addins folders.
- No dynamic Python / generated code execution for model changes.
- No auto-start MCP write server.
- Hermes must not modify shared libs unless the task package explicitly allows it.

Current shared helpers:

- `pyrevit/YangAgent.extension/lib/yang_agent_theme.py`
- `pyrevit/YangAgent.extension/lib/yang_agent_settings.py`
- `pyrevit/YangAgent.extension/lib/yang_agent_report_style.py`
- `pyrevit/YangAgent.extension/lib/yang_agent_lang.py`
- `pyrevit/YangAgent.extension/lib/yang_agent_apply.py`
- `src/YangAgent.Revit2027/DesignSystem/YangAgentTheme.cs`

## Active Queue

Hermes is now authorized to work from a pre-approved sequential queue.
Hermes still must deliver one package at a time and stop after each delivery for Codex review.

Current execution mode:

```text
Pre-approved sequential queue
```

Queue source:

```text
docs/governance/hermes-full-execution-pack-2026-06-14.md
```

Current next package:

```text
HERMES-W3-006 ApplyVisibilityCopy Draft
```

Hermes must treat the restoration map as product truth for feature coverage and panel continuity.
Hermes must treat the authoring spec as the delivery contract for future migration-friendly implementations.

## Task Package: HERMES-W0-001 Theme Compliance Audit

Status: `accepted`

Goal:

- Audit pyRevit and C# candidate UI for hard-coded colors and theme compliance.
- This is a read-only audit. Do not edit code.

Allowed input paths:

- `G:\Codex\YangAgent Revit\YangAgent Revit\pyrevit\YangAgent.extension`
- `G:\Codex\YangAgent Revit\YangAgent Revit\src`
- `G:\Codex\YangAgent Revit\YangAgent Revit\docs\design-system`
- `G:\Codex\YangAgent Revit\YangAgent Revit\docs\governance`

Forbidden:

- Do not modify any file.
- Do not propose new theme names.
- Do not add new theme tokens.
- Do not redesign UI.
- Do not run formatters.

Audit requirements:

- Find hard-coded color literals in pyRevit scripts, XAML, C# WPF code, and report HTML.
- Separate acceptable theme definitions from improper hard-coded UI colors.
- Confirm whether each UI/report path uses one of:
  - `get_theme_id()`;
  - `get_theme_definition()`;
  - `build_intro_block()`;
  - `build_status_block()`;
  - `YangAgentTheme.Current()`;
  - a documented token wrapper.

Required output:

```text
G:\Hermes Agent\YangAgent Revit\YangAgent Revit\docs\drafts\2026-06-14_hermes_theme-compliance-audit.md
```

Output format:

- task name;
- agent name;
- date;
- scanned paths;
- findings table with file, line, issue type, severity, recommendation;
- list of false positives;
- list of files already compliant;
- skipped paths and why;
- no code changes made.

Acceptance criteria:

- Includes exact file paths and line numbers.
- Does not classify colors inside `yang_agent_theme.py` or `YangAgentTheme.cs` as violations.
- Clearly distinguishes report HTML styling through shared helper vs direct hard-coded HTML.
- Does not require Codex to infer the recommendation.

## Task Package: HERMES-W2-001 Gemini Text Tools Inventory

Status: `accepted`

Goal:

- Inventory Gemini text and annotation tools before rewrite.
- This is a read-only inventory. Do not write code.

Gemini source paths:

```text
G:\Codex\YangAgent Revit\YangAgent Revit\Gemini 资料\YangTools_SourceCode\src\YangTools.Revit\Commands
```

Tools to inspect:

- `TextModifierCommand.cs`
- `MergeTextCommand.cs`
- `AlignTextToLineCommand.cs`
- `AlignTextToTextCommand.cs`
- `DistributeTextCommand.cs`
- `DimTextOverrideCommand.cs`
- `TextNoteSelectionFilter.cs`
- `DimensionSelectionFilter.cs`

Required output:

```text
G:\Hermes Agent\YangAgent Revit\YangAgent Revit\docs\drafts\2026-06-14_hermes_text-tools-inventory.md
```

For each tool, document:

- business purpose;
- user workflow;
- UI dependency;
- input selection requirements;
- whether it changes model;
- Transaction use;
- affected element types;
- risky operations;
- whether preview exists;
- whether confirmation exists;
- whether logging exists;
- Undo expectation;
- minimum YangAgent rewrite design;
- recommended priority: P0 / P1 / P2 / defer.

Acceptance criteria:

- No code changes.
- No broad architecture proposals.
- Recommends the first text tool to rewrite.
- Explains why the first tool is the fastest daily-work payoff.

## Task Package: HERMES-W2-002 TextModifier Preview Draft

Status: `accepted with Codex integration fixes`

Goal:

- Draft the first text modifier preview-only pyRevit tool after Codex approves the inventory recommendation.

Default target unless Codex changes it:

```text
PreviewTextFindReplace.pushbutton
```

Allowed:

- Add a new preview-only pyRevit button under the YangAgent extension.
- Output Markdown and CSV to `get_export_dir()`.
- Reuse shared theme/report helpers.
- Use stable English CSV field names.

Forbidden:

- No Transaction.
- No model write.
- No apply button.
- No shared lib modifications.
- No C# work.
- No Gemini architecture copy.

Minimum preview behavior:

- Ask user for find text and replacement text.
- Scan TextNote elements in active document.
- Report candidate count.
- Output ElementId, current text, proposed text, owner view if available, and dry_run=true.
- Clearly state that no model changes were made.

Acceptance criteria:

- `python tools\check_pyrevit_extension.py` passes.
- `python tools\static_checks.py --write-report` passes or warnings are documented.
- Delivery report included.
- Codex can review without asking what changed.

Codex integration result:

- mainline button added at `pyrevit\YangAgent.extension\YangAgent.tab\Reports.panel\Reports.pulldown\PreviewTextFindReplace.pushbutton`;
- missing icon added;
- mojibake Chinese text corrected;
- case sensitivity selection changed to `CommandSwitchWindow`;
- Markdown candidate details include current and proposed text;
- replacement text is preserved exactly instead of stripped;
- no Transaction and no model-write calls.

Validation result:

- `python tools\check_pyrevit_extension.py`: `0 errors`, `0 warnings`;
- `python tools\static_checks.py --write-report`: `0 errors`, `3` pre-existing docs warnings;
- safety grep found no script model-write behavior.

## Task Package: HERMES-W2-003 TextModifier Apply Draft

Status: `assigned`

Goal:

- Build the first low-risk direct-apply text modification tool for personal use.

Default target unless Codex changes it:

```text
ApplyTextFindReplace.pushbutton
```

Business rule:

- This tool is treated as low-risk personal-use model modification.
- Preview output is useful but not mandatory before apply.
- The apply flow must be fast, explicit, and Undo-friendly.

Allowed:

- Add one apply button under the YangAgent extension.
- Read user-entered find text and replacement text directly in the button flow.
- Show impact count before commit.
- Require one explicit confirmation.
- Use one named `revit.Transaction(...)`.
- Modify only `TextNote` text values.
- Export a result Markdown or CSV log through `get_export_dir()`.
- Reuse shared language/theme/report helpers where reasonable.

Forbidden:

- No shared lib modifications unless Codex explicitly reopens scope.
- No multi-step wizard.
- No background automation.
- No external file input.
- No deletion of elements.
- No changes outside `TextNote`.
- No C# work.

Minimum apply behavior:

- Ask for find text and replacement text.
- Let the user choose case-sensitive or case-insensitive matching.
- Scan the active document and compute candidate count before opening a Transaction.
- If candidate count is `0`, stop without opening a Transaction.
- Show one confirmation dialog with:
  - document title;
  - candidate count;
  - find text;
  - replacement text;
  - Undo reminder.
- On confirm, run one named Transaction and replace matching `TextNote` text.
- Export a log/report with changed ElementIds, old text, new text, and owner view if available.
- End with a clear message that the user can use Revit Undo if needed.

Acceptance criteria:

- `python tools\check_pyrevit_extension.py` passes.
- `python tools\static_checks.py --write-report` passes or warnings are documented.
- The script contains one named Transaction only around the actual write phase.
- No write occurs before the confirmation step.
- Delivery report included.
- Hermes explicitly states known limitations, especially formatting-rich TextNote edge cases if not handled.

## Delivery Log

Hermes must append one row for every delivery.

| date | task id | delivery path | changed files | self-check | status | notes |
| --- | --- | --- | --- | --- | --- | --- |
| 2026-06-14 | HERMES-W0-001 | `docs\drafts\2026-06-14_hermes_theme-compliance-audit.md` | none | read-only audit | accepted | 0 hard-coded color violations |
| 2026-06-14 | HERMES-W2-001 | `docs\drafts\2026-06-14_hermes_text-tools-inventory.md` | none | read-only inventory | accepted | TextModifier accepted as P0 |
| 2026-06-14 | HERMES-W2-002 | `docs\drafts\2026-06-14_hermes_textmodifier-preview_delivery` | `PreviewTextFindReplace.pushbutton` | py_compile/check_pyrevit_extension reported by Hermes; mainline checks rerun by Codex | accepted | Codex integrated with fixes instead of copying verbatim |
| 2026-06-14 | HERMES-W2-003 | `docs\drafts\2026-06-14_hermes_W2-003_revision1_delivery` | `ApplyTextFindReplace.pushbutton` | py_compile/check_pyrevit_extension/static_checks reported by Hermes; mainline checks rerun by Codex | accepted | Revision 1 accepted and integrated |
| 2026-06-14 | HERMES-W2-004 | `docs\drafts\2026-06-14_hermes_W2-004_delivery` | `hermes-merge-text-inventory.md` | inventory-only; no code checks required | accepted with direction correction | MergeText confirmed deletion risk; Codex later changed execution mode to direct-apply for personal use |

## Codex Review Log

Codex appends review decisions here after reading delivery output.

| date | task id | decision | review path | required changes |
| --- | --- | --- | --- | --- |
| 2026-06-14 | HERMES-W0-001 | accepted | `docs/reviews/hermes-v1-board-deliveries-review-2026-06-14.md` | none |
| 2026-06-14 | HERMES-W2-001 | accepted | `docs/reviews/hermes-v1-board-deliveries-review-2026-06-14.md` | none |
| 2026-06-14 | HERMES-W2-002 | accepted with Codex integration fixes | `docs/reviews/hermes-textmodifier-preview-delivery-review-2026-06-14.md` | none |
| 2026-06-14 | HERMES-W2-003 | accepted with Codex integration fixes | `docs/reviews/hermes-textmodifier-apply-delivery-review-2026-06-14.md` | live sandbox apply + Undo validation |
| 2026-06-14 | HERMES-W2-004 | accepted with direction correction | `docs/reviews/hermes-merge-text-inventory-review-2026-06-14.md` | Gemini newline behavior must not be copied blindly; execution mode later changed to direct-apply by user decision |
| 2026-06-14 | HERMES-W2-005 | accepted | `docs/reviews/hermes-apply-text-merge-review-2026-06-14.md` | Revision 3 aligns to mainline transaction pattern and writes failure logs |
| 2026-06-14 | HERMES-W2-006 | accepted with implementation direction | `docs/reviews/hermes-dim-text-override-inventory-review-2026-06-14.md` | Direct-apply accepted; replace and clear stay in one button |
| 2026-06-14 | HERMES-W2-007 | accepted | `docs/reviews/hermes-apply-dim-text-override-review-2026-06-14.md` | Failure logs now populate the required `mode` field |
| 2026-06-14 | HERMES-W2-008 | accepted with implementation direction | `docs/reviews/hermes-align-distribute-inventory-review-2026-06-14.md` | DistributeText confirmed as the first align/distribute migration target |
| 2026-06-14 | HERMES-W2-009 | accepted | `docs/reviews/hermes-apply-text-distribute-review-2026-06-14.md` | Descending direction and failure-log coordinate issues fixed |
| 2026-06-14 | HERMES-W3-001 | accepted with implementation direction | `docs/reviews/hermes-wave3-inventory-review-2026-06-14.md` | SectionByLine confirmed as the first Wave 3 migration target |
| 2026-06-14 | HERMES-W3-002 | accepted | `docs/reviews/hermes-apply-section-by-line-review-2026-06-14.md` | Direct-apply section creation accepted; live sandbox validation still required after integration |
| 2026-06-14 | HERMES-W3-003 | accepted with direction correction | `docs/reviews/hermes-view-graphic-cleaner-inventory-review-2026-06-14.md` | Inventory accepted, but V1 target changed from preview+apply split to one direct-apply current-view tool |
| 2026-06-14 | HERMES-W3-004 | accepted | `docs/reviews/hermes-apply-view-graphic-clean-review-2026-06-14.md` | Active-view direct-apply override cleaning accepted; live IronPython field access still needs sandbox validation |
| 2026-06-14 | HERMES-W2-010 | needs changes | `docs/reviews/hermes-apply-align-text-to-text-review-2026-06-14.md` | Mode-selection cancel currently falls through to `left`, which can cause unintended model changes |
| 2026-06-14 | HERMES-W2-010 revision 1 | accepted | `docs/reviews/hermes-apply-align-text-to-text-revision1-review-2026-06-14.md` | Cancel path and missing-bounding-box prevalidation now stop safely before any model change |
| 2026-06-14 | HERMES-W1-001 | accepted with implementation direction | `docs/reviews/hermes-chinese-check-inventory-review-2026-06-14.md` | Audit half enters V1; delete half rejected |
| 2026-06-14 | HERMES-W1-002 | accepted | `docs/reviews/hermes-preview-chinese-content-review-2026-06-14.md` | Read-only Chinese/CJK audit preview accepted for V1 |
| 2026-06-14 | HERMES-W3-005 | accepted with implementation direction | `docs/reviews/hermes-visibility-copier-inventory-review-2026-06-14.md` | Visibility copy may proceed as direct-apply, but only with single-source single-target reduction and durable logs |

Allowed decisions:

- `accepted`
- `needs changes`
- `rejected`
- `superseded by Codex`

## Required Hermes Delivery Report Fields

Every implementation delivery must include:

- task name;
- agent name;
- date;
- source paths inspected;
- files changed;
- reason for each changed file;
- offline validation run;
- skipped validation;
- whether model changes are involved;
- whether the correct risk-tier workflow is satisfied;
- for low-risk tools: `impact summary -> confirmation -> apply -> log -> Undo note`;
- for high-risk tools: strong confirmation, named transaction, durable log, and explicit Undo note; preview is optional when the user explicitly disables it for personal-use workflows;
- known risks;
- next recommendation.

## Stop And Ask Codex

Hermes must stop and ask Codex before:

- modifying shared `lib`;
- adding settings fields;
- changing theme tokens;
- changing C# project structure;
- adding MCP server behavior;
- adding dynamic execution;
- touching Revit Addins deployment;
- implementing apply behavior;
- modifying more than one feature package in a single task.

## Current V1 Success Criteria

V1 is complete when:

- theme switching works for pyRevit settings, reports, and future C# WPF windows;
- at least one text / annotation workflow has a working live tool with confirmation, log, and Undo;
- at least one sheet / view / level / visibility workflow has a working live tool with confirmation, log, and Undo;
- MCP has a minimal read-only safety shell;
- Snowdon sandbox validation is recorded;
- Undo is validated for model-changing workflows;
- Git checkpoint is made from a reviewable state.
