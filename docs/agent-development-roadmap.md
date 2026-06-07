# YangAgent Revit Personal Agent Roadmap

本项目当前按“个人辅助工作 Agent”推进，不按企业级商业插件推进。目标是尽快得到一个你自己能用、最多分享给朋友使用的 Revit 辅助工具。

## 1. 项目边界

当前目标：

- 辅助个人日常 Revit 工作。
- 快速导出模型信息、生成检查报告、定位常见问题。
- 对低风险问题提供 dry-run 和人工确认后的 apply。
- 出错时能看到明确报错、日志和回退方式。
- 代码和文档保持简单，方便 AI 继续维护。

当前不做：

- 企业级权限系统。
- 商业化发布体系。
- 复杂多人审批流。
- 大型平台化 MCP/Bridge。
- 多版本 Revit 全覆盖。
- 自动操作正式中心模型。

保留的底线：

- 不直接修改正式模型。
- 修改模型必须先 dry-run。
- apply 前必须人工确认。
- apply 必须有 Revit Undo、日志和错误反馈。
- 不提交 `.rvt`、客户资料、本机配置、密钥。

## 2. 更现实的时间表

| 阶段 | 时间估计 | 结果 |
| --- | --- | --- |
| 个人可用 MVP | 2-4 天 | pyRevit 工具稳定、能导出报告、能跑 dry-run、少量 apply 可用 |
| 个人日常可用版 | 1-2 周 | 常用检查、报告、AI 提示词、低风险修复形成闭环 |
| 小范围分享版 | 2-4 周 | 安装脚本、故障排查、基础 C# DLL 入口、朋友可按文档安装 |
| 后续增强 | 按需 | MCP、skill、C# 迁移、更多 apply 工具，有需要再做 |

结论：项目不需要一开始做很大。先做个人可用工具，遇到真实工作痛点再扩展。

## 3. 接下来优先做什么

### 优先级 1：把现有 pyRevit MVP 跑顺

- 在测试模型里运行回归测试清单。
- 确认这些按钮能稳定输出文件：
  - 导出模型快照。
  - 模型健康报告。
  - 回归测试清单。
  - AI 分析提示词。
  - 预览缺失门窗标记。
  - 预览缺失房间编号。
  - 预览重复房间编号。
  - 预览未上图视图。
  - 预览视图命名。
- apply 工具只保留低风险：
  - 应用门窗标记。
  - 应用房间编号。

### 优先级 2：把“错误反馈 + 回退”做扎实

每个 apply 工具必须做到：

- 只读取对应 dry-run CSV。
- CSV 字段不对时给明确错误。
- apply 前显示影响数量。
- Revit Transaction 名称清楚，方便 Undo。
- 输出 apply Markdown 日志。
- 输出 apply CSV 结果。
- 跳过已经被人工修改过的元素。

先不用复杂错误系统，先用简单格式：

```text
YA-APPLY-ROOM-001: CSV file name is not supported.
YA-APPLY-ROOM-002: Required CSV columns are missing.
YA-APPLY-ROOM-003: Revit element was not found.
```

### 优先级 3：C# DLL 只做入口和辅助

C# DLL 暂时不迁移复杂业务。它只做：

- 创建 YangAgent Ribbon。
- 打开配置目录。
- 打开报告目录。
- 显示关于信息。
- 以后作为正式入口。

pyRevit 仍然是主要开发层，因为迭代快。

### 优先级 4：MCP / skill 暂缓

MCP 和 skill 有价值，但现在不是主线。

近期只做：

- 让 AI 读取导出的 Markdown、CSV、JSON。
- 把常用规则写入文档或本地 company standards。
- 不直接让 MCP 写 Revit 模型。

等个人 MVP 稳定后，再考虑 MCP server 或 skill。

## 4. 每日工作方式

每天只做小闭环：

1. 明确今天目标。
2. 检查 `git status`。
3. 不主动频繁 pull/push，除非用户通知。
4. 改一个小功能或修一个问题。
5. 能测就测，不能在 Revit 内测就明确说明。
6. 更新当天 worklog。
7. 记录下一步。

每日 worklog 只需要写清楚：

- 今天做了什么。
- 改了哪些文件。
- 怎么验证。
- 哪些还没验证。
- 下一步做什么。

## 5. Hermes 辅助分工

Hermes/DeepSeek 只做低风险辅助任务，必须新建分支 `hermes/docs-personal-mvp`。

Hermes 可以做：

- 个人版快速开始草稿。
- pyRevit 按钮清单。
- 故障排查摘要。
- 面向代码/CAD 新手的术语解释。

Hermes 不可以做：

- 不改 `pyrevit/**/script.py`。
- 不改 C# DLL 代码。
- 不改 `.addin` 模板。
- 不改构建或安装脚本。
- 不运行 install 脚本。
- 不操作 Revit 模型。
- 不设计 MCP 写模型。

详细规则见 `docs/hermes-agent-brief.md`。

## 6. 文档保持最小化

必需文档：

- `README.md`：项目是什么，怎么安装。
- `docs/next-steps.md`：下一步做什么。
- `docs/troubleshooting.md`：常见报错怎么处理。
- `docs/testing-and-qa.md`：怎么测试。
- `docs/worklogs/worklog-YYYY-MM-DD.md`：每天记录。
- `docs/agent-development-roadmap.md`：当前路线图。
- `docs/hermes-agent-brief.md`：Hermes 辅助任务边界。
- `docs/error-codes.md`：当前最小错误代码表。

暂缓文档：

- 企业级发布清单。
- 大型 MCP 架构设计。
- 多角色权限设计。
- 商业化说明。

## 7. 当前最短路径

最快可用路线：

1. 保持 pyRevit 为主。
2. 先跑通所有已有按钮。
3. 修复最影响使用的 bug。
4. 只增加你马上会用的功能。
5. 每个新 apply 都必须先有 preview。
6. C# DLL 只保持能加载和能打开目录。
7. MCP / skill 等到数据导出稳定后再做。

这个路线更符合个人工具：少做架构，多做能马上帮你工作的功能。
## 8. Revit Version Boundary

- First phase targets Revit 2024-2027.
- Current C# DLL skeleton is Revit 2027 only.
- Revit 2011-2023 are deferred compatibility backlog items.
- Do not describe Revit 2011-2027 as already supported.
- Detailed version wording is recorded in `docs/revit-version-support-plan.md`.
