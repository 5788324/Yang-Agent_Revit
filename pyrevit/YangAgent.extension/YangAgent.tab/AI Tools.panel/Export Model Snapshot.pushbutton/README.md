# Export Model Snapshot

只读导出当前 Revit 模型快照，供 Codex、Claude Code、Antigravity 或其他 AI 工具分析。

运行时可选择中文或 English。

## 导出内容

- 文档基本信息。
- 当前视图信息。
- Revit 版本。
- 楼层列表。
- 房间列表。
- 门窗列表。
- 视图列表。
- 图纸列表。
- 类别数量摘要。

## 输出位置

默认输出到桌面：

```text
YangAgent_Revit_Exports/
```

每次运行会生成：

- `model_snapshot_YYYYMMDD_HHMMSS.json`
- `rooms_YYYYMMDD_HHMMSS.csv`
- `doors_windows_YYYYMMDD_HHMMSS.csv`
- `sheets_views_YYYYMMDD_HHMMSS.csv`

## 安全说明

此工具不修改模型，不开启 Transaction。
