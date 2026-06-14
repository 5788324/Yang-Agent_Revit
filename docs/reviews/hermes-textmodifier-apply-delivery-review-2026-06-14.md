# Hermes TextModifier Apply Delivery Review - 2026-06-14

## Delivery Reviewed

Hermes revision package:

```text
G:\Hermes Agent\YangAgent Revit\YangAgent Revit\docs\drafts\2026-06-14_hermes_W2-003_revision1_delivery
```

Files reviewed:

- `delivery-report.md`
- `ApplyTextFindReplace.pushbutton\bundle.yaml`
- `ApplyTextFindReplace.pushbutton\script.py`
- `ApplyTextFindReplace.pushbutton\README.md`
- `ApplyTextFindReplace.pushbutton\icon.png`

## Decision

`accepted with Codex integration fixes`

This revision fixed the prior blocking issues:

- button `title` is now ASCII, reducing pyRevit runtime registration risk;
- `script.py` uses a stable `cancel_button` key instead of the fragile string replacement hack;
- Markdown logs now include `old_text` and `new_text`;
- README was rewritten to avoid encoding ambiguity.

PowerShell console output still displayed mojibake in some reads, but direct UTF-8 verification confirmed the file contents are correct.

## Codex Integration Changes

Integrated mainline button:

```text
pyrevit\YangAgent.extension\YangAgent.tab\Reports.panel\Reports.pulldown\ApplyTextFindReplace.pushbutton
```

Codex integration choices:

- kept the ASCII title from Hermes;
- preserved the low-risk direct-apply flow;
- localized empty replacement text through a dedicated `empty` text key;
- kept the log fields aligned with the accepted review contract;
- reused the existing preview icon as the placeholder icon.

## Validation

Commands run from the main repository root after integration:

```powershell
python tools\check_pyrevit_extension.py
python tools\static_checks.py --write-report
```

Results:

- `check_pyrevit_extension.py`: `0 errors`, `0 warnings`.
- `static_checks.py`: `0 errors`, `4 warnings`.
- Static warnings are pre-existing docs placeholder warnings and not caused by the integrated W2-003 button code.

## Gate Status

| Gate | Status | Notes |
| --- | --- | --- |
| Direct apply risk tier | pass | Low-risk personal-use workflow |
| Impact summary before write | pass | Candidate count computed before Transaction |
| One confirmation | pass | Explicit confirmation via `CommandSwitchWindow` |
| Single named Transaction | pass | `[Agent] Apply Text Find Replace` |
| Log export | pass | Markdown + CSV |
| Undo note | pass | Confirmation, Markdown, and pyRevit output all mention Undo |
| Live Revit test | pending | User should run once in sandbox model |

## Next Required Step

Run the integrated button once in the sandbox model:

```text
YangAgent > Reports > Apply Text Find Replace
```

Suggested live validation:

- find text: `Level`
- replace text: `LEVEL_TEST_APPLY`
- test on sandbox only
- verify export log
- verify Revit Undo fully reverts the batch

After that, Hermes may continue to `HERMES-W2-004`.
