# Claude 文档整合评审

源文档：`C:/Users/YANG/Desktop/Revit-AI-Agent-开发文档.md`

GitHub 仓库：`https://github.com/5788324/Yang-Agent_Revit`

## 1. 当前状态

- GitHub 仓库 `5788324/Yang-Agent_Revit` 已存在，当前是公开仓库。
- 仓库目前基本为空，默认分支是 `main`。
- 当前本地工作区 `D:/codex/Yang Agent_Revit` 还不是 Git 仓库。
- Claude 写的文档内容很完整，适合作为技术蓝图，但不能直接照搬为生产实现方案。

## 2. Claude 文档的价值

Claude 文档覆盖了一个 Revit AI Agent 的完整想象：

- Claude Code / Antigravity 作为 AI 开发入口。
- MCP 作为工具调用层。
- Revit Bridge 作为 Revit 与 AI 的通信桥。
- pyRevit 作为快速脚本执行层。
- C# 插件作为正式插件开发方向。
- Journal 日志作为反馈来源。
- 提示词模板作为 Agent 行为约束。
- 案例覆盖房间编号、视图创建、Excel 导入等高频场景。

这份文档适合作为“愿景说明 + 原型思路库”。真正落地时，需要把它拆成安全、可测试、可维护的阶段。

## 3. 必须修正的关键点

### 3.1 Revit 版本和 .NET 运行时需要分开处理

文档中示例使用 `net6.0-windows`，但不能作为所有 Revit 版本的通用方案。

建议：

- Revit 2022 / 2024：按传统 .NET Framework 插件生态处理。
- Revit 2025+：重点关注 .NET 8 迁移和依赖兼容。
- Revit 2027：单独维护兼容层，不要假设 2025 的代码直接可用。

结论：仓库里应明确拆分 `Revit2022`、`Revit2024`、`Revit2025`、`Revit2027` 适配层。

### 3.2 HTTP Bridge 不能直接执行任意代码

Claude 文档中设计了 `revit_execute`，允许 AI 把代码发给 Revit Bridge 执行。这个方向适合原型验证，但生产环境风险很高。

风险：

- AI 可能生成删除元素、批量修改参数、保存中心文件等高风险操作。
- HTTP 服务如果缺少鉴权和命令白名单，容易被其他本机进程误调用。
- Revit API 必须在 Revit 主线程和合法事务上下文里执行，不能简单从 HTTP 线程直接改模型。

建议：

- 第一阶段只做只读查询，不做模型修改。
- 第二阶段只开放白名单动作，例如导出房间表、导出视图列表。
- 第三阶段才做受控修改，并且必须 dry-run、人工确认、日志记录、Transaction 回滚。
- Bridge 内部必须使用 ExternalEvent 或等价机制把任务切回 Revit API 合法执行上下文。
- 禁止暴露“执行任意 Python/C# 代码”的接口。

### 3.3 MCP 权限要收窄

Claude 文档中的 MCP 配置给了 filesystem、shell、fetch、git 等能力。对个人实验可以，但公司环境要更严格。

建议：

- filesystem 只允许项目仓库、pyRevit extension、临时输出目录。
- shell 不作为默认 MCP 暴露给普通 Agent。
- 写模型的 MCP 工具必须拆成 `preview_*` 和 `apply_*`。
- 所有 `apply_*` 必须要求用户确认。
- 客户模型数据不能默认发到外部服务。

### 3.4 pyRevit 脚本要区分 IronPython 和 CPython

Claude 文档中提到 IronPython 2.7，同时示例里也出现了一些更像现代 Python 的写法。真实使用时要按 pyRevit 版本确认运行时。

建议：

- pyRevit 脚本模板中避免 f-string、类型注解、海象运算符。
- 对中文、CSV、Excel 编码做统一封装。
- 所有脚本先在测试模型运行。
- 优先使用 pyRevit 的 `revit.Transaction` 和 `forms`。

### 3.5 示例代码不能直接当生产代码

Claude 文档里的示例适合说明思路，但有些代码片段需要重写后才能运行。

典型问题：

