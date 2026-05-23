# 用户使用指南

本文档面向不熟悉 AI 和编程的 Revit 使用者。

## 1. 当前能做什么

当前版本提供两个功能区：

- `系统设置`
- `导出报告`

系统设置：

- `系统设置`：统一设置语言、简称、头像路径、Light/Dark Theme，并查看版权声明和更新链接。

导出报告：

- `导出路径`：设置报告输出目录，避免报告堆积。
- `导出模型快照`：导出模型快照，给 AI 分析。
- `模型健康报告`：生成模型健康检查报告。
- `预览缺失标记`：预览缺少标记的门窗，不修改模型。
- `预览缺失房间编号`：预览缺少编号的房间，不修改模型。
- `预览重复房间编号`：预览重复编号的房间，不修改模型。
- `预览未上图视图`：预览可能未放置到图纸的视图，不修改模型。
- `应用门窗标记`：读取 dry-run CSV，在二次确认后写入门窗标记。

除 `应用门窗标记` 外，其它报告和预览工具都不会修改模型。

工具箱支持两种语言：

- 中文
- English

你可以通过 `系统设置` 设置默认语言。

## 2. 安装 pyRevit 工具栏

前提：

- 已安装 Revit。
- 已安装 pyRevit。如果 Revit 中没有 pyRevit 选项卡，本项目按钮也不会显示。
- 本仓库已克隆到本机。

### 2.1 检查 pyRevit 是否安装

打开 Revit 后，先看功能区是否有 `pyRevit` 选项卡。

如果没有，先安装 pyRevit：

```text
https://github.com/pyrevitlabs/pyRevit/releases
```

安装完成后重启 Revit，确认能看到 `pyRevit` 选项卡，再继续安装本项目工具栏。

### 2.2 安装 YangAgent 工具栏

在 PowerShell 中进入仓库目录：

```powershell
cd "D:\codex\Yang Agent_Revit"
.\scripts\install-pyrevit-extension.ps1
```

然后重启 Revit，或在 pyRevit 中 reload。

成功后会看到：

```text
YangAgent -> 系统设置
YangAgent -> 导出报告
```

如果看不到：

1. 确认 Revit 里已经能看到 `pyRevit` 选项卡。
2. 确认脚本没有提示安装失败。
3. 在 pyRevit 里执行 reload。
4. 重启 Revit。

如果按钮都是灰色，并提示 `availability` 或“可用性命令载入失败”，请先关闭 Revit，清理 pyRevit 旧缓存，再重新打开 Revit。

## 3. 设置语言

点击：

```text
YangAgent -> 系统设置
```

选择 `中文` 或 `English`。设置会保存到本机，后续按钮自动使用该语言。

## 4. 设置用户、主题和导出路径

用户和主题设置：

```text
YangAgent -> 系统设置
```

可设置：

- 简称。
- 头像图片路径。
- Light Theme
- Dark Theme

导出路径：

```text
YangAgent -> 导出报告 -> 导出路径
```

用于选择报告输出目录，方便自己管理报告文件。

## 5. 使用 Export Model Snapshot

适合场景：

- 想让 AI 理解当前模型。
- 想导出房间、门窗、视图、图纸数据。
- 想先做数据分析，不改模型。

操作：

1. 打开 Revit 模型。
2. 点击 `YangAgent -> 导出报告 -> 导出模型快照`。
3. 等待导出完成。
4. 到你设置的导出目录查看结果。

输出文件：

- `model_snapshot_*.json`
- `rooms_*.csv`
- `doors_windows_*.csv`
- `sheets_views_*.csv`

## 6. 使用 Model Health Report

适合场景：

- 检查房间编号缺失。
- 检查房间名称缺失。
- 检查重复房间编号。
- 检查门窗标记缺失。
- 检查可能未上图的视图。

操作：

1. 打开 Revit 模型。
2. 点击 `YangAgent -> 导出报告 -> 模型健康报告`。
3. 到你设置的导出目录查看报告。

