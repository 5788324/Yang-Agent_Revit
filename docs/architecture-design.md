# 系统架构设计 (Architecture Design)

本文档描述 Yang Agent Revit 项目的整体架构设计，说明各个模块如何协同工作。

## 1. 核心模块与组件

本项目采用混合架构，结合了快速原型开发和高性能底层插件：

1. **pyRevit 脚本层 (Python 2.7 / pyRevit)**
   - **定位**：快速原型验证、只读数据导出、dry-run 逻辑。
   - **优势**：无需重启 Revit 即可更新代码，开发迭代极快。
   - **通信**：通过生成的 CSV/JSON 和 Markdown 报告与 AI 进行文件级的数据交换。

2. **C# .addin 正式插件层 (.NET / Revit API)**
   - **定位**：高性能、高稳定性、需要复杂 UI 操作或深度 Revit API 交互的功能。
   - **优势**：强类型、运行速度快、完全访问最新的 Revit API。

3. **MCP 服务层 (Model Context Protocol)**
   - **定位**：作为 AI Agent (如 Claude, Cursor, Antigravity) 和 Revit 之间的标准桥梁。
   - **功能**：提供只读上下文查询、工具调用接口，让 AI 可以自然语言查询 Revit 模型状态。

4. **大语言模型 (LLM) 协作层**
   - **定位**：代码生成、报告分析、自动化任务编排。
   - **工具**：Codex, Claude Code, Antigravity。

## 2. 数据流与交互工作流

### 场景 A：数据提取与分析 (只读)
1. 用户在 Revit 中点击 pyRevit 按钮。
2. 脚本使用 `FilteredElementCollector` 提取模型数据。
3. 数据被格式化并序列化为 JSON 或 CSV 保存到本地目录。
4. AI Agent 读取文件，进行分析并生成 Markdown 报告。

### 场景 B：AI 辅助受控修改 (Dry-run 机制)
1. AI Agent 编写/更新 pyRevit dry-run 脚本。
2. 脚本在 Revit 中运行，识别需要修改的元素，但不提交 Transaction，而是输出包含 ElementId 的“待修改清单”(CSV)。
3. 用户在 UI 弹窗中确认影响范围。
4. 确认后，执行 `apply_*` 脚本，读取 CSV，开启 Transaction，根据 ElementId 实际应用修改。

## 3. 部署架构

* **本地开发环境**：依赖本地 Revit、Visual Studio / VS Code，以及克隆的 Git 仓库。
* **分发环境**：通过局域网共享或内部脚本 (`install-pyrevit-extension.ps1`) 统一分发给 BIM 团队成员。
