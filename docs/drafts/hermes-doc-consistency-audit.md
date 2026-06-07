# 文档一致性总审查

> 审查日期：2026-06-07
> 审查范围：全部 9 份 `docs/drafts/` 文档 + 源文档交叉对比
> 目标：检查 Revit 版本、安装命令、dry-run/apply/Undo、危险建议、企业级用语

> Codex review note: 本审查来自 Hermes G 盘草稿。导入主线后，Revit 版本、Undo、错误码说明等表述已按个人版主线规则进一步收紧；本文保留为 Hermes 审查记录，不作为最终规范。

---

## 审查文件清单

| # | 文件 | 类型 |
|---|------|------|
| 1 | hermes-personal-quickstart.md | 用户文档 |
| 2 | hermes-button-inventory.md | 参考清单 |
| 3 | hermes-troubleshooting-summary.md | 故障排查 |
| 4 | hermes-personal-user-guide-outline.md | 用户指南大纲 |
| 5 | hermes-error-code-cheatsheet.md | 参考清单 |
| 6 | hermes-readme-improvement-notes.md | 改善建议 |
| 7 | hermes-button-inventory-audit.md | 审查报告 |
| 8 | hermes-troubleshooting-audit.md | 审查报告 |
| 9 | hermes-install-audit.md | 审查报告 |

---

## 1. Revit 版本表述一致性

| 文档 | 表述 | 评估 |
|------|------|------|
| Quickstart L23 | "当前适配 Revit 2027，2025/2026 也可试" | ✅ |
| Troubleshooting-summary 问题1 L63 | "Revit 2025/2026/2027 等所有实例" | ✅ |
| Troubleshooting-summary 问题3 L120 | "完全关闭 Revit 2027" | ✅（DLL 相关，合理限定） |
| User-guide-outline L22 | "推荐 2027，2025/2026 也可试 pyRevit 部分" | ✅ |
| Error-code-cheatsheet L51 | "完全关闭 Revit 2027" | ✅（DLL 上下文） |
| Readme-notes L97 | "当前适配 Revit 2027。Revit 2025/2026 也可使用（pyRevit 部分），但 C# DLL 仅支持 2027" | ✅ |
| Button-inventory | （无显式版本提及） | 🔹 不缺 |

**结论**：所有文档统一表述为 **2027 为主、2025/2026 兼容 pyRevit**。Troubleshooting 和 cheatsheet 在 DLL 上下文中正确限定为 2027。**无矛盾。**

---

## 2. 安装命令一致性

| 命令 | Quickstart | Troubleshooting-summary | User-guide-outline | Readme-notes | 一致？ |
|------|-----------|------------------------|-------------------|-------------|--------|
| 基本安装 | `.\scripts\install-pyrevit-extension.ps1` (L33) | `.\scripts\install-pyrevit-extension.ps1` (L28) | `.\scripts\install-pyrevit-extension.ps1` (L30) | 同 (L59) | ✅ |
| Force-ClearCache | `.\scripts\install-pyrevit-extension.ps1 -Force -ClearCache` (L43, L130) | `.\scripts\install-pyrevit-extension.ps1 -Force -ClearCache` (L68, L95) | 同 (L36) | 同 (L52 源) | ✅ |
| Bypass 包装 | `powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\install-pyrevit-extension.ps1` (L134) | 同 (L155) | "用 bypass 模式" (简略) | — | ✅ |
| DLL 构建 | （未出现） | `powershell ... build-revit2027-addin.ps1` (L125) | — | — | ✅（仅 Troubleshooting 有） |
| DLL 安装 | （未出现） | `powershell ... install-revit2027-addin.ps1` (L126) | — | — | ✅（同上） |

**结论**：Day1 修正后，所有安装命令跨文档完全一致。**无矛盾。**

---

## 3. dry-run / apply / Undo 说法一致性

### 3.1 dry-run → apply 流程

| 文档 | 流程表述 | 一致性 |
|------|---------|--------|
| Quickstart §5 (L93-97) | 预览 → CSV → 人工确认 → apply → 验证 → Ctrl+Z | ✅ |
| Button-inventory §apply安全机制 (L66-71) | dry-run CSV → 校验 → 弹窗确认 → apply → 日志 | ✅ |
| User-guide-outline §7 (L123) | dry-run 预览 → 看 CSV → 人工确认 → apply → 验证 → 需要时 Undo | ✅ |
| Error-code-cheatsheet (L71-73) | "遇到错误不会改模型" + "不要跳过错误码" | ✅ |

**结论**：四份涉及 apply 流程的文档**完全一致**。dry-run → 看 CSV → 人工确认 → apply → 验证 → Undo 的链式安全流程无矛盾。

### 3.2 Undo 的措辞精度

| 文档 | Undo 表述 | 是否带验证警告 |
|------|----------|--------------|
| Quickstart L97 | "代码层面所有修改在一个 Transaction 中，**理论上一次撤销整批**；最终必须在测试模型上验证" | ✅ 带验证警告 |
| Quickstart L108（术语表） | "所有 apply 操作都在一个事务里，**一次撤销整批**" | ❌ 术语表未带验证 |
| Quickstart L121（安全原则） | "Ctrl+Z **一次全退**" | ❌ 未带验证 |
| Button-inventory L73 | "代码层面所有 apply 在一个 Transaction 中，**理论上一次撤销整批**。但最终必须在测试模型上人工验证" | ✅ 带验证警告 |
| User-guide-outline §8 L145 | "**一次 Ctrl+Z 撤销整批**" | ⚠️ 主文未带，L148 单独警告 |

