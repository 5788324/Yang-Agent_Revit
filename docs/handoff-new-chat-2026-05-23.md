# YangAgent Revit 新对话交接文档 - 2026-05-23

本文件用于上下文压缩或新建 AI 对话后快速接手。新对话开始后，请先阅读本文件，再继续开发。

## 1. 仓库与当前状态

- GitHub 仓库：`https://github.com/5788324/Yang-Agent_Revit`
- 本地路径：`D:\codex\Yang Agent_Revit`
- 当前分支：`main`
- 当前最新提交：`190ba81 feat: add basic DLL folder commands`
- 当前阶段：pyRevit MVP 已成型，C# DLL 骨架已开始补正式插件入口。
- 发布版本：已有 `v1.0.0`，当前主线已超过 1.0.0，仍处于 `[Unreleased]` 迭代。

## 2. 今天完成的核心能力

### pyRevit 工具箱

功能区：

- `系统设置`
- `导出报告`

系统设置已支持：

- 中文 / English。
- Light / Dark Theme。
- 用户简称。
- 头像路径。
- AI 工作习惯：
  - 常用 Revit 版本。
  - 默认工作流。
  - AI 分析重点。
  - 安全偏好。
- 公司标准 Markdown 文件：
  - 可选择已有 `.md/.txt`。
  - 可创建默认模板。
  - 默认位置：`%APPDATA%\YangAgent_Revit\company_standards.md`
- 视图命名规则：
  - FloorPlan
  - CeilingPlan
  - Section
  - Elevation
  - ThreeD
  - DraftingView
  - Legend
  - AreaPlan
  - EngineeringPlan
  - 临时关键词

导出报告已支持：

- `导出路径`
- `导出模型快照`
- `模型健康报告`
- `回归测试清单`
- `AI分析提示词`
- `预览缺失标记`
- `应用门窗标记`
- `预览缺失房间编号`
- `应用房间编号`
- `预览重复房间编号`
- `预览未上图视图`
- `预览视图命名`

### 已经由用户验证成功的功能

- pyRevit 安装后 YangAgent 工具栏显示成功。
- 修复按钮灰色 / availability / FullClassName 缓存问题。
- `预览缺失标记` 成功。
- `应用门窗标记` 成功。
- `预览缺失房间编号` 成功。
- `应用房间编号` 成功。
- `预览重复房间编号` 成功。
- `预览视图命名` 成功。
- `系统设置` 中视图命名规则配置成功。
- `回归测试清单` 成功。
- `AI分析提示词` 经过缓存修复后成功。

## 3. 重要修复和坑

### pyRevit 缓存问题

Revit 2027 + pyRevit 可能报：

```text
无法初始化附加模块 ...
FullClassName ...
必须确保该类实现 Autodesk.Revit.UI.IExternalCommand
```

原因通常不是脚本没有实现接口，而是旧 pyRevit 缓存仍在。

必须关闭 Revit 后清理：

```text
*YangAgent*.dll
*YangAgent*.addin
*YangAgent*.cs
*YangAgent*.pickle
```

使用：

```powershell
.\scripts\install-pyrevit-extension.ps1 -Force -ClearCache
```

如果 Revit 仍在运行，旧 DLL 可能被锁住删不掉。先关闭：

```text
Revit.exe
RevitWorker.exe
```

### pyRevit 命名约束

- `.panel`、`.pulldown`、`.pushbutton` 目录必须英文 ASCII、无空格。
- 中文显示名只放在 `bundle.yaml` 的 `title`。
- 不要在 `bundle.yaml` 使用 `context:`，否则 Revit 2027 容易生成 availability 类型错误。

### Revit 2027 / IronPython 坑

- 创建 ElementId 必须用 `ElementId(Int64(element_id))`。
- 判断参数是否存在用 `param is None`，不要用 `if not param`。
- CSV 读取使用 `utf-8-sig`，避免 BOM 造成字段校验失败。
- Apply 工具只读 dry-run CSV，二次确认后才写入。

## 4. 当前代码结构

关键目录：

