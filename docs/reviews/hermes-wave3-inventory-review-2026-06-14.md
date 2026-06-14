# Hermes Wave 3 Inventory Review - 2026-06-14

Reviewed delivery:

```text
G:\Hermes Agent\YangAgent Revit\YangAgent Revit\docs\drafts\2026-06-14_hermes_W3-001_delivery
```

## Decision

`accepted with implementation direction`

## Codex Decision

Current Wave 3 order is:

1. `SectionByLine`
2. `ViewGraphicCleaner` after deeper logic read
3. `SheetManager` deferred
4. `VisibilityCopier` deferred
5. `LevelModifier` deferred

## Why

### 1. `SectionByLine` can enter V1

Accepted:

- single-element scope;
- one explicit selected line;
- one created section view;
- transaction boundary is simple;
- logging and confirmation can be made explicit in pyRevit.

This fits the current no-preview direct-apply rule better than the other Wave 3 tools.

### 2. `ViewGraphicCleaner` is still under-read

The current command file only shows a window launch.
That is not enough to approve implementation order ahead of `SectionByLine`.

So:

- it stays behind `SectionByLine`;
- if Hermes later wants to promote it, Hermes must first inspect the underlying window logic, not just the command entrypoint.

### 3. `VisibilityCopier` should stay deferred

Accepted:

- cross-view propagation is wider in scope;
- wrong target selection can spread mistakes;
- it is a poor fit for the current no-preview simplification rule.

### 4. `LevelModifier` should stay deferred

Accepted:

- family-instance fallback path includes recreate/delete behavior;
- this is much riskier than a plain parameter write;
- not suitable for current fast V1 direct-apply priority.

### 5. `SheetManager` should stay deferred

Accepted:

- giant manager window shape is not a good V1 migration unit;
- it should be decomposed into smaller workflows later.

## Next Package

```text
HERMES-W3-002 ApplySectionByLine Draft
```

## Mandatory Requirements For HERMES-W3-002

- no preview;
- direct-apply;
- one selected line only;
- explicit confirmation before creating the section;
- confirmation must include:
  - document title;
  - selected line element id;
  - line length;
  - active view name;
  - warning that a new section view will be created;
- one named Transaction;
- Markdown + CSV logs with at least:
  - source_element_id
  - source_view
  - line_length
  - created_view_id
  - created_view_name
  - result
  - message
- final output must include Undo reminder.
