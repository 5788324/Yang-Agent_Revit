# 开源 MCP 工具调研与推荐 (Model Context Protocol)

> Historical reference only.
>
> MCP remains a future goal for automatic model reading and controlled preview/apply modification. It is not the current one-week delivery target.

在 Revit AI Agent 的演进路线中，我们需要让大语言模型（如 Claude Desktop、Cursor 或 Antigravity）直接读取并操作 Revit 模型上下文。这就需要借助 MCP (Model Context Protocol) 标准。

## 当前开源生态与可行方案

### 1. Autodesk 官方支持 (Revit 2027+)
- **状态**: Technical Preview
- **说明**: 从 Revit 2027 开始，Autodesk 内置了一个官方的 MCP Server，当 Revit 打开时在后台自动运行。
- **优点**: 原生、安全控制严格、集成度高。
- **缺点**: 仅限 2027 及以上版本，对我们要求支持的 2022-2025 无法直接使用。

### 2. 社区开源 MCP 桥接方案
对于老版本 Revit (2022-2025)，社区的主流做法是开发一个“双端桥接 (Dual-bridge)”架构：
1. **Revit Addin (C#)**: 在 Revit 内部启动一个本地的 HTTP 或 WebSocket 监听器。
2. **MCP Server (Node.js/Python)**: 暴露标准的 MCP 接口给 Claude，将请求转发给 Revit 内部的 WebSocket。

**推荐关注的 GitHub 项目与思路**：
- **[snyk.io/mcpservers.org 相关示例]**: 有许多演示如何把传统桌面软件包装成 MCP 的模板。
- **Revit API 封装器 (如 Revit.Async / pyRevit 本身)**: 如果基于 pyRevit，其实可以通过 pyRevit 提供的 `pyrevit.api` 和 `System.IO.Pipes` 或者简单的本地 TCP Socket，自己用 Python 写一个轻量级服务端。

### 3. ACC/BIM 360 云端 MCP
- 如果不直接操作本地模型，而是操作 Autodesk Construction Cloud 中的模型，可以利用 Forge/APS (Autodesk Platform Services) 结合 Node.js 快速搭建 MCP Server。
- **优点**: 摆脱本地环境限制，适合纯数据提取和分析。
- **缺点**: 无法实时控制当前工程师桌面的 UI。

## 我们项目的 MCP 演进计划
鉴于现有开源方案大多需要双端通信，本项目后续阶段（如 `mcp/` 目录所示）将：
1. 优先使用 Python/pyRevit 在本地抛出一个简单的 HTTP 端口（只读）。
2. 用标准的 Python MCP SDK (`mcp` python 包) 包装该端口。
3. 让 Cursor / Claude Desktop 直接将其配置为 `command: "python", args: ["local_mcp_server.py"]` 的标准 MCP 服务。
