# Hermes W1-001 ChineseCheck Inventory Review

Reviewed Hermes delivery:

- `G:\Hermes Agent\YangAgent Revit\YangAgent Revit\docs\drafts\2026-06-14_hermes_W1-001_delivery`

Decision:

- `accepted with implementation direction`

What passed review:

- Hermes correctly separated the Gemini feature into two very different halves:
  - read-only Chinese/CJK audit logic;
  - dangerous delete workflow.
- Hermes traced the real logic into `ChineseCheckWindow.xaml.cs` instead of stopping at the command shell.
- The inventory correctly identified the useful V1 scope:
  - family names and symbols;
  - parameter names and values;
  - materials;
  - text notes;
  - views;
  - project info fields.
- The inventory also correctly identified the unsafe scope:
  - batch `doc.Delete(...)`;
  - weak safety messaging;
  - no proper CSV/Markdown action log for destructive work.

Codex direction:

- Only the audit half enters YangAgent V1.
- The delete half is rejected for current YangAgent migration.
- The V1 target should be one read-only preview tool:
  - `PreviewChineseContent.pushbutton`
- It should export Markdown + CSV and make no model changes.

Scheduling decision:

- This feature should enter the active V1 queue now.
- It is smaller, safer, and faster to close than the deferred Wave 3 heavy tools.

Next Hermes package:

- `HERMES-W1-002 PreviewChineseContent Draft`
