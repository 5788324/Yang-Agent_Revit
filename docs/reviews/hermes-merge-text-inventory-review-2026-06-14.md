# Hermes MergeText Inventory Review - 2026-06-14

Reviewed delivery:

```text
G:\Hermes Agent\YangAgent Revit\YangAgent Revit\docs\drafts\2026-06-14_hermes_W2-004_delivery
```

Files reviewed:

- `hermes-merge-text-inventory.md`
- `delivery-report.md`
- Gemini source `Commands/MergeTextCommand.cs`
- Gemini source `UI/MergeTextWindow.xaml.cs`
- Gemini source `UI/MergeTextWindow.xaml`

## Decision

`accepted with direction correction`

Hermes got the main decision right:

- `MergeText` is not a low-risk text tool;
- it performs element deletion;
- YangAgent must not ship it as direct-apply first;
- the correct YangAgent path is `preview -> confirmation -> apply -> log -> Undo note`.

## Findings

### 1. Main conclusion is correct

Accepted:

- high-risk classification;
- preview-first requirement;
- two-button YangAgent shape;
- deletion list must be explicit in preview and apply logs.

### 2. One important implementation detail was missed

Gemini source behavior around newline separation is inconsistent with the UI label:

- `MergeTextWindow.xaml.cs` sets `UseNewlineSeparator = ChkUseNewline.IsChecked == true`
- but `MergeTextCommand.cs` uses:

```csharp
string separator = (!mergeTextWindow.UseNewlineSeparator ? "\r" : "");
```

This means:

- checkbox checked => empty separator
- checkbox unchecked => carriage return separator

So the current Gemini implementation appears inverted relative to the checkbox meaning `以换行符分隔`.

Implication for YangAgent:

- do not blindly copy Gemini behavior;
- define separator behavior explicitly in the YangAgent preview;
- preview output must show the exact merged text result before any apply is allowed.

### 3. XAML was worth reading

Hermes noted the XAML was not read, but it actually contains useful review signal:

- hard-coded colors;
- the exact Chinese labels for sort modes;
- the checkbox label confirming intended separator semantics.

This does not block acceptance of the inventory, but the next implementation package must use the XAML labels only as reference, not as architecture or styling source.

## Direction For Next Package

Next package is:

```text
HERMES-W2-005 PreviewMergeText Draft
```

Required direction:

- preview-only;
- no Transaction;
- no model write;
- no deletion;
- selection-scoped;
- explicit merged text preview;
- explicit keep element vs delete elements list;
- explicit separator behavior;
- Markdown + CSV output;
- user-visible deletion warning.

Apply is not authorized in the next package.