- Python 示例中出现 C# 风格的 `?.` 空值访问。
- `Room.__class__` 这类写法不适合作为 Revit 房间过滤模板。
- `FilteredElementCollector` 的类别、类、链接模型、视图范围需要更严谨处理。
- Journal 解析可以辅助排错，但不应该作为唯一反馈机制。

建议：把这些示例放入 `samples/concepts/`，不要放入正式工具目录。

### 3.6 Antigravity 相关描述需要降级为“可选平台”

文档中把 Antigravity 描述成 AEC/Revit 优化工具。公司文档里建议更稳妥地写成“可选 AI 开发平台”，避免依赖尚未验证的专有能力。

建议：

- Codex：作为项目代码仓库里的开发执行者。
- Claude Code：作为长上下文方案和代码生成助手。
- Antigravity：作为团队中可选的多 Agent/IDE 工作台。
- 底层仓库、标准、MCP、安全规则统一，前端 AI 平台可以多样。

## 4. 建议采用的整合路线

### 阶段 0：仓库初始化

目标：先把项目变成可协作的 Git 仓库。

建议文件：

```text
README.md
docs/
  revit-ai-agent-project-plan.md
  claude-doc-integration-review.md
  safety-rules.md
  developer-guide.md
standards/
  naming-rules.md
  parameter-rules.md
prompts/
  system/
  task-templates/
pyrevit/
  YangAgent.extension/
mcp/
  revit-context/
  revit-docs/
src/
  YangAgent.Revit.Common/
  YangAgent.Revit2024/
  YangAgent.Revit2025/
samples/
tests/
```

### 阶段 1：只读 pyRevit 工具

先做不修改模型的工具。

建议第一个按钮：

- 导出当前模型基本信息。
- 导出当前视图信息。
- 导出房间列表。
- 导出门窗列表。
- 导出图纸和视图列表。
- 输出 JSON、CSV 或 Excel。

这个阶段目标是让 AI 先“看懂模型”，而不是马上“改模型”。

### 阶段 2：模型快照和报告

把导出的模型数据交给 Codex / Claude 分析。

输出：

- 模型健康报告。
- 缺失参数列表。
- 重复编号列表。
- 未上图视图列表。
- 门窗编号检查。
- 房间编号检查。

### 阶段 3：只读 MCP

实现 `revit_context_mcp`，只提供查询和导出工具。

示例工具：

- `get_active_document_info`
- `get_active_view_info`
- `export_rooms`
- `export_sheets`
- `export_views`
- `export_family_instances`

这一阶段不要提供 `execute_code`。

### 阶段 4：受控修改

只开放少量白名单操作。

示例：

- `preview_room_number_update`
- `apply_room_number_update`
- `preview_parameter_update`
- `apply_parameter_update`
- `preview_view_rename`
- `apply_view_rename`

要求：

- preview 输出影响数量和元素 ID。
- apply 必须人工确认。
- 每次执行写日志。
- 所有修改使用 Transaction。
- 失败必须回滚。

### 阶段 5：正式 C# Bridge

等 pyRevit 和 MCP 工作流稳定后，再开发正式 C# Bridge。

Bridge 只应该接收结构化命令，不应该执行任意代码。

建议命令格式：

```json
{
  "action": "update_parameter",
  "dry_run": true,
  "target": {
    "category": "Rooms",
    "ids": [123, 456]
  },
  "changes": {
    "备注": "大房间"
  }
}
```

## 5. 建议优先落地的功能

第一批功能应选择低风险、高频、容易验证的任务：

1. 导出模型信息。
2. 导出房间表。
3. 导出门窗表。
4. 导出视图和图纸列表。
5. 检查房间编号缺失。
6. 检查门窗编号缺失。
7. 检查未上图视图。
8. 生成模型健康报告。
9. 根据报告生成 pyRevit 修复脚本。
10. dry-run 后人工确认执行。

## 6. 建议下一步

建议先做三件事：

1. 把当前工作区初始化为 Git 仓库，并连接到 `5788324/Yang-Agent_Revit`。
2. 把本文档、项目方案文档、README 推送到 GitHub。
3. 创建第一个 pyRevit 工具：`Export Model Snapshot`，只导出数据，不修改模型。

这样做的好处是：先把团队协作和文档地基搭好，再让 AI 逐步获得读取模型、分析模型、最后受控修改模型的能力。
