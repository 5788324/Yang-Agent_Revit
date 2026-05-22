# 下一步工作清单

当前阶段目标：让 Revit AI Agent 先具备“看懂模型、生成报告、让人确认”的能力。

## 已完成

- 项目仓库初始化。
- GitHub 远程仓库连接。
- 项目方案文档。
- Claude 文档整合评审。
- 安全规则。
- 开发指南。
- Agent 提示词模板。
- pyRevit 只读工具：`Export Model Snapshot`。
- pyRevit 只读工具：`Model Health Report`。

## 现在应该做什么

### 第 1 步：在本机安装 pyRevit 工具栏

先确认 Revit 里能看到 `pyRevit` 选项卡。如果看不到，请先安装 pyRevit。

运行：

```powershell
cd "D:\codex\Yang Agent_Revit"
.\scripts\install-pyrevit-extension.ps1
```

然后重启 Revit 或 reload pyRevit。

### 第 2 步：用测试模型运行两个按钮

先不要用正式项目模型。

测试顺序：

1. 打开测试 Revit 模型。
2. 运行 `Export Model Snapshot`。
3. 分别测试 `中文` 和 `English`。
4. 检查桌面 `YangAgent_Revit_Exports` 是否生成 JSON 和 CSV。
5. 运行 `Model Health Report`。
6. 分别测试 `中文` 和 `English`。
7. 检查是否生成 Markdown 报告。

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

- `Preview Missing Door Window Marks`
- `Preview Missing Room Numbers`
- `Preview Unplaced Views`

这些工具只预览，不修改。

## 判断是否进入下一阶段

满足以下条件后，再进入“受控修改”阶段：

- 两个只读按钮能在测试模型稳定运行。
- 输出文件能被 AI 正确分析。
- BIM 负责人确认报告里的检查规则有价值。
- 用户确认哪些问题可以自动修复。

## 后续阶段

1. 加入 dry-run 修复脚本。
2. 加入人工确认后的 `apply_*` 工具。
3. 开发只读 MCP。
4. 开发结构化 C# Bridge。
5. 做公司标准知识库。
