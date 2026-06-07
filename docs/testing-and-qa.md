# 测试与质量保证规范 (Testing & QA)

在执行任何可能修改模型的 Agent 自动化任务前，必须遵循本测试规范。

## 1. 测试环境要求

* **隔离环境**：必须在名为 `*_test.rvt` 或 `*_sandbox.rvt` 的测试模型上进行开发和测试。
* **脱机操作**：测试模型应当是从正式服务器/BIM 360 下载到本地的离线（分离）文件，禁止直接在共享云模型上进行代码调试。

## 2. 工具发布标准 (Definition of Done)

所有 pyRevit 脚本或 C# 插件在合入主分支并向团队发布前，必须满足以下条件：

1. **多语言支持**：界面提示和导出文件必须同时支持中文和英文切换。
2. **Dry-Run 机制**：任何涉及修改的功能，必须存在对应的“预览 (Preview)”模式。
3. **Transaction 约束**：所有改动被包裹在 `revit.Transaction` 中，名称要易于用户在“撤销(Undo)”历史中识别，如 `[Agent] 批量修改门标记`。
4. **日志记录**：失败或异常情况必须记录在日志文件中，而不是直接导致 Revit 崩溃。
5. **用户二次确认**：批量修改前弹出汇总数量，如“即将修改 15 樘门，是否继续？”。

## 3. 回归测试流程

当新增工具或进行版本升级时，按以下流程进行回归测试：

1. 打开标准测试模型 (如 `samples/test_model.rvt`)。
2. 运行 `导出报告 -> 回归测试清单`，生成 `yangagent_regression_checklist_*.md`。
3. 按清单运行所有现有的只读工具，比对输出的 JSON/CSV 是否存在格式突变。
4. 运行现有的 Dry-Run 工具，确认识别出的待处理 Element 数量无误。
5. 对于修改类工具，必须先运行 dry-run，人工检查 CSV，再执行 Apply。
6. Apply 后必须确认可以通过 Revit 撤销。
7. 填写测试清单结果；不要提交 `.rvt` 模型到 Git。

## 4. 不依赖 Revit 的静态检查

在没有打开 Revit 的情况下，可以先运行只读检查：

```powershell
cd "D:\codex\Yang Agent_Revit"
python tools\static_checks.py --write-report
```

该脚本只扫描仓库文件，不运行 Revit，不运行安装脚本，不修改模型。

当前检查范围：

- pyRevit 按钮目录是否缺少 `bundle.yaml`、`script.py`、`README.md` 或 `icon.png`。
- 文档里的 PowerShell 命令是否可能不可复制。
- 文档是否把 Revit 2011-2027 写成已支持。

Hermes/DeepSeek 可以运行这个脚本并整理报告，但不能据此直接修改核心代码。
