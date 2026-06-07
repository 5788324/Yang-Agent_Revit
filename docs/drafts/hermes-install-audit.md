# Installation Command Audit

> 审查日期：2026-06-07
> 审查范围：三份文档中的安装相关命令一致性
> 源文档：`README.md` → 两份 Hermes 产出：`quickstart` / `troubleshooting-summary`

---

## Checked Files

| # | 文档 | 路径 | 行数 |
|---|------|------|------|
| 1 | README（源） | 主线仓库中的 `README.md` | 77 |
| 2 | Quickstart | Hermes 工作区中的 `docs/drafts/hermes-personal-quickstart.md` | 143 |
| 3 | Troubleshooting | Hermes 工作区中的 `docs/drafts/hermes-troubleshooting-summary.md` | 194 |

---

## 命令矩阵

### 命令 A：安装 pyRevit extension（基本）

| 文档 | 出现的命令 | 位置 |
|------|-----------|------|
| README | `.\scripts\install-pyrevit-extension.ps1` | L46 |
| Quickstart | `.\scripts\install-pyrevit-extension.ps1` | L33 |
| Troubleshooting | `.\scripts\install-pyrevit-extension.ps1` | 问题0 L28 |

> ✅ **三份一致**

---

### 命令 B：强制重装 + 清理缓存

| 文档 | 出现的命令 | 位置 |
|------|-----------|------|
| README | `.\scripts\install-pyrevit-extension.ps1 -Force -ClearCache` | L52 |
| Quickstart | `.\scripts\install-pyrevit-extension.ps1 -Force -ClearCache` | L43 |
| Troubleshooting | `.\scripts\install-pyrevit-extension.ps1 -Force -ClearCache` | 问题1 L68, 问题2 L95 |

> ✅ **三份一致**

---

### 命令 C：构建 Revit 2027 DLL

| 文档 | 出现的命令 | 位置 |
|------|-----------|------|
| README | `.\scripts\build-revit2027-addin.ps1` | L64 |
| Quickstart | （未出现） | — |
| Troubleshooting | `powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\build-revit2027-addin.ps1` | 问题3 L125 |

> ⚠️ **形式不一致**（不同上下文，见分析）

---

### 命令 D：安装 Revit 2027 DLL addin

| 文档 | 出现的命令 | 位置 |
|------|-----------|------|
| README | `.\scripts\install-revit2027-addin.ps1` | L70 |
| Quickstart | （未出现） | — |
| Troubleshooting | `powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\install-revit2027-addin.ps1` | 问题3 L126 |

> ⚠️ **形式不一致**（不同上下文，见分析）

---

### 命令 E：pyRevit 安装前提

| 文档 | 是否提供 pyRevit 下载链接 | 内容 |
|------|--------------------------|------|
| README | ❌ | "请先安装 pyRevit"（无 URL） |
| Quickstart | ✅ | `https://github.com/eirannejad/pyRevit/releases` |
| Troubleshooting | ✅ | `https://github.com/eirannejad/pyRevit/releases` |

> ⚠️ **README 缺失 URL**（两 Hermes 文档间一致）

---

### 命令 F：手动清理缓存脚本

| 文档 | 出现的命令 | 位置 |
|------|-----------|------|
| README | （未出现） | — |
| Quickstart | （未出现） | — |
| Troubleshooting | `.\scripts\clear-pyrevit-yangagent-cache.ps1` | 问题1 L74, 流程图 L182 |

> ✅ Troubleshooting 独有，定位合理

---

### 命令 G：PowerShell 执行策略绕过

| 文档 | 出现的命令 | 位置 |
|------|-----------|------|
| README | （未出现） | — |
| Quickstart | `powershell -NoProfile -ExecutionPolicy Bypass -File 脚本路径` | L134 |
| Troubleshooting | `powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\install-pyrevit-extension.ps1` | 问题4 L155 |

> ⚠️ **Quickstart 使用占位符**（见分析）

---

## Findings

### 逐命令审查

