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
| `YA-APPLY-ROOM-007` | CSV 中有重复 `element_id` | 不要 apply，重新生成 dry-run CSV |

## Offline Apply CSV Validation

These codes are emitted by `tools\validate_apply_csv.py`; they do not mean Revit was modified.

| Code | Meaning | User action |
| --- | --- | --- |
| `YA-APPLY-ROOM-CSV-001` / `YA-APPLY-MARK-CSV-001` | CSV 文件不存在 | 检查路径 |
| `YA-APPLY-ROOM-CSV-002` / `YA-APPLY-MARK-CSV-002` | 文件名不匹配 | 选择对应 preview 生成的 CSV |
| `YA-APPLY-ROOM-CSV-003` / `YA-APPLY-MARK-CSV-003` | CSV 读取失败 | 检查文件编码或是否损坏 |
| `YA-APPLY-ROOM-CSV-004` / `YA-APPLY-MARK-CSV-004` | 缺少必要字段 | 重新运行 preview |
| `YA-APPLY-ROOM-CSV-006` / `YA-APPLY-MARK-CSV-006` | `element_id` 无效 | 不要 apply，重新导出 |
| `YA-APPLY-ROOM-CSV-007` / `YA-APPLY-MARK-CSV-007` | `element_id` 重复 | 不要 apply，重新导出 |
| `YA-APPLY-ROOM-CSV-008` / `YA-APPLY-MARK-CSV-008` | `dry_run` 不是 `true` | 不要 apply，重新导出 |
| `YA-APPLY-ROOM-CSV-009` / `YA-APPLY-MARK-CSV-009` | `category` 不匹配 | 不要 apply，检查 CSV 来源 |
| `YA-APPLY-ROOM-CSV-010` / `YA-APPLY-MARK-CSV-010` | 建议值为空 | 不要 apply，先人工补全或重新导出 |
| `YA-APPLY-ROOM-CSV-012` / `YA-APPLY-MARK-CSV-012` | 没有可应用行 | 不需要 apply 或 CSV 不适合 apply |

## Apply Missing Door Window Marks

| Code | Meaning | User action |
| --- | --- | --- |
| `YA-APPLY-MARK-001` | 选择的 CSV 文件名不符合要求 | 选择 `missing_door_window_marks_*.csv` |
| `YA-APPLY-MARK-002` | CSV 缺少必要字段 | 重新运行 `预览缺失标记` |
| `YA-APPLY-MARK-003` | `element_id` 无效 | 检查 CSV 是否被手工改坏 |
| `YA-APPLY-MARK-004` | Revit 找不到对应元素 | 重新生成 dry-run CSV |
| `YA-APPLY-MARK-005` | 找不到 Mark/标记参数 | 检查族或参数 |
| `YA-APPLY-MARK-006` | Mark/标记参数只读 | 跳过该元素，人工处理 |
| `YA-APPLY-MARK-007` | CSV 中有重复 `element_id` | 不要 apply，重新生成 dry-run CSV |

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
