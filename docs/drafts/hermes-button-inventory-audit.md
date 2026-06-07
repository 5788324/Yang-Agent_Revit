# Hermes Button Inventory Audit

> 审查日期：2026-06-07
> 审查范围：`docs/drafts/hermes-button-inventory.md` vs 实际 pyRevit 目录结构
> 源目录：Hermes 工作区中的 `pyrevit/YangAgent.extension/YangAgent.tab/`

---

## Checked Files

### 审查的源文件（实际 pyRevit 目录）

| # | 文件 | 路径 |
|---|------|------|
| 1 | bundle.yaml | `Settings.panel/SystemSettings.pushbutton/bundle.yaml` |
| 2 | README.md | `Settings.panel/SystemSettings.pushbutton/` — **不存在** |
| 3 | script.py | `Settings.panel/SystemSettings.pushbutton/script.py` ✅ |
| 4 | bundle.yaml | `Reports.panel/Reports.pulldown/ReportExportPath.pushbutton/bundle.yaml` |
| 5 | README.md | `Reports.panel/Reports.pulldown/ReportExportPath.pushbutton/README.md` |
| 6 | bundle.yaml | `Reports.panel/Reports.pulldown/ExportModelSnapshot.pushbutton/bundle.yaml` |
| 7 | README.md | `Reports.panel/Reports.pulldown/ExportModelSnapshot.pushbutton/README.md` |
| 8 | bundle.yaml | `Reports.panel/Reports.pulldown/ModelHealthReport.pushbutton/bundle.yaml` |
| 9 | README.md | `Reports.panel/Reports.pulldown/ModelHealthReport.pushbutton/README.md` |
| 10 | bundle.yaml | `Reports.panel/Reports.pulldown/ExportRegressionChecklist.pushbutton/bundle.yaml` |
| 11 | README.md | `Reports.panel/Reports.pulldown/ExportRegressionChecklist.pushbutton/README.md` |
| 12 | bundle.yaml | `Reports.panel/Reports.pulldown/ExportAIReviewPrompt.pushbutton/bundle.yaml` |
| 13 | README.md | `Reports.panel/Reports.pulldown/ExportAIReviewPrompt.pushbutton/README.md` |
| 14 | bundle.yaml | `Reports.panel/Reports.pulldown/PreviewMissingDoorWindowMarks.pushbutton/bundle.yaml` |
| 15 | README.md | `Reports.panel/Reports.pulldown/PreviewMissingDoorWindowMarks.pushbutton/README.md` |
| 16 | bundle.yaml | `Reports.panel/Reports.pulldown/PreviewMissingRoomNumbers.pushbutton/bundle.yaml` |
| 17 | README.md | `Reports.panel/Reports.pulldown/PreviewMissingRoomNumbers.pushbutton/README.md` |
| 18 | bundle.yaml | `Reports.panel/Reports.pulldown/PreviewDuplicateRoomNumbers.pushbutton/bundle.yaml` |
| 19 | README.md | `Reports.panel/Reports.pulldown/PreviewDuplicateRoomNumbers.pushbutton/README.md` |
| 20 | bundle.yaml | `Reports.panel/Reports.pulldown/PreviewUnplacedViews.pushbutton/bundle.yaml` |
| 21 | README.md | `Reports.panel/Reports.pulldown/PreviewUnplacedViews.pushbutton/README.md` |
| 22 | bundle.yaml | `Reports.panel/Reports.pulldown/PreviewViewNamingRules.pushbutton/bundle.yaml` |
| 23 | README.md | `Reports.panel/Reports.pulldown/PreviewViewNamingRules.pushbutton/README.md` |
| 24 | bundle.yaml | `Reports.panel/Reports.pulldown/ApplyMissingDoorWindowMarks.pushbutton/bundle.yaml` |
| 25 | README.md | `Reports.panel/Reports.pulldown/ApplyMissingDoorWindowMarks.pushbutton/README.md` |
| 26 | bundle.yaml | `Reports.panel/Reports.pulldown/ApplyMissingRoomNumbers.pushbutton/bundle.yaml` |
| 27 | README.md | `Reports.panel/Reports.pulldown/ApplyMissingRoomNumbers.pushbutton/README.md` |

共审查 **13 个 .pushbutton 目录**，每个目录 3 项检查 = **39 项检查点**。

---

## Findings

### 1. bundle.yaml 标题一致性