| # | 命令 | 状态 | 详情 |
|---|------|------|------|
| A | 基本 install-pyrevit-extension | ✅ 一致 | 三份完全相同 |
| B | install-pyrevit-extension -Force -ClearCache | ✅ 一致 | 三份完全相同 |
| C | build-revit2027-addin | ⚠️ 形式差异 | README 裸调，Troubleshooting 带 bypass 包裹。不同场景可接受 |
| D | install-revit2027-addin | ⚠️ 形式差异 | 同上 |
| E | pyRevit 前提 | ⚠️ README 缺 URL | 两 Hermes 文档一致给出链接，README 未给出 |
| F | clear-pyrevit-yangagent-cache | ✅ Troubleshooting 独有 | 合理：此脚本是故障排查专用 |
| G | PowerShell bypass 模板 | ❌ 不一致 | Quickstart 用占位符 `脚本路径`，不可复制粘贴 |

---

### 发现 1：Quickstart 常见问题表命令缺少 `.\scripts\` 前缀

**位置**：Quickstart L130

**当前**：
```
| 按钮灰色 | 关 Revit → `install-pyrevit-extension.ps1 -Force -ClearCache` → 开 Revit → Reload |
```

**应改为**：
```
| 按钮灰色 | 关 Revit → `.\scripts\install-pyrevit-extension.ps1 -Force -ClearCache` → 开 Revit → Reload |
```

同一份文档 L43 用了完整路径，L130 却丢了 `.\scripts\` 前缀。用户复制 L130 的命令会找不到脚本。

**严重程度**：⚠️ 中 — 不可复制粘贴

---

### 发现 2：Quickstart PowerShell 绕过命令使用占位符

**位置**：Quickstart L134

**当前**：
```
| PowerShell 脚本不能运行 | 用 `powershell -NoProfile -ExecutionPolicy Bypass -File 脚本路径` |
```

`脚本路径` 是自然语言占位符，不是有效的命令行参数。对比 Troubleshooting 问题 4，同场景给出了可用的完整命令 `powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\install-pyrevit-extension.ps1`。

**严重程度**：⚠️ 中 — 不可复制粘贴

---

### 发现 3：DLL 构建/安装命令在不同文档中形式不同

| 文档 | 形式 | 适用场景 |
|------|------|---------|
| README | `.\scripts\build-revit2027-addin.ps1` | 开发者环境，执行策略已配好 |
| Troubleshooting | `powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\build-revit2027-addin.ps1` | 故障环境，执行策略可能受限 |

**结论**：两类形式都有意义 — README 假设开发者已配好环境，Troubleshooting 面向受限用户。**不算错误，但值得在 Quickstart 的 DLL 部分统一一个推荐形式。**

---

### 发现 4：README 未提供 pyRevit 下载链接

**位置**：README L55

README 说 "如果 Revit 里没有 pyRevit 选项卡，请先安装 pyRevit"，但没有给出下载地址。Quickstart 和 Troubleshooting 都给出了 `https://github.com/eirannejad/pyRevit/releases`。

**严重程度**：🔹 低 — README 不是 Hermes 产出的文件，不需要修改 README，但说明 Hermes 两份文档在此点上比源文档更完善。

---

## Summary

| 指标 | 值 |
|------|-----|
| 审查命令数 | 7 条（A–G） |
| 完全一致 | 3 条（A, B, F） |
| 上下文差异（非错误） | 2 条（C, D） |
| 真正不一致 | 2 条（G 占位符 + Quickstart 丢前缀） |
| 源文档不足 | 1 条（README 缺 pyRevit URL） |

### 是否需要修正？

| 发现 | 需要修正？ | 文档 |
|------|-----------|------|
| 发现 1：Quickstart 丢 `.\scripts\` 前缀 | ✅ **是** | Quickstart L130 |
| 发现 2：Quickstart 用 `脚本路径` 占位符 | ✅ **是** | Quickstart L134 |
| 发现 3：DLL 命令形式差异 | 🔹 可记录，不强制 | — |
| 发现 4：README 缺 pyRevit URL | 🔹 源文档问题，非 Hermes 范围 | README |

---

## Safety Confirmation

- I did not edit pyRevit scripts.
- I did not edit C# files.
- I did not edit scripts or addin templates.
- I did not run install scripts.
- I did not run Revit.
- I did not run git merge / push / pull.
- I did not modify any existing file.
