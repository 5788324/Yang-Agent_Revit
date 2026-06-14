# revit-context MCP

当前状态：占位目录，尚未进入主线实现。

## 当前定位

这是未来 `revit-context` MCP 方向的保留目录。

当前项目不以 MCP 为本周交付目标。当前主线仍然是：

```text
pyRevit MVP usable in a sandbox model
```

## 以后如果恢复实现

第一阶段只应做只读能力，例如：

- `get_active_document_info`
- `get_active_view_info`
- `export_rooms`
- `export_doors_windows`
- `export_sheets_views`
- `export_model_snapshot`

明确禁止直接做：

- `execute_code`
- `delete_elements`
- `save_model`
- `sync_model`

## 当前约束

如果以后进入 MCP：

- 先读，不先写
- preview 和 apply 分离
- 不暴露任意代码执行
- 不绕开现有 safety / governance 规则
