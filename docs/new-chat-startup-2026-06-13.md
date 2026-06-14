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
- 不要再回到 D 盘旧路径开发。
- 不要删除 D 盘旧路径，除非用户明确确认。
- 不要直接修改生产 Revit 模型。
- 所有模型修改功能必须严格走：preview/dry-run -> human confirmation -> apply -> log -> Undo note

开工先做：
1. git status --short --branch
2. git log -3 --oneline
3. 如果工作区是干净的，再执行 git pull
4. 读取 docs/framework/daily-ops-routine.md
5. 读取 docs/handoff-new-chat-2026-06-07.md
6. 读取 docs/next-steps.md
7. 读取 docs/worklogs/worklog-2026-06-13.md 最新相关部分
8. 读取 docs/reviews/gemini-toolbox-initial-inventory-2026-06-13.md

当前状态：
- 远程仓库：https://github.com/5788324/Yang-Agent_Revit
- 当前主分支：main
- Gemini 工具箱路径：G:\Codex\YangAgent Revit\YangAgent Revit\Gemini 资料\YangTools_SourceCode
- Gemini 资料已在 .git/info/exclude 中排除，不要提交

当前最高优先级：
先把 YangAgent 主体落地，让 pyRevit MVP 能在 sandbox Revit 模型里稳定干活。

当前不要做：
- 不要迁移 Gemini 工具箱整套实现
- 不要扩 MCP、微工具箱、项目资产管理器
- 不要重构 C# 大框架
- 不要处理企业化或商业化规划

Gemini 决策：
- Gemini 工具箱功能重要，但当前实现质量不作为主线直接合并依据
- 后续只按 YangAgent 安全规则重写纳入
- 现在只把它当功能素材库和后续迁入池

继续主线：
1. 先跑离线验证：
   python tools\check_pyrevit_extension.py
   python tools\run_sandbox_preflight.py --write-report
   python tools\static_checks.py --write-report
2. 检查 sandbox runbook / checklist / feedback template 是否足够让真人照跑
3. 优先准备 live sandbox Revit 验证
4. 如果没有 live 反馈，不要扩功能，只修文档或预检 blocker

文档和交接规则：
- 每天开始和结束都要更新 worklog / next-steps / new-chat-startup
- 任何外部 AI 交付都必须带 delivery report 和 operation log
- 相关规则文档：
  docs/framework/daily-ops-routine.md
  docs/agent-development-rules.md
  docs/agent-task-template.md
  docs/agent-delivery-report-template.md
  docs/agent-review-checklist.md
```

## Current Migration Verification

Verified on 2026-06-13:

- `G:\Codex\YangAgent Revit\YangAgent Revit` is a Git repository.
- `main` tracks `origin/main`.
- `git status --short --branch` showed `main...origin/main`.
- `Gemini 资料/` is ignored by `.git/info/exclude`.
- Previous D path is clean and retained only as a safety backup.

## Daily Handoff Rule

Added on 2026-06-13:

- Start with Git status/log and core-doc refresh.
- Pull only when the tree is safe.
- End with worklog, next-steps, startup prompt, and a safe Git checkpoint.