输出文件：

- `model_health_report_*.md`

## 7. 使用 Preview Missing Marks

适合场景：

- 检查哪些门窗缺少 `Mark/标记`。
- 生成 dry-run 预览清单。
- 给后续修复工具准备数据。

操作：

1. 打开 Revit 模型。
2. 点击 `YangAgent -> 导出报告 -> 预览缺失标记`。
3. 到你设置的导出目录查看报告。

输出文件：

- `missing_door_window_marks_*.md`
- `missing_door_window_marks_*.csv`

注意：此工具只预览，不会写入标记。

## 8. 使用 Preview Missing Room Numbers

适合场景：

- 检查哪些房间缺少编号。
- 生成 dry-run 预览清单。
- 给后续房间编号修复工具准备数据。

操作：

1. 打开 Revit 模型。
2. 点击 `YangAgent -> 导出报告 -> 预览缺失房间编号`。
3. 到你设置的导出目录查看报告。

输出文件：

- `missing_room_numbers_*.md`
- `missing_room_numbers_*.csv`

注意：此工具只预览，不会写入房间编号。

## 9. 使用 Preview Duplicate Room Numbers

适合场景：

- 检查哪些房间编号重复。
- 生成 dry-run 预览清单。
- 给后续房间编号规则整理做准备。

操作：

1. 打开 Revit 模型。
2. 点击 `YangAgent -> 导出报告 -> 预览重复房间编号`。
3. 到你设置的导出目录查看报告。

输出文件：

- `duplicate_room_numbers_*.md`
- `duplicate_room_numbers_*.csv`

注意：此工具只预览，不会修改房间编号。

## 10. 使用 Preview Unplaced Views

适合场景：

- 检查哪些视图可能没有放到图纸。
- 筛查临时视图、工作视图、分析视图。
- 为后续视图整理规则做准备。

操作：

1. 打开 Revit 模型。
2. 点击 `YangAgent -> 导出报告 -> 预览未上图视图`。
3. 到你设置的导出目录查看报告。

输出文件：

- `unplaced_views_*.md`
- `unplaced_views_*.csv`

注意：此工具只预览，不会修改视图或图纸。

## 11. 使用 Apply Missing Door Window Marks

此工具会修改模型。只建议在测试模型或已备份模型中使用。

使用前必须先运行：

```text
YangAgent -> 导出报告 -> 预览缺失标记
```

然后人工检查输出的：

```text
missing_door_window_marks_*.csv
```

确认无误后再运行：

```text
YangAgent -> 导出报告 -> 应用门窗标记
```

安全机制：

- 只能选择 CSV 文件。
- 只读取 dry-run 行。
- 只处理 `Door` 和 `Window`。
- 只写入当前 Mark 仍为空的元素。
- 执行前会显示影响数量并要求二次确认。
- 所有修改放在一个 Revit Transaction 中，可通过 Revit 撤销。

输出文件：

- `apply_door_window_marks_*.md`
- `apply_door_window_marks_*.csv`

## 12. 如何把结果交给 AI

你可以把导出的 `.md`、`.json`、`.csv` 文件发给 Codex、Claude Code 或 Antigravity，然后这样问：

```text
请分析这份 Revit 模型健康报告，按严重程度列出问题，并建议下一步 pyRevit 修复方案。
```

如果要生成修复脚本，建议这样问：

```text
请先生成 dry-run 脚本，只预览会修改哪些元素，不要直接修改模型。
```

## 13. 版权和更新

点击：

```text
YangAgent -> 系统设置
```

可查看：

- 版权声明：由 Yang 开发，工具为 Codex。
- 插件更新链接。

## 14. 安全提醒

当前报告和预览工具不会修改模型。

后续如果出现修复工具，请记住：

- 先在测试模型运行。
- 先 dry-run。
- 确认影响元素数量。
- 再执行真正修改。
