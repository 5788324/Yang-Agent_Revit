# YangAgent Revit New Chat Handoff - 2026-06-07

本文件用于上下文压缩后的新对话接手。

它保留当前主线脉络，但不再单独承担全部日常启动职责。每日启动请同时读最新 startup、next-steps、worklog。

## 当前权威顺序

文档冲突时，优先级如下：

1. `README.md`
2. `docs/product-brief.md`
3. `docs/project-rules.md`
4. `docs/framework/daily-ops-routine.md`
5. `docs/new-chat-startup-2026-06-13.md`
6. `docs/next-steps.md`
7. 最新相关 `docs/worklogs/worklog-YYYY-MM-DD.md`
8. 本 handoff

旧的公司化、平台化、MCP-first、Bridge-first 规划都视为历史参考。

## 仓库状态

- 仓库：`https://github.com/5788324/Yang-Agent_Revit`
- 当前本地路径：`G:\Codex\YangAgent Revit\YangAgent Revit`
- 旧路径：`D:\codex\Yang Agent_Revit`
- 路径迁移状态：已完成，当前主线以 G 盘仓库为准
- 删除警告：没有用户明确确认前，不要删除旧 D 盘目录
- 默认分支：`main`
- Git 规则：默认不主动 push；只有真实检查点、跨天收尾或用户明确要求时再 push

## 当前产品定位

- 个人自用 Revit AI 助手
- 不是企业平台
- 不是商业化插件产品
- 当前主实现层：pyRevit
- C# DLL 目前只保留轻量轨道，不是当前交付主线

## 当前阶段目标

本周硬目标：

```text
Make the pyRevit MVP usable in a sandbox Revit model.
```

展开说明：

- 先把 YangAgent 核心 pyRevit 工作流跑通
- 先以 sandbox 模型中的只读导出、preview、低风险 apply 为主
- 所有模型修改工具都必须遵守：

```text
preview / dry-run -> human confirmation -> apply -> log -> Undo check
```

## Gemini / 外部工具定位

Gemini C# 工具箱路径：

```text
G:\Codex\YangAgent Revit\YangAgent Revit\Gemini 资料\YangTools_SourceCode
```

当前决策：

- 作为外部参考资产，不直接并入主线
- 先 inventory，再分类，再挑单个工具重写纳入
- 不允许 Gemini 保留自己的架构权、主题权、命名权
- 外部 agent 只能按任务包做受限交付，Codex 保留架构、审查、合并、发布决定权

当前治理入口：

- `docs/external-toolbox-intake.md`
- `docs/governance/tool-registry.md`
- `docs/governance/rewrite-spec-template.md`
- `docs/governance/acceptance-gate-template.md`
- `docs/governance/delegation-pack-template.md`

## 当前已完成的重要工作

- 路径主线已迁移到 G 盘仓库
- sandbox preflight 可离线运行
- pyRevit 共享主题骨架已建立
- `System Settings` 已接入预设主题机制
- `Project Info Report` 已加入主线
- 多个只读/preview/apply 按钮已进入可验证状态
- 日常文档治理规则已建立：
  - 每天开始要看 Git 状态和核心文档
  - 每天结束要更新 worklog、next-steps、startup prompt
  - 外部 agent 每次交付都必须带操作日志

## 已验证与未验证边界

已经有证据支持的范围：

- `YangAgent` 选项卡可见
- `System Settings` 可打开
- 多个只读导出与 preview 按钮在 sandbox 中已产生过报告证据

仍然不能默认声称已验证的范围：

- 所有按钮在最新工作树下都再次 live 通过
- 两个 apply 按钮在完整模型里的最终稳定性
- Undo 在每条 apply 链路上的持续稳定性
- 更广泛的 Revit 版本兼容性

## 新对话接手动作

新对话开始时，先做：

1. `git status --short --branch`
2. `git log -3 --oneline`
3. 读 `docs/new-chat-startup-2026-06-13.md`
4. 读 `docs/next-steps.md`
5. 读当天最新 worklog 的最新相关段落
6. 如要做 live 测试，再读：
   - `docs/sandbox-pyrevit-mvp-runbook.md`
   - `docs/sandbox-pyrevit-mvp-checklist.md`
   - `docs/sandbox-snowdon-live-pack-2026-06-13.md`
   - `docs/troubleshooting.md`
   - `docs/error-codes.md`

## 外部 Agent 规则

Hermes / Gemini / DeepSeek 只允许：

- inventory
- 草稿代码
- 草稿文档
- 测试清单
- 低风险局部实现
- 按任务包执行的局部重写

他们不允许：

- 自行设计项目架构
- 自行设计主题系统
- 自行改命名体系
- 绕过任务包直接改主线
- 未经 Codex 审查直接视为完成

规则入口：

- `docs/agent-development-rules.md`
- `docs/agent-task-template.md`
- `docs/agent-delivery-report-template.md`
- `docs/agent-review-checklist.md`
- `docs/daily-agent-log-template.md`

## 交接提醒

这个仓库当前最重要的不是“再写一堆计划”，而是：

1. 保持核心文档每天同步
2. 用 sandbox 模型持续收集第一 blocker
3. 只修最高价值阻塞点
4. 把外部工具和外部 agent 继续关进 YangAgent 的治理框架里
