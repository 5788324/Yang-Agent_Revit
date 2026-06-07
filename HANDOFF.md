# 交接协议 (HANDOFF)

**Yang Agent Revit 项目标准交接文档**

本文档是项目的永久性交接 SOP（标准操作流程），适用于：
- 人类同事之间的工作交接
- AI 工具（Antigravity / Claude Code / Codex）之间的上下文切换
- AI 对话上下文到达上限后，开启新对话时的快速接续

---

## 第一部分：接手前必读（5分钟）

### 项目是什么
公司内部 Revit AI Agent 工作流。让大语言模型（LLM）通过 pyRevit 脚本和 Revit API，帮助 BIM 工程师自动化检查、生成报告、执行受控修改。

### 最重要的三个约束
1. **第一阶段：只读优先** — 不能随意写入 Revit 模型，修改必须经过 dry-run 和二次确认。
2. **安全第一** — 禁止提交公司模型文件 (`.rvt`)、API 密钥、任何客户数据到 Git。
3. **测试模型先行** — 所有新功能必须在 `*_test.rvt` 或 `*_sandbox.rvt` 中验证，禁止直接在中心文件调试。

---

## 第二部分：项目当前状态（快速定位）

### 代码结构（关键目录）
```
Yang-Agent_Revit/
├── CHANGELOG.md              ← 版本历史，先看这个
├── HANDOFF.md                ← 本文件
├── docs/
│   ├── handoff-YYYY-MM-DD.md ← 每次交接的快照文档（按日期）
│   ├── worklogs/             ← 每日工作日志流水账
│   ├── next-steps.md         ← 当前待办事项
│   ├── safety-rules.md       ← 安全规则（必读）
│   ├── developer-guide.md    ← 开发约定（必读）
│   └── architecture-design.md← 整体架构设计
├── pyrevit/YangAgent.extension/YangAgent.tab/
│   ├── Settings.panel/
│   │   └── SystemSettings.pushbutton/   ← 集成设置窗口（语言/主题/用户名）
│   └── Reports.panel/
│       └── Reports.pulldown/            ← 所有报告和工具的下拉菜单
│           ├── ReportExportPath.pushbutton
│           ├── ExportModelSnapshot.pushbutton
│           ├── ModelHealthReport.pushbutton
│           ├── PreviewMissingDoorWindowMarks.pushbutton
│           ├── ApplyMissingDoorWindowMarks.pushbutton  ← 唯一的"修改模型"工具
│           ├── PreviewMissingRoomNumbers.pushbutton
│           ├── PreviewDuplicateRoomNumbers.pushbutton
│           ├── PreviewUnplacedViews.pushbutton
│           └── PreviewViewNamingRules.pushbutton
├── pyrevit/YangAgent.extension/lib/
│   └── yang_agent_lang.py    ← 核心共享库（语言/主题/配置）
├── src/                      ← 未来 C# 正式插件（当前为骨架）
└── scripts/
    ├── install-pyrevit-extension.ps1
    └── clear-pyrevit-yangagent-cache.ps1
```

### 今天（接手时）的最新状态
- 查阅 `CHANGELOG.md` 的 `[Unreleased]` 部分，了解最新的变更。
- 查阅 `docs/worklogs/` 目录下最新日期的工作日志，了解上一个人做了什么、遇到了什么问题、下一步是什么。
- 查阅 `docs/next-steps.md` 了解当前优先级最高的任务。

---

## 第三部分：AI 上下文续接指南（新对话必读）

当 AI 对话上下文到达上限，需要开启新对话时，请将以下模板内容**直接粘贴给新的 AI 对话**：

---

```
[Yang Agent Revit 项目上下文]

仓库：https://github.com/5788324/Yang-Agent_Revit
本地路径：D:\Antigravity\YANG ANENT_REVIT

请先执行以下步骤接手工作：
1. 阅读 CHANGELOG.md 了解最新版本历史
2. 阅读 docs/worklogs/ 下最新的工作日志了解上次进展
3. 阅读 docs/next-steps.md 了解当前优先任务
4. 阅读 docs/safety-rules.md（安全约束）
5. 阅读 docs/developer-guide.md（开发约定）

关键约束：
- 目标 Revit 版本：2022 / 2024 / 2025 / 2027
- pyRevit 脚本必须兼容 IronPython 2.7，禁止 f-string、类型注解
- 所有 bundle 目录名必须为英文无空格，禁止 bundle.yaml 里使用 context:
- 修改 Revit 模型必须先 dry-run，然后用户二次确认
- 禁止提交 .rvt 文件、API 密钥到 Git
- 完成工作后必须更新 docs/worklogs/worklog-YYYY-MM-DD.md 并提交 Git

当前任务：[在此处补充你的具体任务]
```

---

## 第四部分：工作日志规范

### 每次工作开始时
1. 执行 `git pull` 获取最新代码。
2. 阅读 `docs/worklogs/` 中最新的工作日志。
3. 阅读 `docs/next-steps.md` 确认当前优先任务。

### 每次工作结束时（人工或 AI 都必须执行）
1. 在 `docs/worklogs/` 下创建或更新当天的工作日志文件（格式：`worklog-YYYY-MM-DD.md`）。
2. 记录：做了什么、遇到什么问题、下一步计划。
3. 更新 `CHANGELOG.md` 的 `[Unreleased]` 部分。
4. 更新 `docs/next-steps.md` 的任务状态。
5. 执行 `git add` 和 `git commit` 保存本地进度。
6. 不要自动 `git push`；只有用户明确通知时才 push。

### Commit Message 规范
```
feat: 新增功能
fix: 修复 bug
docs: 文档更新
refactor: 代码重构
chore: 脚本/工具/配置调整
```

---

## 第五部分：部署到 Revit（本地环境同步）

### 首次安装
```powershell
.\scripts\install-pyrevit-extension.ps1
```
然后重启 Revit。

### 代码更新后刷新 Revit
```powershell
# 方法1：在 Revit 里点击 pyRevit 选项卡 -> Reload
# 方法2（如遇缓存问题，先关 Revit）：
.\scripts\install-pyrevit-extension.ps1 -Force -ClearCache
```
然后重新打开 Revit。

### 已知注意事项
- Revit 2027 + IronPython 创建 `ElementId` 必须用 `ElementId(Int64(value))`，否则报重载错误。
- `bundle.yaml` 禁止使用 `context:` 字段，会导致 Revit 2027 中按钮全灰。
- Revit 参数对象不能用 `if not param` 判断，必须用 `if param is None`。
- CSV 文件写入/读取需明确指定 `utf-8-sig` 编码，避免 BOM 头造成字段错误。
- 门窗标记参数读取需同时尝试 `ALL_MODEL_MARK`、`LookupParameter("Mark")`、`LookupParameter("标记")`。

---

## 第六部分：紧急联系与风险处置

### 如果脚本意外修改了 Revit 模型
1. **立即** 在 Revit 中按 `Ctrl+Z` 撤销（所有 Apply 工具均已包裹在 Transaction 内，支持撤销）。
2. 不要保存文件。
3. 检查是否在生产模型或中心文件上操作。

### 如果 Git 代码出现问题需要回滚
```powershell
git log --oneline -10     # 查看最近10次提交
git revert <commit-hash>  # 安全回滚指定提交
```
