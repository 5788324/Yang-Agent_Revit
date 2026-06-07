# Hermes Next Tasks

Hermes/DeepSeek 当前能力评估：可以承担文档、测试、只读静态检查任务。仍然不允许修改核心代码、安装脚本、addin 模板或 Revit 模型。

## 工作边界

文档草稿可继续使用分支：

```powershell
hermes/docs-personal-mvp
```

只读检查试运行使用分支：

```powershell
hermes/read-only-checks
```

不做：

- 不改 `pyrevit/**/script.py`
- 不改 `src/**`
- 不改 `scripts/**`
- 不改 `addins/**`
- 不运行 Revit
- 不运行 install/build 脚本
- 不做 git merge / push / pull
- 不添加 `.rvt`

## Day 1：安装文档修正复查

目标：确认安装相关文档可复制、可执行、面向新手。

只允许修改：

- `docs/drafts/hermes-personal-quickstart.md`

任务：

- 修正安装命令中缺少 `.\scripts\` 的地方。
- 替换不可复制的自然语言占位符命令。
- 检查所有 PowerShell 命令是否都可以直接复制。
- 输出修改摘要。

## Day 2：README 草稿建议

目标：给主 README 提供个人版简化建议，但不要直接改 README。

新增文件：

- `docs/drafts/hermes-readme-improvement-notes.md`

内容：

- README 里哪些内容适合保留。
- 哪些地方应补 pyRevit 下载链接。
- 哪些地方应强调 Revit 2027。
- 哪些地方应提醒先用测试模型。
- 不要写企业级内容。

## Day 3：用户指南草稿

目标：把 quickstart 扩展成更完整的个人用户指南草稿。

新增文件：

- `docs/drafts/hermes-personal-user-guide-outline.md`

内容：

- 安装。
- 第一次运行。
- 如何选择导出目录。
- 如何读报告。
- 如何把报告交给 AI。
- 如何安全使用 apply。
- 如何撤销。
- 常见问题入口。

## Day 4：错误代码易读化

目标：把 `docs/error-codes.md` 转成新手容易看懂的摘要。

新增文件：

- `docs/drafts/hermes-error-code-cheatsheet.md`

内容：

- 错误代码。
- 你看到这个错误时发生了什么。
- 是否改动了模型。
- 下一步怎么做。

## Day 5：文档一致性总审查

目标：审查 drafts 文档之间是否互相矛盾。

新增文件：

- `docs/drafts/hermes-doc-consistency-audit.md`

检查：

- Revit 版本表述是否一致。
- 安装命令是否一致。
- dry-run/apply/Undo 说法是否一致。
- 是否有危险建议。
- 是否有企业级复杂化内容。

## 每次完成后汇报格式

```text
Branch:
- hermes/docs-personal-mvp

Changed files:
- ...

Summary:
- ...

Safety confirmation:
- I did not edit pyRevit scripts.
- I did not edit C# files.
- I did not edit scripts or addin templates.
- I did not run install/build scripts.
- I did not run Revit.
- I did not add .rvt files.
- I did not run git merge / push / pull.

Questions for Codex:
- ...
```

## Codex 验收标准

- 只接受 docs/drafts 范围内的低风险文档。
- 有命令的地方必须可复制。
- 不接受危险 Revit 操作建议。
- 不接受企业级复杂化。
- 不接受核心代码改动。
## 只读代码试运行任务

Hermes/DeepSeek 当前可以承担文档、测试、只读静态检查任务。仍然不允许修改核心代码、安装脚本、addin 模板或 Revit 模型。

分支建议：

```powershell
hermes/read-only-checks
```

允许做：

- 运行 `python tools\static_checks.py --write-report`。
- 整理 `docs/drafts/static-check-report.md` 的结果。
- 修改 `docs/drafts/*.md` 草稿。
- 在新分支上新增只读测试草稿或审计报告。

禁止做：

- 不改 `pyrevit/**/script.py`。
- 不改 `src/**`。
- 不改 `scripts/**`。
- 不改 `addins/**`。
- 不运行 Revit。
- 不运行 install/build 脚本。
- 不做 git merge / push / pull。
- 不添加 `.rvt`。

任务：

1. 运行静态检查：

   ```powershell
   cd "G:\Hermes Agent\YangAgent Revit\YangAgent Revit"
   python tools\static_checks.py --write-report
   ```

2. 阅读生成的 `docs/drafts/static-check-report.md`。
3. 新增 `docs/drafts/hermes-static-check-review.md`，只写：
   - 发现了哪些 `ERROR`。
   - 发现了哪些 `WARN`。
   - 哪些是文档问题。
   - 哪些需要 Codex 判断。
4. 不直接修核心代码。

## Hermes 后续只读脚本检查

可以检查但不能修改：

- `scripts\build-revit-addin.ps1`
- `scripts\install-revit-addin.ps1`
- `scripts\build-revit2027-addin.ps1`
- `scripts\install-revit2027-addin.ps1`

检查目标：

- 2027 是否是唯一 implemented track。
- 2024/2025/2026 是否明确返回 `YA-CS-VERSION-PLANNED`。
- 文档是否没有把 2024/2025/2026 写成已经可构建。
