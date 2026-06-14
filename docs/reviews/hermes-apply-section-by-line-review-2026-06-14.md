# Hermes W3-002 ApplySectionByLine Review

Reviewed Hermes delivery:

- `G:\Hermes Agent\YangAgent Revit\YangAgent Revit\docs\drafts\2026-06-14_hermes_W3-002_delivery`

Decision:

- `accepted`

What passed review:

- The direct-apply workflow matches the current personal-use YangAgent rule:
  - impact summary;
  - explicit confirmation;
  - one named transaction;
  - Markdown and CSV logs;
  - Undo reminder.
- Scope is intentionally narrow:
  - exactly one pre-selected line;
  - no batch behavior;
  - creates one new `ViewSection`;
  - no deletion path.
- The section transform and bounding-box math match the original Gemini `SectionByLineCommand.cs` implementation closely enough for migration review.
- Offline guardrails are present:
  - `py_compile` passed;
  - `check_pyrevit_extension.py` passed.

Residual live-validation risks:

- `CurveElement.GeometryCurve` and `ViewSection.CreateSection(...)` still need live Revit validation in the sandbox model.
- If export-path writing fails after a successful transaction, the section may already exist while the script reports a late failure. This is not a blocker for acceptance, but Codex should keep it in mind during mainline integration.

Codex integration note:

- When this button is merged into the main pyRevit extension, rebuild or refresh the pyRevit runtime cache before the first live click to avoid the recurring wrong FullClassName registration failure.

Next Hermes package:

- `HERMES-W3-003 ViewGraphicCleaner Logic Inventory`
