# YangAgent Revit — 个人版快速开始

> 面向代码新手和 CAD/Revit 新手。本指南假设你已经在用 Revit 做日常建模工作。

---

## 这是什么？

YangAgent Revit 是一个**个人辅助工具**，嵌在 Revit 里帮你：

- 📊 导出模型信息（快照、健康报告）
- 🔍 检查常见问题（缺标记、缺编号、未上图视图）
- ✏️ 低风险修复（预览 → 人工确认 → 写入）

它**不是**企业级软件，不做权限管理，不自动改正式模型。是帮你干活的工具箱。

---

## 安装

### 前提条件

1. **Revit 2027** 已安装。当前 C# DLL 骨架只按 Revit 2027 验证；其他版本先不要按正式支持处理。
2. **pyRevit** 已安装。如果 Revit 顶部没有 `pyRevit` 选项卡，先装 pyRevit：[pyRevit 官网](https://github.com/eirannejad/pyRevit/releases)

### 安装本工具

1. 把本项目文件夹放到任意位置（例如 `D:\YangAgent`）。
2. 打开 PowerShell（右键"以管理员身份运行"不是必须的，但执行策略需要允许脚本）：

```powershell
cd "D:\YangAgent"   # 替换为你的实际路径
.\scripts\install-pyrevit-extension.ps1
```

3. 重启 Revit。在 pyRevit 选项卡里应该能看到 **YangAgent** 面板。

### 如果按钮灰色 / 报错

关闭 Revit，执行：

```powershell
.\scripts\install-pyrevit-extension.ps1 -Force -ClearCache
```

然后重新打开 Revit，在 pyRevit 里点 Reload。

---

## 上手 5 步

> ⚠️ **重要：先用测试模型，不要用正式项目！** 找个单独的 `.rvt` 文件练手。

### 1. 设置语言和路径

- 点 `系统设置` → 选 `中文`（或 English）
- 点 `导出报告 → 导出路径` → 选一个空文件夹存放报告

### 2. 跑只读报告（不会改模型）

按顺序点击，每次完成后去导出文件夹看文件：

| 按钮 | 会生成什么 | 安全 |
|------|-----------|------|
| 导出模型快照 | JSON/CSV 模型数据 | ✅ 只读 |
| 模型健康报告 | Markdown 健康检查报告 | ✅ 只读 |
| 回归测试清单 | Markdown 测试清单 | ✅ 只读 |
| AI分析提示词 | AI 分析用的提示词 + 报告清单 | ✅ 只读 |

### 3. 跑预览检查（dry-run，不写入）

| 按钮 | 检查什么 | 会生成什么 |
|------|---------|-----------|
| 预览缺失标记 | 哪些门窗没标记 | Markdown + CSV |
| 预览缺失房间编号 | 哪些房间没编号 | Markdown + CSV |
| 预览重复房间编号 | 哪些房间编号重复 | Markdown + CSV |
| 预览未上图视图 | 哪些视图可能没放到图纸上 | Markdown + CSV |
| 预览视图命名 | 视图命名是否符合规则 | Markdown + CSV |

### 4. 把报告发给 AI 分析

如果你用 Codex 或 Claude，可以把 `model_health_report_*.md` 发给它，问：

```
请分析这份 Revit 模型健康报告，按严重程度列出问题。
只给建议，不要生成会直接修改模型的脚本。
```

### 5.（可选）低风险修复

> 仅在测试模型上练习！正式项目等你在测试模型上完全跑通再说。

1. 先跑 `预览缺失标记`（或 `预览缺失房间编号`）→ 得到 CSV。
2. 打开 CSV，人工确认要写什么值。
3. 点 `应用门窗标记`（或 `应用房间编号`），**选择对应 CSV**。
4. 弹出确认框 → 确认。
5. 如果不对，在 Revit 里 **Ctrl+Z 撤销**。当前 apply 工具使用一个 Revit Transaction，设计目标是一次撤销整批；每次新版本仍要在测试模型里验证。

---

## 术语解释

| 术语 | 意思 |
|------|------|
| **只读 / Read-only** | 只看不改。跑多少次都不会动模型。 |
| **dry-run / 预览** |模拟运行。生成报告告诉你"如果执行会怎样"，但**不实际修改模型**。 |
| **apply / 应用** | 真正写入模型。必须先 dry-run，再看 CSV，最后确认才能 apply。 |
| **Undo / 撤销** | Revit 里 Ctrl+Z。当前 apply 操作放在一个事务里，目标是一次撤销整批；正式使用前先在测试模型验证。 |
| **CSV** | 表格文件，可用 Excel 打开。dry-run 的检查结果、apply 的输入都走 CSV。 |
| **报告目录** | 你通过 `导出路径` 设置的那个文件夹，所有输出都放这里。 |
| **测试模型** | 专门用来测试工具的 `.rvt` 文件，不是你的正式项目。随便改，不怕坏。 |
| **正式模型 / 中心模型** | 你实际工作中用的项目文件。**工具的设计原则：不在未经确认的情况下修改正式模型。** |

---

## 安全原则

1. **不直接改正式模型** — 先在测试模型上跑通。
2. **修改前必 dry-run** — apply 按钮只接受对应 dry-run 产生的 CSV。
3. **人工确认** — apply 前会弹窗显示影响数量。
4. **可撤销** — 每次 apply 是一个 Revit Transaction，目标是 Ctrl+Z 一次全退；先在测试模型验证。
5. **不要直接用于中心模型** — 工具不会主动判断你的业务风险。正式模型、中心模型、客户模型先不要用 apply。

---

## 常见问题

| 问题 | 处理 |
|------|------|
| 按钮灰色 | 关 Revit → `.\scripts\install-pyrevit-extension.ps1 -Force -ClearCache` → 开 Revit → Reload |
| 提示 FullClassName 错误 | 同上，清理旧缓存 |
| 找不到 pyRevit 选项卡 | 先安装 pyRevit |
| DLL 被锁定 | 保存工作 → 正常关闭 Revit → 确认任务管理器无 Revit.exe → 重新构建 |
| PowerShell 脚本不能运行 | 用 `powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\install-pyrevit-extension.ps1` |

---

## 需要帮助？

- 详细故障排查：`docs/troubleshooting.md`
- 错误代码说明：`docs/error-codes.md`
- 项目路线图：`docs/agent-development-roadmap.md`
