# New Chat Startup - 2026-06-13

Use this prompt when starting the next Codex chat.

## Copy This Prompt

```text
我们继续 YangAgent Revit 项目。请用中文回答。

当前主路径：
G:\Codex\YangAgent Revit\YangAgent Revit

旧路径：
D:\codex\Yang Agent_Revit

重要规则：
- G 盘路径已经完成迁移，是当前唯一主开发路径。
- 不要再在 D 盘旧路径开发。
- 不要删除 D 盘旧路径，除非用户明确确认。
- 不要直接修改生产 Revit 模型。
- 所有模型修改功能必须 preview/dry-run -> human confirmation -> apply -> log -> Undo note。

请先运行：
1. git status --short --branch
2. git log -3 --oneline
3. 读取 docs/handoff-new-chat-2026-06-07.md
4. 读取 docs/next-steps.md
5. 读取 docs/worklogs/worklog-2026-06-13.md 最新部分
6. 读取 docs/reviews/gemini-toolbox-initial-inventory-2026-06-13.md

当前状态：
- 远端仓库：https://github.com/5788324/Yang-Agent_Revit
- 当前主分支：main
- 最近已推送提交：d3357e4 docs: prioritize core MVP before Gemini migration
- Gemini 工具箱路径：G:\Codex\YangAgent Revit\YangAgent Revit\Gemini 资料\YangTools_SourceCode
- Gemini 资料已在 .git/info/exclude 中排除，不要提交。

当前最高优先级：
先把 YangAgent 主体落地，让 pyRevit MVP 能在 sandbox Revit 模型里干活。

当前不要做：
- 不要迁移 Gemini 工具箱功能实现。
- 不要扩 MCP、微工具箱、项目资产管理器。
- 不要重构 C# 大框架。
- 不要处理企业级/商业化规划。

Gemini 决策：
- Gemini 工具箱功能都重要，尤其 MCP、微工具箱、项目资产管理器。
- 但 Gemini 当前实现工程质量不合格。
- 后续要纳入管理并按 YangAgent 安全规则重写。
- 现在只保留为功能素材库和后续迁入池。

请继续主线：
1. 先跑离线验证：
   python tools\check_pyrevit_extension.py
   python tools\run_sandbox_preflight.py --write-report
   python tools\static_checks.py --write-report
2. 检查 sandbox runbook/checklist/feedback template 是否足够让真人照跑。
3. 准备第一次 live sandbox Revit 验证。
4. 如果没有 live 反馈，不要扩功能，只修文档或预检 blocker。

Hermes/Gemini/DeepSeek 协作规则：
- 可以写代码和插件草稿，但必须有任务单和交付报告。
- 不能直接合并。
- Codex 负责最终审查、合并和质量门禁。
- 相关文档：docs/agent-development-rules.md、docs/agent-task-template.md、docs/agent-delivery-report-template.md、docs/agent-review-checklist.md。
```

## Current Migration Verification

Verified on 2026-06-13:

- `G:\Codex\YangAgent Revit\YangAgent Revit` is a Git repository.
- `main` tracks `origin/main`.
- `git status --short --branch` showed `main...origin/main`.
- `Gemini 资料/` is ignored by `.git/info/exclude`.
- Previous D path is clean and retained only as a safety backup.

## Next Human Decision

Before deleting the old D path, the user should confirm the G path works in normal daily use.
