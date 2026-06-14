# pyRevit MVP Sandbox Checklist

本文件是第一轮 sandbox 人工测试的短版执行单。

解释和背景见：

- `docs/sandbox-pyrevit-mvp-runbook.md`

更快的 Snowdon 测试包见：

- `docs/sandbox-snowdon-live-pack-2026-06-13.md`

## Revit 前

1. 动作：运行 `python tools\check_pyrevit_extension.py`
   预期：`Summary: 0 errors, 0 warnings`
   失败：先停，先修 pyRevit 结构或脚本问题。

2. 动作：运行 `python tools\run_sandbox_preflight.py --write-report`
   预期：全部步骤 `PASS`
   失败：打开 `docs/drafts/sandbox-preflight-report.md`，停在第一个失败点。

3. 动作：确认最新 preflight 报告路径
   预期：`docs/drafts/sandbox-preflight-report.md`
   失败：说明预检查没完成，不进入 Revit。

## 安装 / 刷新

4. 动作：如果 `YangAgent` 缺失或明显是旧状态，运行 `.\scripts\install-pyrevit-extension.ps1 -Force -ClearCache`
   预期：extension 刷新成功
   失败：记录脚本原始报错。

5. 动作：重开 Revit 或在 pyRevit 中执行 `Reload`
   预期：`pyRevit` 和 `YangAgent` 两个选项卡都可见
   失败：停并填写反馈模板。

## Live 测试模型

6. 动作：打开本地 `*_sandbox.rvt` 或 `*_test.rvt`
   预期：是可丢弃的测试模型
   失败：不要用生产模型。

   推荐完整测试模型：
   `G:\Codex\YangAgent Revit\YangAgent Revit\Gemini 资料\Revit 测试模型\Snowdon Towers Sample Architectural_sandbox.rvt`

   推荐报告目录：
   `G:\Codex\YangAgent Revit\YangAgent Revit\Gemini 资料\Revit 测试模型\报告`

## 按钮顺序

7. 动作：按下面顺序执行
   预期：每一步都出现预期文件或可见结果
   失败：在第一处 blocker 停下并填写反馈模板

   1. `System Settings`
   2. `Project Info Report`
   3. `Export Model Snapshot`
   4. `Model Health Report`
   5. `Export Regression Checklist`
   6. `Export AI Review Prompt`
   7. `Preview Missing Door Window Marks`
   8. `Preview Missing Room Numbers`
   9. `Preview Duplicate Room Numbers`
   10. `Preview Unplaced Views`
   11. `Preview View Naming Rules`
   12. `Apply Missing Door Window Marks`
   13. 测一次 Revit `Undo`
   14. `Apply Missing Room Numbers`
   15. 再测一次 Revit `Undo`
   16. 切换语言到 `English`
   17. 重跑一到两个只读报告按钮

## 失败时

8. 动作：填写 `docs/sandbox-pyrevit-mvp-feedback-template.md`
   预期：只记录一个第一 blocker
   失败：如果很多东西都坏了，也先只报第一处。

9. 动作：带上 runbook 的步骤号
   预期：Codex 能直接映射到执行顺序
   失败：如果步骤号不清楚，就按 runbook 顺序描述。

10. 动作：第一处 blocker 后停止扩测
    预期：不在混乱状态下继续堆新问题
    失败：后续错误只能作为次级信息，不能替代第一 blocker。
