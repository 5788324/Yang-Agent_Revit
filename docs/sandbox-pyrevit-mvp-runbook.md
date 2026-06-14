# pyRevit MVP Sandbox Runbook

本文件用于人工 Revit 会话中的第一轮真实 sandbox 验证。

它是执行指引，不代表这些检查已经自动完成。

配套短版执行单：

- `docs/sandbox-pyrevit-mvp-checklist.md`

高密度人工 live 测试入口：

- `docs/sandbox-snowdon-live-pack-2026-06-13.md`

## 目标

- 验证当前 pyRevit MVP 能否在 Revit 中正常加载
- 验证当前只读导出和 preview 按钮
- 验证两个低风险 apply 工具的基本执行链路
- 在第一处真实 blocker 停下，并把证据交给 Codex

## 安全规则

- 不要使用生产模型。
- 只使用本地 sandbox/test 模型，例如 `*_sandbox.rvt` 或 `*_test.rvt`。
- apply 测试前，确认模型可丢弃或已备份。
- 只有手动做过一次 Revit `Undo`，才能声称 Undo 已验证。

## 打开 Revit 前的离线预检查

在仓库根目录运行：

```powershell
python tools\run_sandbox_preflight.py --write-report
```

预期：

- sandbox preflight 全部 `PASS`
- pyRevit preflight：`0 errors`
- static check：`0 errors`
- 合法 CSV fixture：通过
- 重复 `element_id` fixture：按预期失败并给出 `YA-APPLY-*-CSV-007`
- 生成报告：`docs/drafts/sandbox-preflight-report.md`

如果某一步失败：

1. 先停，不进 Revit。
2. 先看 `docs/drafts/sandbox-preflight-report.md`。
3. 只修第一个失败点，不并行扩 scope。

## 安装或刷新 pyRevit Extension

如果 extension 未安装，或怀疑缓存旧：

```powershell
.\scripts\install-pyrevit-extension.ps1 -Force -ClearCache
```

然后：

1. 完全重开 Revit，或
2. 在 pyRevit 中执行 `Reload`

## 建议测试模型

基础只读验证可用任意 sandbox 模型。

当前更推荐的完整测试模型：

```text
G:\Codex\YangAgent Revit\YangAgent Revit\Gemini 资料\Revit 测试模型\Snowdon Towers Sample Architectural_sandbox.rvt
```

当前报告目录：

```text
G:\Codex\YangAgent Revit\YangAgent Revit\Gemini 资料\Revit 测试模型\报告
```

## Revit 内验证顺序

按这个顺序执行，减少歧义：

1. 打开 Revit。
2. 确认 `pyRevit` 选项卡可见。
3. 确认 `YangAgent` 选项卡可见。
4. 打开 sandbox/test 模型。
5. 打开 `System Settings`。
6. 语言先设为 `中文`。
7. 确认报告导出目录。
8. 运行 `Project Info Report`。
9. 确认报告文件已生成。
10. 运行 `Export Model Snapshot`。
11. 确认 JSON/CSV 已生成。
12. 运行 `Model Health Report`。
13. 确认 Markdown 报告已生成。
14. 运行 `Export Regression Checklist`。
15. 确认清单文件已生成。
16. 运行 `Export AI Review Prompt`。
17. 确认提示词文件已生成。
18. 运行 `Preview Missing Door Window Marks`。
19. 确认 dry-run Markdown/CSV 已生成。
20. 运行 `Preview Missing Room Numbers`。
21. 确认 dry-run Markdown/CSV 已生成。
22. 运行 `Preview Duplicate Room Numbers`。
23. 确认 dry-run Markdown/CSV 已生成。
24. 运行 `Preview Unplaced Views`。
25. 确认 dry-run Markdown/CSV 已生成。
26. 运行 `Preview View Naming Rules`。
27. 确认 dry-run Markdown/CSV 已生成。
28. 对已审阅的 `missing_door_window_marks_*.csv` 运行 `Apply Missing Door Window Marks`。
29. 确认 apply 日志已生成。
30. 立即手动执行一次 Revit `Undo`。
31. 对已审阅的 `missing_room_numbers_*.csv` 运行 `Apply Missing Room Numbers`。
32. 确认 apply 日志已生成。
33. 立即手动执行一次 Revit `Undo`。
34. 再次打开 `System Settings`。
35. 切换语言到 `English`。
36. 重跑一到两个只读报告按钮，确认英文输出可用。

## 记录什么

每次失败，至少记录：

- 按钮名
- 原始报错文本
- 按钮是灰色、可点后失败，还是导出后内容异常
- 是否生成了任何输出文件
- 模型名
- Revit 版本
- 是否已经尝试过 pyRevit `Reload` 或完整重启

使用：

- `docs/sandbox-pyrevit-mvp-checklist.md`
- `docs/sandbox-pyrevit-mvp-feedback-template.md`
- `docs/troubleshooting.md`
- `docs/error-codes.md`

## 第一阻塞规则

不要一次扩很多修复方向。

如果第一轮 live run 失败：

1. 先记录第一处 blocker。
2. 立即停在这里。
3. 把按钮名、原始错误、输出文件情况和模型信息交给 Codex。

下一次编码只应针对这个第一 blocker。
