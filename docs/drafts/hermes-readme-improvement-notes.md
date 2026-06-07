# README 改善建议（个人版方向）

> 基于当前 `README.md` 审查。不改 README 原文，仅提供建议给 Codex 审查后决定是否采用。

---

## 当前 README 结构

| 段落 | 内容 | 建议 |
|------|------|------|
| L1–2 | 项目说明（"公司内部 Revit AI Agent 工作流"） | 见 §1 |
| L5–21 | 主文档索引 | 见 §2 |
| L23–42 | pyRevit 工具清单 | ✅ 保留 |
| L43–47 | 安装 pyRevit extension | 见 §3 |
| L49–53 | 更新后缓存问题处理 | ✅ 保留 |
| L55 | "先安装 pyRevit" | 见 §4 |
| L57–59 | 必备开发辅助工具 | 见 §5 |
| L61–71 | DLL 构建/安装 | ✅ 保留 |
| L73–77 | 当前策略 | ✅ 保留 |

---

## §1 项目定位用语

**当前**：`本仓库用于规划和逐步实现公司内部 Revit AI Agent 工作流。`

**建议**：改为个人版用语，例如：

> 本仓库是个人 Revit 辅助工具，用于导出模型信息、生成检查报告、低风险修复。

**理由**："公司内部"暗示企业级，与当前 MVP 定位不符。

---

## §2 文档索引精简

**当前**：列出 14 个文档链接。

**建议**：只保留个人用户核心文档，其余移到 `docs/` 下的单独索引页。

| 保留 | 移除（或移到二级索引） |
|------|----------------------|
| HANDOFF.md | handoff-2026-05-23.md |
| CHANGELOG.md | architecture-design.md（暂缓用） |
| docs/worklogs/ | mcp-tools.md（暂缓用） |
| docs/next-steps.md | collaboration-workflow.md（暂缓用） |
| docs/user-guide.md | colleague-quickstart.md（与个人版定位冲突） |
| docs/safety-rules.md | revit-ai-agent-project-plan.md（合并到 roadmap） |
| docs/troubleshooting.md | view-naming-rules.md（保留但移二级） |
| docs/developer-guide.md | |
| docs/agent-development-roadmap.md | |

---

## §3 安装命令

**当前**：
```powershell
.\scripts\install-pyrevit-extension.ps1
```
（没有 `cd` 到项目目录的步骤）

**建议**：增加 `cd` 到项目目录的引导行，与 quickstart 一致：

```powershell
cd "D:\YangAgent"   # 替换为项目实际路径
.\scripts\install-pyrevit-extension.ps1
```

---

## §4 pyRevit 下载链接缺失

**当前**：L55 `如果 Revit 里没有 pyRevit 选项卡，请先安装 pyRevit` — 无链接。

**建议**：添加下载地址：

> 如果 Revit 里没有 `pyRevit` 选项卡，请先安装 pyRevit：
> https://github.com/eirannejad/pyRevit/releases

---

## §5 必备开发辅助工具

**当前**：列出 Revit Lookup 和 pyRevit CLI。

**建议**：加上一句说明这些是**开发者工具，个人日常使用不需要**。避免新手困惑。

---

## §6 Revit 版本强调

**当前**：DLL 构建部分提到了 Revit 2027，但 pyRevit 安装部分没有说明版本兼容性。

**建议**：在安装前提中加一行：

> 当前只按 Revit 2027 处理和验证。其他 Revit 版本暂不写成支持范围，除非后续单独测试通过。

---

## §7 测试模型提醒

**当前**：完全没有提到测试模型。

**建议**：在安装步骤末尾或工具清单前加：

> ⚠️ **请先在测试模型上练习，不要直接在正式项目上使用。** 找一个单独的 `.rvt` 文件，避免误操作。

---

## §8 不应添加的内容

以下内容明确不应出现在个人版 README 中：

- ❌ 企业级权限说明
- ❌ 多人协作审批流
- ❌ 商业化发布步骤
- ❌ MCP 写模型方案
- ❌ 多版本 Revit 全覆盖矩阵
- ❌ CI/CD 部署配置

---

## 建议修改优先级

| 优先级 | 建议 | 影响 |
|--------|------|------|
| 🔴 高 | §4 添加 pyRevit 下载链接 | 新用户无法继续安装 |
| 🔴 高 | §7 添加测试模型提醒 | 安全底线 |
| 🟡 中 | §1 定位用语改为个人版 | 避免误导 |
| 🟡 中 | §3 补充 cd 引导 | 新手容易找不到目录 |
| 🟡 中 | §6 Revit 版本强调 | 避免 2026 用户装 DLL 失败 |
| 🟢 低 | §2 文档索引精简 | 美观，非阻塞 |
| 🟢 低 | §5 开发者工具说明 | 降低新手门槛 |
