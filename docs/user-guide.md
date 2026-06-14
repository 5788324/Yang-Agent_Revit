# 用户使用指南

这份文档面向当前个人使用场景。

如果你只关心“现在能点什么、会不会改模型、先怎么测”，看这份就够了。

## 1. 这套工具现在是做什么的

当前 `YangAgent` 主要做三件事：

1. 导出模型信息
2. 生成检查报告
3. 先预览，再谨慎执行低风险修改

当前不是：

- 全自动 AI 改模系统
- 企业平台
- 正式生产环境批量修改工具

## 2. 当前工具入口

Revit 里当前主要看：

- `YangAgent -> System Settings`
- `YangAgent -> Reports`

## 3. System Settings 能做什么

`System Settings` 当前负责：

- 语言设置：中文 / English
- 主题预设选择
- 用户昵称和头像路径
- AI 工作偏好
- 公司标准文档路径
- 视图命名规则
- 报告导出路径相关设置入口

当前主题预设：

- `YangAgent Core`
- `Toolbox Warm`
- `Dark Pro`

## 4. Reports 里有哪些按钮

当前主线按钮包括：

- `Project Info Report`
- `Report Export Path`
- `Export Model Snapshot`
- `Model Health Report`
- `Export Regression Checklist`
- `Export AI Review Prompt`
- `Preview Missing Marks`
- `Preview Missing Room Numbers`
- `Preview Duplicate Room Numbers`
- `Preview Unplaced Views`
- `Preview View Naming Rules`
- `Apply Missing Door Window Marks`
- `Apply Missing Room Numbers`

## 5. 哪些按钮不会改模型

这些按钮默认只读：

- `Project Info Report`
- `Report Export Path`
- `Export Model Snapshot`
- `Model Health Report`
- `Export Regression Checklist`
- `Export AI Review Prompt`
- 所有 `Preview ...` 按钮

只读工具会：

- 读取模型信息
- 导出 Markdown / CSV / JSON

只读工具不会：

- 修改模型参数
- 删除元素
- 创建元素

## 6. 哪些按钮会改模型

当前只有这两个按钮属于 apply：

- `Apply Missing Door Window Marks`
- `Apply Missing Room Numbers`

它们都应该按这个顺序使用：

```text
先运行对应 Preview -> 检查 CSV -> 再运行 Apply -> 再测 Undo
```

## 7. 第一次使用建议顺序

第一次不要直接点 apply。

推荐顺序：

1. 打开测试模型
2. 打开 `System Settings`
3. 确认语言和导出目录
4. 运行 `Project Info Report`
5. 运行 `Export Model Snapshot`
6. 运行 `Model Health Report`
7. 运行各个 `Preview ...` 按钮
8. 只有在 preview 结果合理后，再测试 apply

## 8. 推荐测试模型

不要直接拿正式项目试。

当前推荐测试模型：

```text
G:\Codex\YangAgent Revit\YangAgent Revit\Gemini 资料\Revit 测试模型\Snowdon Towers Sample Architectural_sandbox.rvt
```

## 9. 报告保存到哪里

当前报告目录建议设到：

```text
G:\Codex\YangAgent Revit\YangAgent Revit\Gemini 资料\Revit 测试模型\报告
```

你也可以通过：

```text
YangAgent -> Reports -> Report Export Path
```

来改导出位置。

## 10. Apply 工具怎么安全使用

### 10.1 门窗标记

先运行：

```text
Preview Missing Marks
```

检查生成的 `missing_door_window_marks_*.csv` 后，再运行：

```text
Apply Missing Door Window Marks
```

### 10.2 房间编号

先运行：

```text
Preview Missing Room Numbers
```

检查生成的 `missing_room_numbers_*.csv` 后，再运行：

```text
Apply Missing Room Numbers
```

不要把别的 CSV 误拿去 apply。

## 11. 出问题先看什么

如果按钮灰掉、点了报错、没出文件，先看：

- `docs/troubleshooting.md`
- `docs/error-codes.md`
- `docs/sandbox-pyrevit-mvp-checklist.md`

## 12. 当前最重要的安全提醒

- 只在 sandbox / test 模型里试
- 先 preview，后 apply
- apply 后立刻测一次 Undo
- 没看懂结果时先别继续

## 13. 相关文档

- `README.md`
- `docs/safety-rules.md`
- `docs/sandbox-pyrevit-mvp-checklist.md`
- `docs/sandbox-pyrevit-mvp-runbook.md`
- `docs/troubleshooting.md`
