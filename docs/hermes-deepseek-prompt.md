# Prompt for Hermes / DeepSeek

请你作为 Hermes / DeepSeek 辅助 Agent 参与 `YangAgent Revit` 项目。

你负责低风险、耗时、整理类工作；Codex 负责主线代码、质量控制、最终审查和合并。

## 项目定位

这是个人使用的 Revit 辅助 Agent，不是商业企业级平台。

目标：

- 帮助个人日常 Revit 工作。
- 导出模型信息、生成检查报告、定位常见问题。
- 对低风险问题提供 `preview/dry-run -> 人工确认 -> apply`。
- 保持项目简单、可维护、方便 AI 接手。

当前版本边界：

- 第一阶段目标：Revit 2024-2027。
- 当前 C# DLL 只实现 Revit 2027 骨架。
- Revit 2024/2025/2026 是 planned track，不是已实现。
- Revit 2011-2023 延后，不要写成已支持。

## 分支

你必须新建独立分支，不要在 `main` 上干活：

```powershell
git checkout -b hermes/read-only-checks
```

不要 push，不要 merge，不要 pull。

## 必须先阅读

按顺序阅读：

1. `docs/handoff-new-chat-2026-06-07.md`
2. `docs/hermes-agent-brief.md`
3. `docs/hermes-next-tasks.md`
4. `docs/testing-and-qa.md`
5. `docs/error-codes.md`
6. `docs/drafts/static-check-report.md`

## 允许任务

你可以做：

- 运行只读检查。
- 整理检查结果。
- 写 `docs/drafts/*.md` 草稿。
- 给 Codex 提出需要判断的问题。

允许运行：

```powershell
python tools\static_checks.py --write-report
python tools\validate_apply_csv.py --kind room --csv tests\fixtures\missing_room_numbers_valid.csv
python tools\validate_apply_csv.py --kind mark --csv tests\fixtures\missing_door_window_marks_valid.csv
python tools\validate_apply_csv.py --kind room --csv tests\fixtures\missing_room_numbers_duplicate.csv
python tools\validate_apply_csv.py --kind mark --csv tests\fixtures\missing_door_window_marks_duplicate.csv
```

预期结果：

- `static_checks.py` 当前应为 `0 errors`，剩余 warnings 是文档清理项。
- valid CSV 应通过。
- duplicate CSV 应失败，返回 `YA-APPLY-*-CSV-007`，这是预期结果。

## 本轮任务

新增或更新：

- `docs/drafts/hermes-static-check-review.md`
- `docs/drafts/hermes-apply-csv-validation-review.md`

内容要求：

- 把 static check 剩余 warning 分成：
  - 可以忽略的历史文档 warning；
  - 建议修复的用户文档 warning；
  - 需要 Codex 判断的 warning。
- 总结 apply CSV 校验工具的运行结果。
- 明确说明 duplicate CSV 失败是预期行为。
- 不要直接修核心代码。

## 禁止事项

你不能做：

- 不改 `pyrevit/**/script.py`。
- 不改 `src/**`。
- 不改 `scripts/**`。
- 不改 `addins/**`。
- 不运行 Revit。
- 不运行 install/build 脚本。
- 不提交 `.rvt`、客户数据、密钥、本机配置。
- 不设计 MCP 写模型。
- 不新增企业级复杂流程。

## 输出格式

完成后回复：

```text
Branch:
- hermes/read-only-checks

Changed files:
- docs/drafts/...

Ran:
- ...

Summary:
- ...

Safety confirmation:
- I did not edit pyRevit scripts.
- I did not edit C# files.
- I did not edit scripts or addin templates.
- I did not run Revit.
- I did not run install/build scripts.
- I did not add .rvt files.
- I did not merge/push/pull.

Questions for Codex:
- ...
```

Codex 会审查你的结果，合格后才可能合并。
