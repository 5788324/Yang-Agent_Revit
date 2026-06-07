# YangAgent Error Codes

当前只维护个人版 MVP 需要的最小错误代码。遇到新错误时，先补充清晰说明，不做复杂错误系统。

## Apply Missing Room Numbers

| Code | Meaning | User action |
| --- | --- | --- |
| `YA-APPLY-ROOM-001` | 选择的 CSV 文件名不符合要求 | 选择 `missing_room_numbers_*.csv` |
| `YA-APPLY-ROOM-002` | CSV 缺少必要字段 | 重新运行 `预览缺失房间编号` |
| `YA-APPLY-ROOM-003` | `element_id` 无效 | 检查 CSV 是否被手工改坏 |
| `YA-APPLY-ROOM-004` | Revit 找不到对应元素 | 重新生成 dry-run CSV |
| `YA-APPLY-ROOM-005` | 找不到房间编号参数 | 检查模型房间参数 |
| `YA-APPLY-ROOM-006` | 房间编号参数只读 | 跳过该房间，人工处理 |

## Apply Missing Door Window Marks

| Code | Meaning | User action |
| --- | --- | --- |
| `YA-APPLY-MARK-001` | 选择的 CSV 文件名不符合要求 | 选择 `missing_door_window_marks_*.csv` |
| `YA-APPLY-MARK-002` | CSV 缺少必要字段 | 重新运行 `预览缺失标记` |
| `YA-APPLY-MARK-003` | `element_id` 无效 | 检查 CSV 是否被手工改坏 |
| `YA-APPLY-MARK-004` | Revit 找不到对应元素 | 重新生成 dry-run CSV |
| `YA-APPLY-MARK-005` | 找不到 Mark/标记参数 | 检查族或参数 |
| `YA-APPLY-MARK-006` | Mark/标记参数只读 | 跳过该元素，人工处理 |

## C# DLL Build

| Code | Meaning | User action |
| --- | --- | --- |
| `YA-CS-BUILD-LOCKED-DLL` | Revit 正在锁定 DLL，无法覆盖 | 关闭 Revit 2027 后重新构建 |
| `YA-CS-VERSION-PLANNED` | 选择的 Revit DLL 版本还只是计划 | 当前只构建/安装 Revit 2027；等待对应版本项目创建 |
| `YA-CS-PROJECT-MISSING` | C# 项目文件不存在 | 检查 `src/YangAgent.Revit20xx` 是否已创建 |
| `YA-CS-ADDIN-TEMPLATE-MISSING` | `.addin` 模板不存在 | 检查 `addins/Revit20xx` 是否已创建 |
| `YA-CS-DLL-MISSING` | 构建后找不到 DLL | 先查看 `dotnet build` 输出 |
## C# DLL Startup

| Code | Meaning | User action |
| --- | --- | --- |
| `YA-CS-STARTUP-001` | DLL 启动失败 | 查看弹窗中的异常信息，先确认 Revit 版本和 DLL 安装路径 |