```text
pyrevit/YangAgent.extension/
  lib/yang_agent_lang.py
  YangAgent.tab/
    Settings.panel/SystemSettings.pushbutton/
    Reports.panel/Reports.pulldown/

src/YangAgent.Revit2027/
  App.cs
  YangAgentPaths.cs
  Commands/

addins/Revit2027/
scripts/
docs/
standards/
samples/
tests/
mcp/
prompts/
```

## 5. C# DLL 当前状态

Revit 2027 `.addin + .dll` 骨架已存在。

当前 DLL 功能：

- 创建 `YangAgent` Ribbon Tab。
- 创建 `系统设置`、`导出报告` Panel。
- 占位按钮：
  - 关于 / 更新
  - 系统设置
  - 配置目录
  - 导出报告
  - 报告目录
- `配置目录` 打开 `%APPDATA%\YangAgent_Revit`。
- `报告目录` 打开默认桌面导出目录。
- 当前 DLL 仍是骨架，不修改模型。

下一步需要在 Revit 2027 中重启加载 DLL 并人工验证这些按钮。

## 6. 完成度评估

以“公司内部可用 Revit AI Agent 工作流”为目标，当前大约完成：

- pyRevit MVP：约 75%
- 团队协作和交接体系：约 80%
- 本机用户习惯 / 公司标准上下文：约 55%
- C# 正式插件：约 15%
- MCP / Bridge：约 5%
- 自动化测试体系：约 20%

总体项目完成度估算：约 35% - 40%。

已经完成的是“能看懂模型、导出报告、dry-run、少量受控修改、给 AI 安全分析上下文”的第一阶段。

距离最终目标还差：

- 标准测试模型和更多回归测试。
- 公司真实 BIM 标准录入和验证。
- 更多 dry-run 工具。
- 更多 apply 工具，但必须谨慎推进。
- 稳定功能迁移到 C# DLL。
- 只读 MCP。
- 结构化 C# Bridge。
- 公司标准知识库和项目知识库完善。

## 7. 长期演进方向

当前文档记录的是基础阶段：让工具先具备“看懂模型、生成报告、dry-run、人工确认、少量受控 apply”的能力。后续项目会继续扩展为更完整的 Revit AI Agent 平台，不局限于当前 pyRevit MVP。

后续大方向包括：

- 大规模增加修改模型能力，但所有修改功能都必须继续遵守 `dry-run -> 人工确认 -> apply`。
- 修改模型功能需要分风险等级推进：
  - 低风险：补充门窗标记、补充房间编号、重命名视图、生成检查报告。
  - 中风险：批量调整图纸/视图参数、按公司标准批量修正命名、生成待修改清单。
  - 高风险：删除元素、移动构件、修改族类型、改中心文件、操作链接模型，默认不做，必须单独设计审批和回滚方案。
- pyRevit 继续作为快速验证和 MVP 层；稳定功能逐步迁移到 C# `.addin + .dll` 正式插件。
- C# 插件后续应承担更稳定的 UI、权限控制、事务管理、日志记录、错误恢复和企业部署。
- MCP / Bridge / Skill 后续会成为重要能力，但初期必须只读优先：
  - MCP 先读取导出的 JSON/CSV/Markdown，不直接写模型。
  - Bridge 先做结构化通信和状态查询，再考虑受控写入。
  - Skill 用于沉淀公司标准、项目流程、测试流程、发布流程和插件开发规范。
- 所有 AI 参与的模型修改，都必须能追溯输入文件、人工确认记录、执行日志、失败原因和撤销方式。
- 正式 Revit 模型、中心文件、客户数据、API Key、本机 `%APPDATA%` 配置仍然禁止提交到 Git。

换句话说：当前只是“安全基础设施和第一批工具”的起点，后续目标是逐步发展成可插件化、可审计、可扩展、可与 MCP/skill 协作的 Revit AI Agent。

## 8. 下一阶段建议

优先级从高到低：

1. **验证当前所有按钮**
   - 使用测试模型。
   - 运行 `回归测试清单`。
   - 逐项记录 Pass / Fail。

