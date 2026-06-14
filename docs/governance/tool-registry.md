# External Tool Registry

This registry tracks external tools before rewrite into YangAgent.

| tool_id | source | class | rewrite_status | owner | review_outcome | target_feature | notes |
| --- | --- | --- | --- | --- | --- | --- | --- |
| gemini.project_info | Gemini | A | in_progress | Codex | needs changes | yangagent.project_info_report | First active external rewrite candidate |
| gemini.chinese_check | Gemini | B/C | planned | Codex | needs changes | yangagent.text_audit | Keep check idea, drop delete-first behavior |
| gemini.sheet_manager | Gemini | B | deferred | Codex | needs changes | yangagent.sheet_workflows | Needs exact workflow and safety shell |
| gemini.level_modifier | Gemini | B/C | deferred | Codex | needs changes | yangagent.level_adjust | Only after preview/report design |
| gemini.text_modifier | Gemini | B | planned | Codex | needs changes | yangagent.text_tools | Strong rewrite candidate |
| gemini.merge_text | Gemini | B | backlog | Codex | needs changes | yangagent.text_merge | Keep only if work need appears |
| gemini.align_text_to_line | Gemini | B | backlog | Codex | needs changes | yangagent.text_align_line | UI style must be rewritten |
| gemini.align_text_to_text | Gemini | B | backlog | Codex | needs changes | yangagent.text_align_text | UI style must be rewritten |
| gemini.distribute_text | Gemini | B | backlog | Codex | needs changes | yangagent.text_distribute | Needs preview count |
| gemini.dim_text_override | Gemini | B/C | deferred | Codex | needs changes | yangagent.dim_text_override | Explicit warning required |
| gemini.view_graphic_cleaner | Gemini | B | backlog | Codex | needs changes | yangagent.view_graphics_clean | Scope must stay explicit |
| gemini.visibility_copier | Gemini | B/C | deferred | Codex | needs changes | yangagent.visibility_copy | Strong target-view confirmation required |
| gemini.paste_cad | Gemini | C | blocked | Codex | rejected | n/a | External data/model change too risky now |
| gemini.batch_task | Gemini | C | blocked | Codex | rejected | n/a | Broad batch workflow not allowed now |
| gemini.project_asset_manager | Gemini | C | blocked | Codex | rejected | n/a | Future-only idea source |
| gemini.family_manager | Gemini | C | blocked | Codex | rejected | n/a | High-risk family operations |
| gemini.family_instance_manager | Gemini | C | blocked | Codex | rejected | n/a | High-risk instance operations |
| gemini.face_based_converter | Gemini | C | blocked | Codex | rejected | n/a | High-risk transformation flow |
| gemini.boolean_geometry | Gemini | C | blocked | Codex | rejected | n/a | High-risk geometry tool |
| gemini.entity_generator | Gemini | C | blocked | Codex | rejected | n/a | High-risk generation tool |
| gemini.linear_placement | Gemini | C | blocked | Codex | rejected | n/a | Requires placement safety system first |
| gemini.section_by_line | Gemini | B/C | backlog | Codex | needs changes | yangagent.section_from_line | Possible future candidate |
| gemini.micro_tool | Gemini | X | blocked | Codex | rejected | n/a | Unknown dynamic runner shape |
| gemini.copilot_panel | Gemini | X | blocked | Codex | rejected | n/a | Dynamic execution not accepted |
| gemini.mcp_status | Gemini | X | blocked | Codex | rejected | n/a | MCP design not approved yet |
| gemini.hello_world | Gemini | X | blocked | Codex | rejected | n/a | Demo only |
| gemini.sample_window | Gemini | D | backlog | Codex | needs changes | yangagent.window_pattern_reference | Visual reference only |
| gemini.ribbon_settings | Gemini | D | backlog | Codex | needs changes | yangagent.feature_visibility | Only as future controlled settings idea |

## Migration Waves

The goal is full controlled migration, not one-off cherry-picking. Gemini tools are migrated by waves so new Gemini code cannot define YangAgent architecture.

| wave | scope | goal | status | rule |
| --- | --- | --- | --- | --- |
| 0 | theme and design system | Shared `theme_id`, report styling, WPF token bridge | in_progress | No new migrated UI may hard-code colors |
| 1 | read-only reports and audits | Fast useful diagnostics with no model write | in_progress | Prefer pyRevit unless C# is required |
| 2 | text and annotation tools | Daily production drafting helpers | planned | Default to direct-apply after impact summary; use stronger confirmation and stricter transaction safety instead of preview |
| 3 | sheets, views, levels, visibility | Higher-impact project coordination tools | planned | One workflow at a time; target model must be explicit |
| 4 | MCP and automation shell | Controlled agent access to Revit context | planned | No auto-start write server and no dynamic code execution |
| 5 | family, geometry, generation tools | High-risk transformations | deferred | Only after safety shell is proven |

## Current Priority Queue

1. Finish wave 0 so pyRevit and future C# Gemini rewrites share the same theme tokens.
2. Freeze the already validated report/preview/apply buttons unless a concrete blocker appears.
3. Start wave 2 with the text tool family because it has the fastest daily-work payoff.
4. Keep MCP as wave 4: design the safety shell first, then implement.

## Hermes Execution Board

Active board:

```text
G:\Hermes Agent\YangAgent Revit\YangAgent Revit\docs\drafts\codex-hermes-v1-migration-board-2026-06-14.md
```

Main-repo mirror:

```text
docs/governance/codex-hermes-v1-migration-board-2026-06-14.md
```

Execution model:

- Codex writes task packages.
- Hermes / DeepSeek implement or inventory only inside task package boundaries.
- Codex reviews delivery reports and code diffs.
- Codex decides `accepted`, `needs changes`, `rejected`, or `superseded by Codex`.
- Hermes may not merge, redesign architecture, or declare live Revit success.

Current assigned packages:

| task id | status | type | output |
| --- | --- | --- | --- |
| HERMES-W0-001 | assigned | read-only audit | `2026-06-14_hermes_theme-compliance-audit.md` |
| HERMES-W2-001 | queued | read-only inventory | `2026-06-14_hermes_text-tools-inventory.md` |
| HERMES-W2-002 | blocked | preview draft | wait for Codex review of W2-001 |
