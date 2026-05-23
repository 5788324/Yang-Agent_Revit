# 下一步工作清单

当前阶段目标：让 Revit AI Agent 先具备“看懂模型、生成报告、让人确认”的能力。

## 已完成

- 2026-05-23 交接记录：`docs/handoff-2026-05-23.md`。
- 项目仓库初始化。
- GitHub 远程仓库连接。
- 项目方案文档。
- Claude 文档整合评审。
- 安全规则。
- 开发指南。
- Agent 提示词模板。
- pyRevit 只读工具：`Export Model Snapshot`。
- pyRevit 只读工具：`Model Health Report`。
- pyRevit 只读工具：`Export Regression Checklist`。
- pyRevit 只读工具：`Export AI Review Prompt`。
- pyRevit dry-run 工具：`Preview Missing Marks`。
- pyRevit dry-run 工具：`Preview Missing Room Numbers`。
- pyRevit dry-run 工具：`Preview Duplicate Room Numbers`。
- pyRevit dry-run 工具：`Preview Unplaced Views`。
- pyRevit dry-run 工具：`Preview Views By Naming Rules`。
- pyRevit 受控修改工具：`Apply Missing Door Window Marks`。
- pyRevit 受控修改工具：`Apply Missing Room Numbers`。
- 系统设置支持维护视图命名规则前缀和临时关键词。
- Revit 2027 C# `.addin + .dll` 正式插件骨架。

## 现在应该做什么

### 第 1 步：在本机安装 pyRevit 工具栏

先确认 Revit 里能看到 `pyRevit` 选项卡。如果看不到，请先安装 pyRevit。

运行：

```powershell
cd "D:\codex\Yang Agent_Revit"
.\scripts\install-pyrevit-extension.ps1
```

然后重启 Revit 或 reload pyRevit。

### 第 2 步：用测试模型运行工具箱

先不要用正式项目模型。

测试顺序：

1. 打开测试 Revit 模型。
2. 运行 `系统设置`，设置中文。
3. 运行 `导出报告 -> 导出路径`，选择一个项目报告目录。
4. 运行 `导出报告 -> 导出模型快照`。
5. 检查导出目录是否生成 JSON 和 CSV。
6. 运行 `导出报告 -> 模型健康报告`。
7. 检查是否生成中文 Markdown 报告。
8. 运行 `导出报告 -> 回归测试清单`。
9. 后续测试按生成的 Markdown 清单逐项记录 Pass / Fail。
10. 运行 `导出报告 -> AI分析提示词`。
11. 检查是否生成安全分析提示词和最近报告清单。
12. 运行 `导出报告 -> 预览缺失标记`。
13. 检查是否生成 dry-run Markdown 和 CSV。
14. 运行 `导出报告 -> 预览缺失房间编号`。
15. 检查是否生成 dry-run Markdown 和 CSV。
16. 运行 `导出报告 -> 预览重复房间编号`。
17. 检查是否生成 dry-run Markdown 和 CSV。
18. 运行 `导出报告 -> 预览未上图视图`。
19. 检查是否生成 dry-run Markdown 和 CSV。
20. 运行 `导出报告 -> 预览视图命名`。
21. 检查是否生成 dry-run Markdown 和 CSV。
22. 在测试模型中运行 `导出报告 -> 应用门窗标记`。
23. 选择已人工确认的 `missing_door_window_marks_*.csv`。
24. 检查是否生成 apply 日志，并确认 Revit 可一次撤销。
25. 在测试模型中运行 `导出报告 -> 应用房间编号`。
26. 选择已人工确认的 `missing_room_numbers_*.csv`。
27. 检查是否生成 apply 日志，并确认 Revit 可一次撤销。
28. 再运行 `系统设置`，设置 English。
29. 重复运行报告按钮，检查英文输出。

如果所有按钮都是灰色，优先清理 pyRevit 缓存并重启 Revit。

### 第 3 步：把报告交给 AI 分析

可以把 `model_health_report_*.md` 发给 Codex 或 Claude，然后问：

```text
请分析这份 Revit 模型健康报告，按严重程度列出问题。
只给建议，不要生成会直接修改模型的脚本。
```

### 第 4 步：选择一个低风险修复任务

建议优先选择：

- 缺少门窗标记检查。
- 缺少房间编号检查。
- 未上图视图检查。

不要一开始做：

- 删除元素。
- 批量重编号。
- 修改中心文件。
- 操作链接模型。

### 第 5 步：生成 dry-run 修复工具

下一轮开发目标：

- 整理一份标准测试模型，用于后续回归测试。
- 与 BIM 负责人确认公司实际视图命名规范，并通过 `系统设置` 写入本机规则。

## 判断是否进入下一阶段

满足以下条件后，再进入“受控修改”阶段：

- 只读和 dry-run 按钮能在测试模型稳定运行。
- 输出文件能被 AI 正确分析。
- BIM 负责人确认报告里的检查规则有价值。
- 用户确认哪些问题可以自动修复。

## 后续阶段

1. 在 Revit 2027 中加载 DLL 插件骨架。
2. 继续完善 pyRevit dry-run 修复脚本。
3. 把稳定的 pyRevit 功能迁移到 DLL。
4. 加入人工确认后的 `apply_*` 工具。
5. 开发只读 MCP。
6. 开发结构化 C# Bridge。
7. 做公司标准知识库。
