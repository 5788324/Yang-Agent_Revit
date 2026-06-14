# YangAgent Error Codes

本文件只维护当前 MVP 阶段已经使用、或明确保留的错误码。

原则：

- 先保证错误码可读、可定位、可指导下一步；
- 不为了“体系完整”发明大量暂时没用的错误码；
- 新增错误码时，优先补清楚含义和用户动作。

## 1. Apply Missing Room Numbers

| Code | 含义 | 用户动作 |
| --- | --- | --- |
| `YA-APPLY-ROOM-001` | 选择的 CSV 文件名不符合要求 | 重新选择 `missing_room_numbers_*.csv` |
| `YA-APPLY-ROOM-002` | CSV 缺少必要字段 | 重新运行对应 preview 导出 |
| `YA-APPLY-ROOM-003` | `element_id` 无效 | 不要继续 apply，检查 CSV 是否被手改 |
| `YA-APPLY-ROOM-004` | Revit 找不到对应元素 | 重新生成 dry-run CSV |
| `YA-APPLY-ROOM-005` | 找不到房间编号参数 | 检查模型中的房间参数配置 |
| `YA-APPLY-ROOM-006` | 房间编号参数只读 | 跳过该元素，人工处理 |
| `YA-APPLY-ROOM-007` | CSV 中存在重复 `element_id` | 不要 apply，重新生成 dry-run CSV |

## 2. Apply Missing Door Window Marks

| Code | 含义 | 用户动作 |
| --- | --- | --- |
| `YA-APPLY-MARK-001` | 选择的 CSV 文件名不符合要求 | 重新选择 `missing_door_window_marks_*.csv` |
| `YA-APPLY-MARK-002` | CSV 缺少必要字段 | 重新运行对应 preview 导出 |
| `YA-APPLY-MARK-003` | `element_id` 无效 | 不要继续 apply，检查 CSV 是否被手改 |
| `YA-APPLY-MARK-004` | Revit 找不到对应元素 | 重新生成 dry-run CSV |
| `YA-APPLY-MARK-005` | 找不到 Mark/标记参数 | 检查族或参数配置 |
| `YA-APPLY-MARK-006` | Mark/标记参数只读 | 跳过该元素，人工处理 |
| `YA-APPLY-MARK-007` | CSV 中存在重复 `element_id` | 不要 apply，重新生成 dry-run CSV |

## 3. 离线 CSV 校验

这些错误码来自：

```text
tools\validate_apply_csv.py
```

它们表示输入文件不合格，不表示 Revit 已经改动模型。

| Code | 含义 | 用户动作 |
| --- | --- | --- |
| `YA-APPLY-ROOM-CSV-001` / `YA-APPLY-MARK-CSV-001` | CSV 文件不存在 | 检查路径 |
| `YA-APPLY-ROOM-CSV-002` / `YA-APPLY-MARK-CSV-002` | 文件名不匹配预期 | 使用 preview 生成的原始 CSV |
| `YA-APPLY-ROOM-CSV-003` / `YA-APPLY-MARK-CSV-003` | CSV 读取失败 | 检查编码、损坏或占用情况 |
| `YA-APPLY-ROOM-CSV-004` / `YA-APPLY-MARK-CSV-004` | 缺少必要字段 | 重新运行 preview |
| `YA-APPLY-ROOM-CSV-006` / `YA-APPLY-MARK-CSV-006` | `element_id` 无效 | 不要 apply，重新导出 |
| `YA-APPLY-ROOM-CSV-007` / `YA-APPLY-MARK-CSV-007` | `element_id` 重复 | 不要 apply，重新导出 |
| `YA-APPLY-ROOM-CSV-008` / `YA-APPLY-MARK-CSV-008` | `dry_run` 不是 `true` | 不要 apply，重新导出 |
| `YA-APPLY-ROOM-CSV-009` / `YA-APPLY-MARK-CSV-009` | `category` 不匹配 | 不要 apply，检查 CSV 来源 |
| `YA-APPLY-ROOM-CSV-010` / `YA-APPLY-MARK-CSV-010` | 建议值为空 | 先人工补全，或重新导出 |
| `YA-APPLY-ROOM-CSV-012` / `YA-APPLY-MARK-CSV-012` | 没有可应用的记录 | 不需要 apply，或 CSV 不适合 apply |

## 4. C# DLL 构建与安装

| Code | 含义 | 用户动作 |
| --- | --- | --- |
| `YA-CS-BUILD-LOCKED-DLL` | Revit 正在锁定 DLL，无法覆盖 | 关闭 Revit 2027 后重试 |
| `YA-CS-VERSION-PLANNED` | 目标版本仍是计划态，尚未实现 | 当前只按已落地版本执行，不要误判为构建失败 |
| `YA-CS-PROJECT-MISSING` | 对应 C# 项目不存在 | 检查 `src/YangAgent.Revit20xx` |
| `YA-CS-ADDIN-TEMPLATE-MISSING` | 对应 `.addin` 模板不存在 | 检查 `addins/Revit20xx` |
| `YA-CS-DLL-MISSING` | 构建后找不到 DLL | 先看 `dotnet build` 输出 |

## 5. C# DLL 启动

| Code | 含义 | 用户动作 |
| --- | --- | --- |
| `YA-CS-STARTUP-001` | DLL 启动失败 | 先确认 Revit 版本、安装路径、弹窗原文，再继续排查 |

## 6. 使用规则

看到错误码时，优先这样做：

1. 先记下完整错误码，不要只记中文描述。
2. 再记下触发按钮、测试模型、CSV 文件名或报告路径。
3. 如果是 apply 类问题，先停在预览和日志层，不要继续反复改模型。
4. 如果本文件没有对应错误码，再补到主线文档，而不是只留在聊天记录里。
