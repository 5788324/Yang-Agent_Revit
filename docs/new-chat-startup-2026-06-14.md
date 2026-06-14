# New Chat Startup - 2026-06-14

Use this prompt when starting the next Codex chat.

## Copy This Prompt

```text
Continue the YangAgent Revit project. Reply in Chinese to the user.

Active repository:
G:\Codex\YangAgent Revit\YangAgent Revit

Do not return to the old D drive path for development.
Do not modify production Revit models.
Model-modification rule:
Low-risk personal tools may use:
impact summary -> human confirmation -> apply -> log -> Undo check
High-risk or external-input tools must still use:
preview/dry-run -> human confirmation -> apply -> log -> Undo check

Start with:
1. git status --short --branch
2. git log -3 --oneline
3. Pull only if the working tree is safe.
4. Read docs/framework/daily-ops-routine.md.
5. Read docs/next-steps.md.
6. Read docs/worklogs/worklog-2026-06-14.md.
7. If any new `.pushbutton` was added or renamed since the last live run, proactively rebuild the pyRevit YangAgent runtime cache before asking the user to click the new button.

Current priority:
Accelerate controlled Gemini migration through bounded Hermes task packages. Codex reviews, integrates, and validates; Hermes writes low-risk drafts only.

Fixed blocker:
ProjectInfoReport pyRevit runtime cache / Wrong Full Class Name issue is fixed.

Evidence:
- Cleared the pyRevit 2027 YangAgent runtime cache DLL/CS.
- pyRevit rebuilt the YangAgent runtime DLL.
- The rebuilt DLL contains yangagent_yangagent_reports_reports_projectinforeport.
- Snowdon sandbox generated project_info_report_20260614_105341.md and project_info_report_20260614_105621.md.

Current test model:
Snowdon Towers Sample Architectural_sandbox.rvt under the local Gemini materials / Revit test model folder.
If the exact path is needed and Chinese path segments display badly, read docs/worklogs/worklog-2026-06-14.md or ask the user to confirm the path.

Current report directory:
The report folder next to the local Revit test models. If the exact path displays badly, read docs/worklogs/worklog-2026-06-14.md or ask the user to confirm the path.

Manual live validation completed by the user:
- All report/export/preview buttons exported successfully.
- Apply Missing Room Numbers succeeded.
- Undo after Apply Missing Room Numbers succeeded.
- Apply Missing Door Window Marks succeeded.
- Undo after Apply Missing Door Window Marks succeeded.

Next work:
1. Treat `TextModifier` as a low-risk personal-use tool candidate.
2. Authorize `HERMES-W2-003 TextModifier Apply Draft` with impact summary + confirmation + Undo note.
3. Review Hermes/DeepSeek bounded code deliveries before merge.
4. Fix only concrete bugs found from live use.
5. Keep docs updates limited to worklog / next-steps / startup.

Current Wave 2 status:
- `HERMES-W0-001 Theme Compliance Audit`: accepted.
- `HERMES-W2-001 Gemini Text Tools Inventory`: accepted.
- `HERMES-W2-002 TextModifier Preview Draft`: accepted with Codex integration fixes.
- Mainline now includes `PreviewTextFindReplace.pushbutton`.
- Offline checks pass: `python tools\check_pyrevit_extension.py` reports 0 errors / 0 warnings; `python tools\static_checks.py --write-report` reports 0 errors and only 3 pre-existing docs warnings.
- Preview is useful, but no longer mandatory for every low-risk personal-use tool.

Hermes / DeepSeek:
They may provide low-risk code or checklist drafts, but Codex owns review, merge decisions, and live validation closure.
Do not let external agents define architecture, theme, naming, or safety rules.
```

## Current Status

- `ProjectInfoReport` runtime registration/cache issue is fixed.
- Snowdon sandbox report generation is confirmed.
- Report/export/preview/apply/Undo chain is manually live-validated.
- `PreviewTextFindReplace.pushbutton` is integrated as the first Wave 2 Gemini text-tool rewrite preview.
- Next work is a bounded TextModifier apply draft under the low-risk direct-apply rule.
