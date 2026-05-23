# YangAgent pyRevit Extension

公司内部 Revit AI Agent 工具栏。

当前功能区：

系统设置：

- `系统设置`：统一设置语言、简称、头像路径、Light / Dark Theme，并查看版权声明和更新链接。

导出报告：

- `导出路径`：设置报告输出目录。
- `导出模型快照`：只读导出模型快照。
- `模型健康报告`：只读生成模型健康报告。
- `预览缺失标记`：dry-run 预览缺少标记的门窗。

工具箱支持：

- 中文
- English

默认语言通过 `系统设置` 设置。

安全原则：

- 默认只读。
- 不修改模型。
- 不开启 Transaction。
- 输出文件写入桌面 `YangAgent_Revit_Exports`。
