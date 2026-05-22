# Yang Agent Revit

## 项目目标

本项目用于构建公司内部 Revit AI Agent 工作流，帮助用户通过 Codex、Claude Code、Antigravity、MCP、pyRevit 和 Revit API 开发插件、分析模型、生成工具，并在安全边界内执行受控自动化。

## 当前阶段

当前处于 MVP 阶段：优先实现只读模型数据导出、模型快照分析、报告生成和 pyRevit 工具原型。

## Revit 版本

目标版本：

- Revit 2022
- Revit 2024
- Revit 2025
- Revit 2027

版本策略：

- Revit 2022 / 2024：优先考虑传统 .NET Framework 插件生态和 pyRevit。
- Revit 2025+：注意 .NET 8 迁移和依赖兼容。
- Revit 2027：单独验证，不默认假设旧版本代码直接兼容。

## 安全规则

1. 第一阶段只做只读导出，不修改模型。
2. 所有模型修改必须先 dry-run。
3. 所有批量修改必须显示影响元素数量和 ElementId。
4. 所有修改必须使用 Transaction。
5. 禁止无确认删除元素。
6. 禁止无确认修改中心文件或云模型。
7. 禁止在 Bridge/MCP 中暴露任意代码执行接口。
8. 客户模型数据不得默认发送到未经批准的外部服务。

## pyRevit 规则

- 脚本应兼容 IronPython 2.7 风格。
- 避免 f-string、类型注解、walrus 运算符。
- 中文输出和 CSV/JSON 编码要显式处理。
- 使用 `pyrevit.revit`、`pyrevit.forms`、`pyrevit.script`。
- 修改模型时使用 `with revit.Transaction(...)`。

## 推荐工作流

1. 用户提出需求。
2. Agent 判断是否需要读取模型上下文。
3. 优先生成只读导出或 dry-run 脚本。
4. 用户确认影响范围。
5. 再生成可执行修改脚本。
6. 在测试模型验证。
7. 写日志和使用说明。

## 重要目录

- `docs/`：项目文档。
- `standards/`：公司 BIM 标准。
- `prompts/`：提示词模板。
- `pyrevit/`：pyRevit 工具栏和脚本。
- `mcp/`：MCP 服务原型。
- `src/`：正式 C# 插件源码。
- `samples/`：示例和概念验证代码。
- `tests/`：测试和验证脚本。
