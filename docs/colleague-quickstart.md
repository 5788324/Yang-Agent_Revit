# YangAgent Revit 同事快速使用说明

这份说明用于发给公司同事，帮助他们安装并使用 YangAgent Revit 工具箱。

## 1. 这是什么

YangAgent Revit 是一个基于 pyRevit 的公司内部工具箱，用来配合 Codex、Claude Code、Antigravity 等 AI 工具分析 Revit 模型、生成报告、辅助开发插件。

当前版本以安全为主：

- 只读模型。
- 不修改模型。
- 不删除元素。
- 不保存模型。
- 输出报告给人和 AI 分析。

## 2. 当前功能

在 Revit 中会出现：

```text
YangAgent -> AI Tools
```

当前按钮：

- `Language Settings`：设置默认语言。
- `Export Model Snapshot`：导出模型快照。
- `Model Health Report`：生成模型健康报告。

## 3. 安装前检查

必须先安装 pyRevit。

打开 Revit 后，检查功能区是否能看到：

```text
pyRevit
```

如果看不到，请先安装 pyRevit：

```text
https://github.com/pyrevitlabs/pyRevit/releases
```

安装完成后重启 Revit。

## 4. 安装 YangAgent 工具箱

在 PowerShell 中运行：

```powershell
cd "D:\codex\Yang Agent_Revit"
.\scripts\install-pyrevit-extension.ps1
```

然后重启 Revit，或在 pyRevit 中 reload。

## 5. 设置语言

点击：

```text
YangAgent -> AI Tools -> Language Settings
```

选择：

- 中文
- English

设置会保存到本机：

```text
%APPDATA%\YangAgent_Revit\settings.json
```

后续按钮会自动使用默认语言。

## 6. 导出模型快照

点击：

```text
YangAgent -> AI Tools -> Export Model Snapshot
```

输出目录：

```text
桌面\YangAgent_Revit_Exports
```

输出文件：

- `model_snapshot_*.json`
- `rooms_*.csv`
- `doors_windows_*.csv`
- `sheets_views_*.csv`

用途：

- 给 AI 分析模型。
- 检查房间、门窗、视图、图纸数据。
- 作为后续自动化任务的数据来源。

## 7. 生成模型健康报告

点击：

```text
YangAgent -> AI Tools -> Model Health Report
```

输出文件：

- `model_health_report_*.md`

当前检查：

- 房间缺少编号。
- 房间缺少名称。
- 房间编号重复。
- 门缺少标记。
- 窗缺少标记。
- 可能未放置到图纸的视图。

## 8. 如何把报告交给 AI

把导出的 `.md`、`.json`、`.csv` 文件发给 Codex、Claude Code 或 Antigravity，然后可以这样问：

```text
请分析这份 Revit 模型健康报告，按严重程度列出问题。
只给建议，不要生成会直接修改模型的脚本。
```

如果要生成修复脚本，必须先要求 dry-run：

```text
请先生成 dry-run 脚本，只预览会修改哪些元素，不要直接修改模型。
```

## 9. 常见问题

### Revit 里看不到 YangAgent

先检查 Revit 里有没有 `pyRevit` 选项卡。

如果没有，说明 pyRevit 还没安装或没有加载。先安装 pyRevit，再安装 YangAgent。

### 点击按钮没有输出文件

检查桌面是否有：

```text
YangAgent_Revit_Exports
```

如果没有，查看 pyRevit 输出窗口里的错误信息。

### 语言不对

运行 `Language Settings` 重新选择语言。

## 10. 安全提醒

当前工具不会修改模型。

后续如果增加修复按钮，使用原则是：

1. 先测试模型。
2. 先 dry-run。
3. 确认影响元素数量。
4. 再执行真正修改。
