# revit-context MCP

第一阶段目标：只读查询 Revit 上下文，不修改模型。

计划工具：

- `get_active_document_info`
- `get_active_view_info`
- `export_rooms`
- `export_doors_windows`
- `export_sheets_views`
- `export_model_snapshot`

禁止第一阶段实现：

- `execute_code`
- `delete_elements`
- `save_model`
- `sync_model`