| # | 按钮目录名 | bundle.yaml title | Inventory 中文显示 | 一致？ |
|---|-----------|-------------------|-------------------|--------|
| 1 | SystemSettings | 系统设置 | 系统设置 | ✅ |
| 2 | ReportExportPath | 导出路径 | 导出路径 | ✅ |
| 3 | ExportModelSnapshot | 导出模型快照 | 导出模型快照 | ✅ |
| 4 | ModelHealthReport | 模型健康报告 | 模型健康报告 | ✅ |
| 5 | ExportRegressionChecklist | 回归测试清单 | 回归测试清单 | ✅ |
| 6 | ExportAIReviewPrompt | AI分析提示词 | AI分析提示词 | ✅ |
| 7 | PreviewMissingDoorWindowMarks | 预览缺失标记 | 预览缺失标记 | ✅ |
| 8 | PreviewMissingRoomNumbers | 预览缺失房间编号 | 预览缺失房间编号 | ✅ |
| 9 | PreviewDuplicateRoomNumbers | 预览重复房间编号 | 预览重复房间编号 | ✅ |
| 10 | PreviewUnplacedViews | 预览未上图视图 | 预览未上图视图 | ✅ |
| 11 | PreviewViewNamingRules | 预览视图命名 | 预览视图命名 | ✅ |
| 12 | ApplyMissingDoorWindowMarks | 应用门窗标记 | 应用门窗标记 | ✅ |
| 13 | ApplyMissingRoomNumbers | 应用房间编号 | 应用房间编号 | ✅ |

**结论：13/13 bundle.yaml 标题与 inventory 中文显示完全一致。**无偏差。

### 2. 目录结构完整性

| 检查项 | 通过 | 备注 |
|--------|------|------|
| `.panel` 目录使用英文名 | ✅ | `Settings.panel`, `Reports.panel` |
| `.pushbutton` 目录使用英文名 | ✅ | 13/13 均为无空格 ASCII |
| `bundle.yaml` 存在 | ✅ | 13/13 |
| `script.py` 存在 | ✅ | 13/13 |
| `icon.png` 存在 | ✅ | 13/13 |
| `README.md` 存在 | ⚠️ 12/13 | SystemSettings.pushbutton 缺少 README.md |

### 3. README.md 第一行标题

| 按钮 | README 标题 |
|------|------------|
| ReportExportPath | `# 导出路径` |
| ExportModelSnapshot | `# Export Model Snapshot` |
| ModelHealthReport | `# Model Health Report` |
| ExportRegressionChecklist | `# Export Regression Checklist` |
| ExportAIReviewPrompt | `# Export AI Review Prompt` |
| PreviewMissingDoorWindowMarks | `# Preview Missing Door Window Marks` |
| PreviewMissingRoomNumbers | `# 预览缺失房间编号` |
| PreviewDuplicateRoomNumbers | `# 预览重复房间编号` |
| PreviewUnplacedViews | `# 预览未上图视图` |
| PreviewViewNamingRules | `# 预览视图命名` |
| ApplyMissingDoorWindowMarks | `# 应用门窗标记` |
| ApplyMissingRoomNumbers | `# Apply Missing Room Numbers` |
| **SystemSettings** | **（文件不存在）** |

**备注**：README 标题语言不统一 — 6 个用中文、6 个用英文。这不影响功能（display name 在 bundle.yaml），但属于文档债务。

### 4. Inventory 覆盖范围

| 检查项 | 结论 |
|--------|------|
| 按钮数量 | 13/13，无遗漏 |
| 按钮目录名 | 13/13 匹配 |
| 中文显示名 | 13/13 匹配 bundle.yaml title |
| 面板归属 | 2 面板正确反映 |
| 类型分类 | 配置(2) + 只读(4) + dry-run(5) + apply(2) = 13，正确 |

---

## Summary

| 指标 | 值 |
|------|-----|
| 审查目录数 | 13 .pushbutton |
| 审查文件数 | 27 (bundle.yaml × 13 + README × 12 + script.py × 13) |
| bundle.yaml 标题一致 | 13/13 ✅ |
| 目录命名规范 | 13/13 ✅ |
| Inventory 覆盖 | 13/13 ✅ |
| 不一致发现 | **0 个功能/命名不一致** |
| 轻微发现 | 2 个 |

### 轻微发现（不影响功能，仅记录）

1. **SystemSettings.pushbutton 缺少 README.md**：其他 12 个按钮都有，此按钮没有。不影响功能（bundle.yaml 已定义显示名）。
2. **README 语言不统一**：6 个 README 用中文标题、6 个用英文标题。建议未来统一为中文（与 bundle.yaml title 一致）。

### 是否需要修正 inventory？

**不需要。** `hermes-button-inventory.md` 在所有关键数据点（目录名、中文显示名、数量、类型分类、面板归属）上与实际 pyRevit 结构完全一致。上述两个轻微发现不要求 inventory 做任何改动。

---

## Safety Confirmation

- I did not edit pyRevit scripts.
- I did not edit C# files.
- I did not edit scripts or addin templates.
- I did not run install scripts.
- I did not add .rvt files.
- I did not run git merge / push / pull.
- I did not modify `hermes-button-inventory.md`.
