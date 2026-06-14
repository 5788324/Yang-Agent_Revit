# Hermes / DeepSeek 实施包 - 2026-06-13

这份文档给 `Hermes` 和它可能调用的 `DeepSeek` 使用。目标不是让你们参与架构决策，而是在已经确定的 YangAgent 边界内，完成小范围、可审查、可替换的按钮实现草稿。

## 1. 当前目标

当前主线目标只有一个：

- 让 `YangAgent` 的 pyRevit MVP 在 sandbox Revit 模型里稳定跑通。

当前不要做：

- 不要扩展新产品线。
- 不要把 `Gemini` 当第二主产品维护。
- 不要重做主题系统。
- 不要大改 `lib`。
- 不要碰 C# 主框架。

## 2. 权威路径

- 主开发仓：`G:\Codex\YangAgent Revit\YangAgent Revit`
- Hermes 工作目录：`G:\Hermes Agent\YangAgent Revit\YangAgent Revit`
- 不要回到旧路径：`D:\codex\Yang Agent_Revit`

## 3. 角色边界

`Codex` 负责：

- 架构边界
- 共享主题与设置
- 安全规则
- 最终审查
- Revit live 验证
- 合并决定

`Hermes / DeepSeek` 只负责：

- 指定按钮目录内的脚本草稿
- 低风险 UI 文案整理
- bundle 标题/tooltip 微调
- delivery report
- 离线自检结果整理

## 4. 禁止触碰

除非任务单单独授权，否则不要修改这些路径：

- `pyrevit/YangAgent.extension/lib/`
- `docs/design-system/`
- `docs/framework/`
- `docs/governance/`
- 任何不属于你本次 ownership 的 `.pushbutton/`

也不要做这些事：

- 不要新增独立配色系统
- 不要写死一套 Gemini 风格 UI
- 不要发明新的命名体系
- 不要做跨按钮的大重构
- 不要声称“已 live 可用”除非有 Revit 实测证据

## 5. 可复用共享库

优先复用现有共享库，不要自己再造一套：

- `pyrevit/YangAgent.extension/lib/yang_agent_theme.py`
- `pyrevit/YangAgent.extension/lib/yang_agent_settings.py`
- `pyrevit/YangAgent.extension/lib/yang_agent_report_style.py`
- `pyrevit/YangAgent.extension/lib/yang_agent_lang.py`
- `pyrevit/YangAgent.extension/lib/yang_agent_apply.py`

最低使用规则：

- 报告导出目录：走 `get_export_dir()`
- 当前主题：走 `get_theme_id()`
- Markdown 报告头/状态块：走 `build_intro_block()`、`build_status_block()`
- 语言：优先走 `get_or_choose_language()`
- apply 类 CSV 读取、确认、结果统计：优先走 `yang_agent_apply.py`

不要主动修 `yang_agent_lang.py` 里的历史编码问题，除非 Codex 单独下任务。

## 6. 按钮类型合同

### 6.1 Report 类按钮

要求：

- 只读
- 输出到 `get_export_dir()`
- 文件名稳定、英文机器名、带时间戳
- Markdown 正文可中文，但字段和文件名前缀保持稳定
- 使用共享 report style

### 6.2 Preview 类按钮

要求：

- 只读 dry-run
- 不开启 `Transaction`
- 输出问题数量
- 输出 `ElementId`
- 输出足够人工判断的信息
- 明确写出“这是候选/审查结果，不代表直接可 apply”

### 6.3 Apply 类按钮

硬规则：

`preview -> confirmation -> apply -> log -> Undo note`

最低要求：

- 先读取 preview CSV
- 校验文件名前缀和字段
- 校验重复 `element_id`
- 显示影响数量
- 明确提示当前模型名
- 用户确认后才进入 apply
- 输出结果 CSV 或 Markdown 日志
- 结尾说明 Undo 是否已实际验证

## 7. 当前优先任务

如果你的工作目录还没跟上最新主线，不要重做已经完成或已在审查中的按钮。优先只做这 3 个：

