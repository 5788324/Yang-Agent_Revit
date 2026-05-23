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
- [非程序员路线图](docs/non-programmer-roadmap.md)
- [DLL 插件开发计划](docs/dll-addin-development-plan.md)
- [故障排查](docs/troubleshooting.md)
- [AI 协作开发流程](docs/collaboration-workflow.md)

当前 pyRevit 工具：

- `系统设置`：统一设置语言、简称、头像路径、Light/Dark Theme，并查看版权声明和更新链接。
- `导出报告 -> 导出路径`：设置报告输出目录。
- `导出报告 -> 导出模型快照`：只读导出模型快照。
- `导出报告 -> 模型健康报告`：只读生成模型健康报告。
- `导出报告 -> 预览缺失标记`：dry-run 预览缺少标记的门窗。
- `导出报告 -> 预览缺失房间编号`：dry-run 预览缺少编号的房间。

工具箱支持 `中文` 和 `English`，通过 `系统设置` 设置默认语言。

版权声明：由 Yang 开发，工具为 Codex。

安装 pyRevit extension：

```powershell
.\scripts\install-pyrevit-extension.ps1
```

更新后如果 Revit 仍然加载旧按钮或提示 FullClassName 错误，先关闭 Revit，再执行：

```powershell
.\scripts\install-pyrevit-extension.ps1 -Force -ClearCache
```

注意：如果 Revit 里没有 `pyRevit` 选项卡，请先安装 pyRevit，再安装本项目工具栏。

### 必备开发辅助工具：
- **Revit Lookup**: 进行 Revit API 开发和元素探查的必备工具，请务必安装。
- **pyRevit CLI**: 用于通过命令行管理和重新加载 pyRevit 插件环境。

构建 Revit 2027 DLL 插件骨架：

```powershell
.\scripts\build-revit2027-addin.ps1
```

安装 Revit 2027 `.addin + .dll` 插件骨架：

```powershell
.\scripts\install-revit2027-addin.ps1
```

当前策略：

- `pyrevit/`：快速原型、报告、dry-run。
- `src/` + `addins/`：正式 C# `.addin + .dll` 插件。
