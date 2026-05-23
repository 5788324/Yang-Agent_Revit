# 数据结构与交互协议 (API & Data Schema)

在 Yang Agent Revit 工作流中，为了保证 AI 与 Revit 之间的稳定通信，所有工具输出的数据必须遵循以下结构规范。

## 1. 导出规范原则

1. **结构化优先**：所有供 AI 读取的数据尽量使用 JSON（对于复杂层级）或 CSV（对于扁平列表数据）。
2. **Key 必须为英文**：无论是中文还是英文模式，JSON/CSV 的字段名称 (Key/Header) 必须保持英文，以防止反序列化错误。
3. **包含唯一标识符**：任何涉及 Revit 元素的输出，必须包含 `ElementId` 字段，作为未来修改的句柄。

## 2. 核心数据结构参考

### 2.1 Dry-Run 修改清单 (CSV)

用于记录“预览操作”中即将受到影响的元素。
格式：`.csv`

| ElementId | Category | ElementName | OldValue | ProposedValue | Status |
| :--- | :--- | :--- | :--- | :--- | :--- |
| 123456 | Doors | 单开门_900x2100 | "" | "D-01" | Missing |
| 789012 | Rooms | 办公室_101 | "" | "101" | Unnumbered |

**说明**：后续的 `apply_*` 脚本将直接读取此 CSV 文件，根据 `ElementId` 查询元素，并将参数更新为 `ProposedValue`。

### 2.2 模型快照 (JSON)

用于生成当前模型的概览状态。
格式：`.json`

```json
{
  "timestamp": "2026-05-23T10:00:00Z",
  "projectInfo": {
    "name": "Sample Project",
    "number": "P-2026-001"
  },
  "statistics": {
    "totalDoors": 150,
    "totalWindows": 300,
    "totalRooms": 50
  },
  "warnings": [
    {
      "type": "UnplacedRoom",
      "elementId": 12345
    }
  ]
}
```

## 3. 报告输出规范

所有由系统自动生成的报告，均输出为 Markdown (`.md`) 格式。
- 必须包含生成时间和执行环境。
- 采用明确的标题层级（H1, H2, H3）。
- 统计数据优先使用表格形式展示。

## 4. 本地设置结构

本地用户设置保存在：

```text
%APPDATA%\YangAgent_Revit\settings.json
```

可配置规则必须保持英文 key。例如视图命名规则：

```json
{
  "view_naming_rules": {
    "prefix_by_view_type": {
      "FloorPlan": ["FP-", "PL-"]
    },
    "temporary_keywords": ["temp", "test", "临时", "测试"]
  }
}
```
