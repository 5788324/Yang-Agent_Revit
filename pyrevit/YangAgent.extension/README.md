# YangAgent pyRevit Extension

公司内部 Revit AI Agent 工具栏。

当前按钮：

- `Language Settings`：设置默认语言。
- `Export Model Snapshot`：只读导出模型快照。
- `Model Health Report`：只读生成模型健康报告。
- `Preview Missing Marks`：dry-run 预览缺少标记的门窗。

工具箱支持：

- 中文
- English

默认语言通过 `Language Settings` 设置。

安全原则：

- 默认只读。
- 不修改模型。
- 不开启 Transaction。
- 输出文件写入桌面 `YangAgent_Revit_Exports`。
