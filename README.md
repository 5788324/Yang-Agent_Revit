# Yang Agent Revit

本仓库用于规划和逐步实现公司内部 Revit AI Agent 工作流。

当前主文档：

- [Revit AI Agent 项目方案](docs/revit-ai-agent-project-plan.md)
- [Claude 文档整合评审](docs/claude-doc-integration-review.md)
- [用户使用指南](docs/user-guide.md)
- [开发指南](docs/developer-guide.md)
- [安全规则](docs/safety-rules.md)
- [下一步工作清单](docs/next-steps.md)
- [同事快速使用说明](docs/colleague-quickstart.md)
- [语言策略](docs/language-strategy.md)

当前 pyRevit 工具：

- `Language Settings`：设置默认语言。
- `Export Model Snapshot`：只读导出模型快照。
- `Model Health Report`：只读生成模型健康报告。
- `Preview Missing Marks`：dry-run 预览缺少标记的门窗。

工具箱支持 `中文` 和 `English`，通过 `Language Settings` 设置默认语言。

安装 pyRevit extension：

```powershell
.\scripts\install-pyrevit-extension.ps1
```

注意：如果 Revit 里没有 `pyRevit` 选项卡，请先安装 pyRevit，再安装本项目工具栏。
