# 开发指南

## 1. 当前 MVP

当前 MVP 目标是先让 AI 看懂 Revit 模型。第一批工具只读，不修改模型。

优先开发：

1. `Export Model Snapshot`：导出当前模型基本信息。
2. `Model Health Report`：直接生成只读模型健康报告。
3. `Preview Missing Marks`：dry-run 预览缺少标记的门窗。
4. `Export Rooms`：导出房间列表。
5. `Export Doors Windows`：导出门窗列表。
6. `Export Sheets Views`：导出图纸和视图列表。

## 2. pyRevit 开发约定

pyRevit 工具目录：

```text
pyrevit/
  YangAgent.extension/
    YangAgent.tab/
      AI Tools.panel/
        Export Model Snapshot.pushbutton/
          script.py
          bundle.yaml
          README.md
```

脚本要求：

- 兼容 IronPython 2.7 风格。
- 不使用 f-string。
- 不使用 Python 类型注解。
- 不直接修改模型，除非工具明确是 `apply_*`。
- 输出文件统一放到用户桌面 `YangAgent_Revit_Exports`。
- 所有按钮必须提供语言选项：`中文` 和 `English`。
- 用户可见的弹窗、pyRevit 输出、Markdown 报告必须跟随统一语言设置。
- 给 AI 或脚本读取的 JSON key 建议保持稳定英文，避免双语切换破坏自动化解析。

语言设置统一使用：

```python
from yang_agent_lang import get_or_choose_language

lang = get_or_choose_language(forms)
```

## 3. C# 插件开发约定

正式插件源码放在 `src/`。

建议拆分：

```text
src/
  YangAgent.Revit.Common/
  YangAgent.Revit2024/
  YangAgent.Revit2025/
  YangAgent.Revit2027/
```

正式 Bridge 只接收结构化命令，不允许执行任意代码。

## 4. MCP 开发约定

MCP 目录：

```text
mcp/
  revit-context/
  revit-docs/
  company-standards/
```

第一阶段 MCP 只做只读查询和导出。

## 5. 提交前检查

提交前确认：

- 文档链接可读。
- pyRevit 脚本没有 f-string。
- 只读工具没有 Transaction。
- 修改工具必须有 dry-run。
- 没有提交客户模型文件。
- 没有提交密钥或本地配置。