2. **验证 C# DLL 骨架**
   - 执行：

   ```powershell
   .\scripts\build-revit2027-addin.ps1
   .\scripts\install-revit2027-addin.ps1
   ```

   - 重启 Revit 2027。
   - 验证 `配置目录` 和 `报告目录`。

3. **整理公司标准**
   - 在 `系统设置` 中创建 `company_standards.md`。
   - 写入视图命名、房间编号、门窗标记规则。
   - 运行 `AI分析提示词`，确认标准被带入。

4. **整理标准测试模型**
   - 不提交 `.rvt` 到 Git。
   - 使用本地或公司内部共享位置。
   - 文件名建议：`YangAgent_sandbox_architecture_2027.rvt`。

5. **继续只读 / dry-run 工具**
   - 优先未上图视图、视图命名、房间编号等低风险场景。
   - 不做删除元素。
   - 不直接修改中心文件。

6. **准备 MCP**
   - 先只读。
   - 读取已导出的 JSON/CSV/Markdown。
   - 不直接连接 Revit 修改模型。

## 9. 新对话启动指令

新对话可以直接粘贴以下内容：

```text
我们继续开发 YangAgent Revit 项目。

仓库：https://github.com/5788324/Yang-Agent_Revit
本地路径：D:\codex\Yang Agent_Revit

请先执行：
1. git status --short --branch
2. git pull
3. 阅读 docs/handoff-new-chat-2026-05-23.md
4. 阅读 docs/next-steps.md
5. 阅读 docs/worklogs/worklog-2026-05-23.md 的最后部分

当前重点：
- 不要直接修改正式 Revit 模型。
- 优先测试和完善 pyRevit MVP。
- 下一步优先验证 C# DLL 骨架和回归测试清单。
- 所有新功能遵守 dry-run -> 人工确认 -> apply 的模式。
- 当前只是基础阶段，后续会继续开发更多修改模型功能、正式插件、MCP、Bridge、skill 等能力。
```

## 10. 收工前检查

本次对话结束前必须确认：

- `git status --short --branch` 状态可解释。
- 所有交接文档已提交。
- 不要 push，除非用户明确通知。
- 新对话优先阅读 `docs/handoff-new-chat-2026-06-07.md`，再读本文件。
## 2026-06-07 Update

Current local state:

- Branch: `main`.
- Local branch is ahead of `origin/main`; do not push unless the user asks.
- Project direction: personal-use Revit assistant, not enterprise platform.
- First Revit version phase: 2024-2027.
- Revit 2011-2023: deferred compatibility backlog only.
- Current C# DLL skeleton: Revit 2027 only.

New authoritative docs:

- `docs/revit-version-support-plan.md` records version support wording.
- `tools/static_checks.py` provides a no-Revit static check entry point.
- Generic DLL scripts now exist:
  - `scripts\build-revit-addin.ps1 -Version 2027`
  - `scripts\install-revit-addin.ps1 -Version 2027`
  - Revit 2024/2025/2026 currently stop with `YA-CS-VERSION-PLANNED`.
- Offline apply CSV validation now exists:
  - `python tools\validate_apply_csv.py --kind room --csv path\to\missing_room_numbers_YYYYMMDD_HHMMSS.csv`
  - `python tools\validate_apply_csv.py --kind mark --csv path\to\missing_door_window_marks_YYYYMMDD_HHMMSS.csv`
  - This is read-only and does not require Revit.

Current safety rules:

- Do not directly modify production Revit models.
- New model-changing functions must follow dry-run -> human confirmation -> apply.
- Apply tools must provide logs, clear errors, and Revit Undo verification steps.
- Do not claim Undo is verified unless manually tested in a sandbox model.

Hermes/DeepSeek boundary:

- Hermes may run read-only checks and write draft reports.
- Hermes must not edit pyRevit `script.py`, C# core, build/install scripts, addin templates, or Revit models.
- Hermes output remains draft until Codex reviews it.

## 2026-06-07 Final Handoff Pointer

The current active handoff is now:

- `docs/handoff-new-chat-2026-06-07.md`

Use that file first for new Codex chats. This 2026-05-23 file is retained for historical context.