> ⚠️ **发现**：Quickstart 有 3 处提到 Undo（L97/L108/L121），其中只有 L97 带了验证警告。术语表 L108 和安全原则 L121 未带 `理论上/必须验证` 限定。
>
> 另外 user-guide-outline §8 L145 主文说 "一次 Ctrl+Z 撤销整批"（陈述语气），L148 单独一行加 "⚠️ 必须在测试模型上验证撤销行为"。这种分隔可能会让只扫标题的用户漏看验证警告。

**建议**：User-guide-outline L145 补充"理论上"一词；Quickstart L108/L121 加 `（必须在测试模型验证）` 后缀。

---

## 4. 危险建议检查

| 文档 | 检查结果 |
|------|---------|
| Quickstart | ✅ 无危险建议。多处强调"测试模型""不要用正式项目" |
| Troubleshooting-summary | ✅ 仅覆盖缓存清理、DLL 解锁、执行策略。无可操作模型的建议 |
| Button-inventory | ✅ apply 安全机制明确，Undo 栏标记为"必须验证" |
| User-guide-outline | ✅ §3.1 测试模型提醒、§11 安全守则、§6.2 AI 建议不直接改模型 |
| Error-code-cheatsheet | ✅ 明确"错误不会改模型""不要忽略错误码" |
| Readme-notes | ✅ 仅建议文档措辞，不涉及操作 |

**结论**：**0 个危险建议。** 安全底线在所有文档中一致贯彻。

---

## 5. 企业级 / 复杂化用语检查

| 文档 | 企业级用语 | 评估 |
|------|-----------|------|
| Quickstart L15 | "它**不是**企业级软件" | ✅ 明确否定 |
| User-guide-outline §1 | "不做权限管理" | ✅ 明确否定 |
| Readme-notes §1, §8 | 建议移除"公司内部"、列出不应添加的企业内容 | ✅ |
| 其余文档 | 无企业级用语 | ✅ |

**结论**：**0 处企业级用语。** 唯一出现"企业级"的地方都是为了明确说 "不是企业级"。

---

## 6. 术语表跨文档一致性

| 术语 | Quickstart 定义 | User-guide-outline 引用 | 一致？ |
|------|----------------|------------------------|--------|
| 只读 | "只看不改" | — | — |
| dry-run | "模拟运行，不实际修改模型" | §7 流程中 | ✅ |
| apply | "真正写入模型，必须先 dry-run" | §7 流程中 | ✅ |
| Undo | "Ctrl+Z，一次撤销整批" | §8 | ✅ 概念一致 |
| CSV | "表格文件，Excel 可打开" | §5.1 | ✅ |
| 测试模型 | "专门测试用的 .rvt" | §3.1 | ✅ |
| 正式/中心模型 | "实际项目文件" | §11 | ✅ |

User-guide-outline 附录明确引用 quickstart 术语表同步，方向正确。

---

## Summary

| 检查项 | 结果 |
|--------|------|
| Revit 版本 | ✅ 一致（2027 为主，2025/2026 兼容 pyRevit） |
| 安装命令 | ✅ 一致（Day1 已修正） |
| dry-run → apply 流程 | ✅ 一致 |
| Undo 措辞 | ⚠️ 轻微不一致（3 处缺验证警告） |
| 危险建议 | ✅ 0 个 |
| 企业级用语 | ✅ 0 个 |
| 术语表 | ✅ 一致 |

### 发现的不一致（共 1 类，3 处）

| # | 文件 | 位置 | 问题 | 严重度 |
|---|------|------|------|--------|
| 1 | Quickstart | L108 术语表 "Undo" | 说"一次撤销整批"，缺验证警告 | 🔹 低 |
| 2 | Quickstart | L121 安全原则 §4 | 说"Ctrl+Z 一次全退"，缺验证警告 | 🔹 低 |
| 3 | User-guide-outline | L145 §8 撤销 | 主文"一次撤销整批"未带"理论上"，与警告行分离 | 🔹 低 |

所有三处都是同一性质：某些地方说 Undo "一次撤销整批"时未附带 `理论上/必须验证` 限定词，而 Quickstart L97 和 Button-inventory L73 已经用了正确的精确措辞。

### 总体评价

**9 份文档之间没有严重矛盾。** 核心安全流程（测试模型 → dry-run → 人工确认 → apply → 验证 → Undo）在所有文档中一致贯彻。安装命令 Day1 修正后全程一致。唯一的瑕疵是 Undo 的措辞在少数几处不如主要段落精确。

---

## Safety Confirmation

- I did not edit pyRevit scripts.
- I did not edit C# files.
- I did not edit scripts or addin templates.
- I did not run install/build scripts.
- I did not run Revit.
- I did not add .rvt files.
- I did not run git merge / push / pull.
