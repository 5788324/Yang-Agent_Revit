# YangAgent Revit 同事快速使用说明

这份说明用于发给公司同事，帮助他们安装并使用 YangAgent Revit 工具箱。

## 1. 这是什么

YangAgent Revit 是一个基于 pyRevit 的公司内部工具箱，用来配合 Codex、Claude Code、Antigravity 等 AI 工具分析 Revit 模型、生成报告、辅助开发插件。

当前版本以安全为主：

- 报告和预览工具只读模型。
- 修改工具必须先 dry-run 并二次确认。
- 不删除元素。
- 不保存模型。
- 输出报告给人和 AI 分析。

## 2. 当前功能

在 Revit 中会出现：

```text
YangAgent -> 系统设置
YangAgent -> 导出报告
```

系统设置：

- `系统设置`：统一设置语言、简称、头像路径、Light/Dark Theme，并查看版权声明和更新链接。

导出报告：

- `导出路径`：设置报告导出目录。
- `导出模型快照`：导出模型快照。
- `模型健康报告`：生成模型健康报告。
- `预览缺失标记`：dry-run 预览缺少标记的门窗。
- `预览缺失房间编号`：dry-run 预览缺少编号的房间。
- `预览重复房间编号`：dry-run 预览重复编号的房间。
- `预览未上图视图`：dry-run 预览可能未放置到图纸的视图。
- `预览视图命名`：dry-run 预览视图命名规则问题。
- `应用门窗标记`：读取 dry-run CSV，并在二次确认后写入门窗标记。
- `应用房间编号`：读取 dry-run CSV，并在二次确认后写入缺失房间编号。

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
YangAgent -> 系统设置
```

选择：

- 中文
- English

设置会保存到本机：

```text
%APPDATA%\YangAgent_Revit\settings.json
```

后续按钮会自动使用默认语言。

## 6. 设置用户、主题和报告路径

用户和主题设置：

```text
YangAgent -> 系统设置
```

报告路径：

```text
YangAgent -> 导出报告 -> 导出路径
```

建议每个项目单独设置一个报告目录，避免文件堆积。

## 7. 导出模型快照

点击：

```text
YangAgent -> 导出报告 -> 导出模型快照
```

输出目录由 `导出路径` 设置。未设置时默认在桌面 `YangAgent_Revit_Exports`。

输出文件：

- `model_snapshot_*.json`
- `rooms_*.csv`
- `doors_windows_*.csv`
- `sheets_views_*.csv`

用途：

- 给 AI 分析模型。
- 检查房间、门窗、视图、图纸数据。
- 作为后续自动化任务的数据来源。

## 8. 生成模型健康报告

点击：

```text
YangAgent -> 导出报告 -> 模型健康报告
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

## 9. 预览门窗缺失标记

点击：

```text
YangAgent -> 导出报告 -> 预览缺失标记
```

输出文件：

- `missing_door_window_marks_*.md`
- `missing_door_window_marks_*.csv`

这个按钮是 dry-run，只生成预览，不会写入模型。

## 10. 预览房间缺失编号

点击：

```text
YangAgent -> 导出报告 -> 预览缺失房间编号
```

输出文件：

- `missing_room_numbers_*.md`
- `missing_room_numbers_*.csv`

这个按钮是 dry-run，只生成预览，不会写入模型。

## 11. 预览重复房间编号

点击：

```text
YangAgent -> 导出报告 -> 预览重复房间编号
```

输出文件：

- `duplicate_room_numbers_*.md`
- `duplicate_room_numbers_*.csv`

这个按钮是 dry-run，只生成预览，不会修改模型。

## 12. 预览未上图视图

点击：

```text
YangAgent -> 导出报告 -> 预览未上图视图
```

输出文件：

- `unplaced_views_*.md`
- `unplaced_views_*.csv`

这个按钮是 dry-run，只生成预览，不会修改模型。

## 13. 预览视图命名

点击：

```text
YangAgent -> 导出报告 -> 预览视图命名
```

输出文件：

- `view_naming_rules_*.md`
- `view_naming_rules_*.csv`

这个按钮是 dry-run，只生成预览，不会修改模型。

## 14. 应用门窗标记

此工具会修改模型。请先使用测试模型。

步骤：

1. 运行 `导出报告 -> 预览缺失标记`。
2. 人工检查 `missing_door_window_marks_*.csv`。
3. 运行 `导出报告 -> 应用门窗标记`。
4. 选择刚检查过的 CSV。
5. 在二次确认窗口确认影响数量。
6. 执行后检查 `apply_door_window_marks_*.md` 和 `.csv` 日志。

安全机制：

- 只处理 `Door` 和 `Window`。
- 只写入当前 Mark 仍为空的元素。
- 全部修改在一个 Revit Transaction 中，可撤销。

## 15. 应用房间编号

此工具会修改模型。请先使用测试模型。

步骤：

1. 运行 `导出报告 -> 预览缺失房间编号`。
2. 人工检查 `missing_room_numbers_*.csv`。
3. 运行 `导出报告 -> 应用房间编号`。
4. 选择刚检查过的 CSV。
5. 在二次确认窗口确认影响数量。
6. 执行后检查 `apply_room_numbers_*.md` 和 `.csv` 日志。

安全机制：

- 只处理 `Room`。
- 只写入当前编号仍为空的房间。
- 全部修改在一个 Revit Transaction 中，可撤销。

## 16. 如何把报告交给 AI

把导出的 `.md`、`.json`、`.csv` 文件发给 Codex、Claude Code 或 Antigravity，然后可以这样问：

```text
请分析这份 Revit 模型健康报告，按严重程度列出问题。
只给建议，不要生成会直接修改模型的脚本。
```

如果要生成修复脚本，必须先要求 dry-run：

```text
请先生成 dry-run 脚本，只预览会修改哪些元素，不要直接修改模型。
```

## 17. 版权和更新

点击：

```text
YangAgent -> 系统设置
```

版权声明：

```text
由 Yang 开发，工具为 Codex。
```

更新链接：

```text
https://github.com/5788324/Yang-Agent_Revit
```

## 18. 常见问题

### Revit 里看不到 YangAgent

先检查 Revit 里有没有 `pyRevit` 选项卡。

如果没有，说明 pyRevit 还没安装或没有加载。先安装 pyRevit，再安装 YangAgent。

### 按钮都是灰色，提示 availability 或可用性命令载入失败

这是 pyRevit 编译缓存或旧版本目录结构导致的常见问题。

处理步骤：

1. 确认已经更新到最新仓库版本。
2. 关闭 Revit。
3. 删除 pyRevit 缓存中旧的 `YangAgent` 临时 DLL。
4. 重新打开 Revit。
5. 在 pyRevit 中 reload。

本项目已经避免在 `.panel` 和 `.pushbutton` 目录名中使用中文，并移除了 `context:` 可用性声明。

### 点击按钮没有输出文件

检查桌面是否有：

```text
YangAgent_Revit_Exports
```

如果没有，查看 pyRevit 输出窗口里的错误信息。

### 语言不对

运行 `系统设置` 重新选择语言。

## 19. 安全提醒

当前工具不会修改模型。

后续如果增加修复按钮，使用原则是：

1. 先测试模型。
2. 先 dry-run。
3. 确认影响元素数量。
4. 再执行真正修改。
