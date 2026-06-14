# Gemini Feature Restoration Map - 2026-06-14

## Purpose

This document defines what "restore Gemini functionality" means for YangAgent.

The rule is:

- restore the user-facing business capability;
- restore a recognisable panel and button layout where it helps daily work;
- do not restore Gemini's internal architecture, unsafe runtime model, or dynamic execution design.

## Current Source Of Truth

Gemini reference source:

```text
G:\Codex\YangAgent Revit\YangAgent Revit\Gemini 资料\YangTools_SourceCode
```

Target mainline:

```text
G:\Codex\YangAgent Revit\YangAgent Revit
```

## Restoration Outcomes

Only four outcomes are allowed:

| outcome | meaning |
| --- | --- |
| restore_same_capability | Restore the same user-visible business function in YangAgent. |
| restore_split_workflow | Restore the function, but split into preview/apply or several smaller tools. |
| restore_later | Keep the target and panel slot, but defer implementation. |
| reject_architecture_keep_idea | Keep only the business idea; reject Gemini runtime design. |

## Panel Restoration Map

### 文本工具区

| Gemini button | source command | target YangAgent feature | outcome | target phase | notes |
| --- | --- | --- | --- | --- | --- |
| 文本修改 | `TextModifierCommand` | `yangagent.text_find_replace` | restore_split_workflow | Wave 2 | Already started with preview/apply pair |
| 文本合并 | `MergeTextCommand` | `yangagent.text_merge` | restore_same_capability | Wave 2 | Keep tool narrow and selection-scoped |
| 对齐文本 | `AlignTextToTextCommand` | `yangagent.text_align_to_text` | restore_same_capability | Wave 2 | Must log affected TextNote ids |
| 对齐到线 | `AlignTextToLineCommand` | `yangagent.text_align_to_line` | restore_same_capability | Wave 2 | Should stay selection-driven |
| 等距分布 | `DistributeTextCommand` | `yangagent.text_distribute` | restore_same_capability | Wave 2 | Must show impact count before apply |

### 标注工具区

| Gemini button | source command | target YangAgent feature | outcome | target phase | notes |
| --- | --- | --- | --- | --- | --- |
| 标注替换 | `DimTextOverrideCommand` | `yangagent.dim_text_override` | restore_split_workflow | Wave 2 or 3 | Needs explicit warning because dimension override is easy to misuse |

### 检查工具区

| Gemini button | source command | target YangAgent feature | outcome | target phase | notes |
| --- | --- | --- | --- | --- | --- |
| 中文检查 | `ChineseCheckCommand` | `yangagent.text_audit` | restore_same_capability | Wave 1 or 2 | Keep audit logic; reject delete-first behavior |

### 视图修改区

| Gemini button | source command | target YangAgent feature | outcome | target phase | notes |
| --- | --- | --- | --- | --- | --- |
| 覆盖清理 | `ViewGraphicCleanerCommand` | `yangagent.view_graphics_clean` | restore_same_capability | Wave 3 | Active-view scope first |
| 可见性拷贝 | `VisibilityCopierCommand` | `yangagent.visibility_copy` | restore_split_workflow | Wave 3 | Must force explicit source/target confirmation |
| 剖面(By Line) | `SectionByLineCommand` | `yangagent.section_from_line` | restore_later | Wave 3 | Candidate after safer view workflow pattern exists |

### 项目管理区

| Gemini button | source command | target YangAgent feature | outcome | target phase | notes |
| --- | --- | --- | --- | --- | --- |
| 图纸管理 | `SheetManagerCommand` | `yangagent.sheet_workflows` | restore_split_workflow | Wave 3 | Split by exact task, not one giant manager window |
| 族实例管理 | `FamilyInstanceManagerCommand` | `yangagent.family_instance_workflows` | restore_later | Post-V1 | Needs safety shell first |
| 族文档管理 | `FamilyManagerCommand` | `yangagent.family_document_workflows` | restore_later | Post-V1 | Family save/load/delete stays high risk |
| 项目资产管理器 | `ProjectAssetManagerCommand` | `yangagent.project_assets` | reject_architecture_keep_idea | Post-V1 | Keep idea source only; do not port current design |

### 模型修改区

| Gemini button | source command | target YangAgent feature | outcome | target phase | notes |
| --- | --- | --- | --- | --- | --- |
| 标高修改 | `LevelModifierCommand` | `yangagent.level_adjust` | restore_split_workflow | Wave 3 | Useful, but preview/report first |
| 基于面转换 | `FaceBasedConverterCommand` | `yangagent.face_based_convert` | restore_later | Post-V1 | High-risk transformation |
| 布尔几何 | `BooleanGeometryCommand` | `yangagent.boolean_geometry` | restore_later | Post-V1 | High-risk geometry operation |
| 实体生成(Loft) | `EntityGeneratorCommand` | `yangagent.entity_generator` | restore_later | Post-V1 | High-risk generation |
| 线性布置 | `LinearPlacementCommand` | `yangagent.linear_placement` | restore_later | Post-V1 | Needs placement safety shell |

### 项目信息区

| Gemini button | source command | target YangAgent feature | outcome | target phase | notes |
| --- | --- | --- | --- | --- | --- |
| 文件统计 | `ProjectInfoCommand` | `yangagent.project_info_report` | restore_same_capability | Wave 1 | Already restored in YangAgent direction |

### 项目工具区

| Gemini button | source command | target YangAgent feature | outcome | target phase | notes |
| --- | --- | --- | --- | --- | --- |
| 项目微工具 | `MicroToolCommand` | `yangagent.project_microtools` | reject_architecture_keep_idea | Post-V1 | No dynamic runner allowed |

### 系统管理区

| Gemini button | source command | target YangAgent feature | outcome | target phase | notes |
| --- | --- | --- | --- | --- | --- |
| 面板设置 | `RibbonSettingsCommand` | `yangagent.feature_visibility` | restore_later | Wave 0 or later | Only after theme/settings settle |
| AI 助手 | `CopilotCommand` | `yangagent.assistant_shell` | reject_architecture_keep_idea | Wave 4 | No dynamic Python execution |
| MCP 状态 | `McpStatusCommand` | `yangagent.mcp_status` | restore_same_capability | Wave 4 | Status shell only, no unsafe auto-start |
| 你好，Revit | `HelloWorldCommand` | none | reject_architecture_keep_idea | n/a | Demo only |
| 窗口测试 | `SampleWindowCommand` | `yangagent.window_pattern_reference` | restore_later | Wave 0 | Reference only, not product feature |

### 总控中心

| Gemini button | source command | target YangAgent feature | outcome | target phase | notes |
| --- | --- | --- | --- | --- | --- |
| 批处理与云链接 | `BatchTaskCommand` | `yangagent.batch_workflows` | reject_architecture_keep_idea | Post-V1 | Too broad; future only as controlled workflows |

### 导入工具区

| Gemini button | source command | target YangAgent feature | outcome | target phase | notes |
| --- | --- | --- | --- | --- | --- |
| 从CAD粘贴 | `PasteCadCommand` | `yangagent.paste_cad` | restore_later | Post-V1 | External input and geometry risk too high for current stage |

## Practical Interpretation

From now on, "功能要还原" means:

1. Restore Gemini's practical job-to-be-done.
2. Keep recognisable panel grouping where useful.
3. Keep user habit continuity where possible.
4. Rebuild under YangAgent standards instead of copying Gemini runtime design.
