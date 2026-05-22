# AI 协作开发流程

本项目允许 Codex、Claude Code、Antigravity 和人工开发者一起工作，但必须遵守同一套边界。

## 1. 分工建议

- Codex：本地代码修改、排错、脚本、测试、Git 提交、整理开发文档。
- Claude Code：长文档整理、需求拆解、代码审阅、复杂方案对比。
- Antigravity：多文件工程导航、原型探索、界面/插件结构调整。
- 人工开发者：最终确认需求、在 Revit 中试运行、判断工具是否符合公司习惯。

## 2. 分支规则

不要多人同时直接改 `main`。

建议分支命名：

```text
feature/report-export-path
fix/pyrevit-cache-loading
docs/colleague-guide
experiment/dll-addin
```

每个 AI 平台或同事一次只负责一个小任务。任务完成后通过 Pull Request 合并。

## 3. 每次开发前

```powershell
git status
git pull
```

确认没有未保存的本地修改。如果有修改，先提交、暂存或问清楚是谁改的。

## 4. 每次开发后

```powershell
git status
git diff --check
```

pyRevit 工具还要检查：

- `.panel` 和 `.pushbutton` 目录名只用无空格英文。
- 中文界面文字放在 `bundle.yaml` 或脚本语言表里。
- 不使用 `context:`，避免 Revit 2027 可用性命令加载失败。
- 新功能默认只读；要修改模型时必须先做 dry-run。

## 5. 给 AI 的任务模板

```text
请在 Yang-Agent_Revit 仓库中开发/修复：

目标：
- 

限制：
- Revit 2027 + pyRevit 优先
- pyRevit 目录名必须无空格英文
- UI 需要中英双语
- 默认只读，不修改模型
- 修改模型必须先提供 dry-run

完成后：
- 更新 docs/user-guide.md 或 docs/developer-guide.md
- 运行能运行的检查
- 说明无法在 Revit 中验证的部分
```

## 6. 冲突处理

如果 Codex、Claude Code、Antigravity 改了同一批文件，先不要让任何一个 AI 自动覆盖。

处理顺序：

1. 看 `git status`。
2. 看 `git diff`。
3. 保留已经能在 Revit 中工作的版本。
4. 把另一个版本的好想法拆出来单独合并。

## 7. 发布给同事

发布前至少确认：

- Revit 能看到 YangAgent 选项卡。
- 按钮不是灰色。
- 系统设置、语言切换、导出路径能打开。
- 报告输出到用户选择的目录。
- 没有提交公司模型、客户数据、账号密钥。