1. `ApplyMissingDoorWindowMarks.pushbutton`
2. `ApplyMissingRoomNumbers.pushbutton`
3. `ModelHealthReport.pushbutton`

补充说明：

- `SystemSettings` 已在 live Revit 打开验证过。
- `ProjectInfoReport` 已在 live Revit 导出成功。
- `ExportAIReviewPrompt` 已在 live Revit 点测成功。
- 一批 report/preview 按钮已经在主线审查中，Hermes 不要重复造轮子。

如果你打算做别的按钮，必须先在交付说明里写清楚为什么没有和当前主线冲突。

## 8. 推荐实现模式

### 8.1 ApplyMissingDoorWindowMarks

目标：

- 从 preview CSV 读取缺失门窗标记候选
- 仅对空 mark 元素尝试填值
- 已有 mark 的元素必须 `skipped`

输出最少字段建议：

- `element_id`
- `category`
- `current_mark`
- `proposed_mark`
- `result`
- `message`

### 8.2 ApplyMissingRoomNumbers

目标：

- 从 preview CSV 读取缺失房间编号候选
- 仅对空房间编号尝试填值
- 对不可写、已存在、找不到元素的情况显式记录

输出最少字段建议：

- `element_id`
- `level`
- `room_name`
- `current_number`
- `proposed_number`
- `result`
- `message`

### 8.3 ModelHealthReport

目标：

- 汇总当前 MVP 已有预览结果的高层摘要
- 可以是单按钮扫描，不要求依赖其他按钮已先运行
- 输出 Markdown 为主

建议章节：

- Project info
- View naming issues
- Missing room numbers
- Duplicate room numbers
- Missing door/window marks
- Unplaced view candidates
- Risk notes
- Next actions

## 9. 交付格式

每次交付必须带一个 Markdown 说明，最少包含：

- task name
- agent name
- date
- changed files
- each file changed for what reason
- offline validation run
- skipped validation
- whether model changes are involved
- whether `preview -> confirmation -> apply -> log -> Undo note` is satisfied
- known risks
- next recommendation

推荐命名：

- `2026-06-13_hermes_apply-room-numbers_delivery-report.md`
- `2026-06-13_hermes_model-health-report_delivery-report.md`

## 10. 离线自检

允许优先跑这些：

```powershell
python tools\check_pyrevit_extension.py
python tools\static_checks.py --write-report
python -m py_compile <target script paths>
```

注意：

- 如果 `py_compile` 因 `__pycache__` 权限或环境原因失败，不要假装通过。
- 把“没跑成”和“跑过但失败”分开写。
- 没有 live Revit 证据时，只能写“offline checked”。

## 11. 文案与实现要求

- 用户可见文案默认中英双语或中文优先
- 面向用户的错误信息要能让初学者看懂
- 机器字段保持英文稳定
- 保持 IronPython 2.7 兼容
- 不要用 f-string
- 不要用类型注解
- 不要引入只在 CPython 3 才稳的语法

## 12. 提交前自问

- 我有没有碰共享 `lib`？
- 我有没有改到不属于我的按钮？
- 这是只读按钮还是改模型按钮？
- 如果改模型，是否完整覆盖 `preview -> confirmation -> apply -> log -> Undo note`？
- 我的输出路径是不是统一走 `get_export_dir()`？
- 我的报告样式是不是统一走共享 theme/report helper？
- 我有没有把未验证项写清楚？

## 13. 需要立即回报 Codex 的情况

遇到这些情况，不要自己拍脑袋继续：

- 需要改共享 `lib`
- 需要新增设置字段
- 需要改主题 token
- 需要改窗口 XAML
- 需要跨多个按钮重构
- 发现主线按钮已被别人实现
- 发现现有共享函数不够用，必须扩接口
- 发现 live Revit 行为和离线预期明显冲突

## 14. 最终原则

你交付的是“可审查草稿”，不是“自定架构后的成品”。

只要做到这三点，这次交付就是合格方向：

- 改动边界小
- 输出和风险说清楚
- 方便 Codex 接手审查和修正
