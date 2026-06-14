# Snowdon Towers Live Pack - 2026-06-13

这是当前最快的人工 live 验证入口。

目标不是一次测完所有按钮，而是用内容更完整的 sandbox 模型，尽快拿到第一个高价值 blocker。

## 固定使用

仓库路径：

```text
G:\Codex\YangAgent Revit\YangAgent Revit
```

测试模型：

```text
G:\Codex\YangAgent Revit\YangAgent Revit\Gemini 资料\Revit 测试模型\Snowdon Towers Sample Architectural_sandbox.rvt
```

报告目录：

```text
G:\Codex\YangAgent Revit\YangAgent Revit\Gemini 资料\Revit 测试模型\报告
```

## Revit 前 2 个命令

先在仓库根目录执行：

```powershell
python tools\check_pyrevit_extension.py
python tools\run_sandbox_preflight.py --write-report
```

预期：

- `check_pyrevit_extension.py`：`Summary: 0 errors, 0 warnings`
- `run_sandbox_preflight.py --write-report`：全部步骤 `PASS`

如果失败：

- 停，不进 Revit；
- 把 `docs/drafts/sandbox-preflight-report.md` 作为第一份证据。

## Revit 内最短执行顺序

按这个顺序跑，第一处失败就停：

1. 打开 `Snowdon Towers Sample Architectural_sandbox.rvt`
2. 打开 `YangAgent > System Settings`
3. 语言先选 `中文`
4. 确认导出目录指向 `...\Gemini 资料\Revit 测试模型\报告`
5. 点 `Project Info Report`
6. 点 `Model Health Report`
7. 点 `Preview Missing Door Window Marks`
8. 点 `Preview Missing Room Numbers`
9. 如果前面都成功，再点 `Apply Missing Door Window Marks`
10. 立即在 Revit 里做一次 `Undo`

这一轮不要贪多。

只要第 `5-10` 步里任一步失败，就先停，不继续后面的按钮。

## 这轮最重要的产出

只需要收集下面 4 类信息：

1. 第一处失败的步骤和按钮名
2. 弹窗或 pyRevit 输出里的原始报错文字
3. `报告` 目录里这次新生成了哪些文件
4. `Undo` 是否真的成功

## 最短反馈模板

```text
模型：Snowdon Towers Sample Architectural_sandbox.rvt

失败步骤：
失败按钮：
报错原文：
本次生成文件：
Undo 结果：
- 成功
- 失败
- 还没测到
```

## 如果这一轮全过

如果第 `5-10` 步全过，再补第二轮：

1. `Export Model Snapshot`
2. `Export Regression Checklist`
3. `Export AI Review Prompt`
4. `Preview Duplicate Room Numbers`
5. `Preview Unplaced Views`
6. `Preview View Naming Rules`
7. `Apply Missing Room Numbers`
8. `Undo`

第二轮仍然遵守同一规则：第一处失败就停。
