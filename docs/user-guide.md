# 用户使用指南

本文档面向不熟悉 AI 和编程的 Revit 使用者。

## 1. 当前能做什么

当前版本提供两个只读 pyRevit 按钮：

- `Export Model Snapshot`：导出模型快照，给 AI 分析。
- `Model Health Report`：生成模型健康检查报告。

它们都不会修改模型。

## 2. 安装 pyRevit 工具栏

前提：

- 已安装 Revit。
- 已安装 pyRevit。
- 本仓库已克隆到本机。

在 PowerShell 中进入仓库目录：

```powershell
cd "D:\codex\Yang Agent_Revit"
.\scripts\install-pyrevit-extension.ps1
```

然后重启 Revit，或在 pyRevit 中 reload。

成功后会看到：

```text
YangAgent -> AI Tools
```

## 3. 使用 Export Model Snapshot

适合场景：

- 想让 AI 理解当前模型。
- 想导出房间、门窗、视图、图纸数据。
- 想先做数据分析，不改模型。

操作：

1. 打开 Revit 模型。
2. 点击 `YangAgent -> AI Tools -> Export Model Snapshot`。
3. 等待导出完成。
4. 到桌面 `YangAgent_Revit_Exports` 文件夹查看结果。

输出文件：

- `model_snapshot_*.json`
- `rooms_*.csv`
- `doors_windows_*.csv`
- `sheets_views_*.csv`

## 4. 使用 Model Health Report

适合场景：

- 检查房间编号缺失。
- 检查房间名称缺失。
- 检查重复房间编号。
- 检查门窗标记缺失。
- 检查可能未上图的视图。

操作：

1. 打开 Revit 模型。
2. 点击 `YangAgent -> AI Tools -> Model Health Report`。
3. 到桌面 `YangAgent_Revit_Exports` 文件夹查看报告。

输出文件：

- `model_health_report_*.md`

## 5. 如何把结果交给 AI

你可以把导出的 `.md`、`.json`、`.csv` 文件发给 Codex、Claude Code 或 Antigravity，然后这样问：

```text
请分析这份 Revit 模型健康报告，按严重程度列出问题，并建议下一步 pyRevit 修复方案。
```

如果要生成修复脚本，建议这样问：

```text
请先生成 dry-run 脚本，只预览会修改哪些元素，不要直接修改模型。
```

## 6. 安全提醒

当前两个工具都是只读工具，不会修改模型。

后续如果出现修复工具，请记住：

- 先在测试模型运行。
- 先 dry-run。
- 确认影响元素数量。
- 再执行真正修改。
