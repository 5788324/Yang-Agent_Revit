# `.addin + .dll` 正式插件开发计划

## 1. 为什么需要 DLL 插件

pyRevit 适合快速验证，C# DLL 插件适合公司正式部署。

DLL 插件优势：

- 更稳定。
- 更适合长期维护。
- 更适合复杂窗口。
- 更适合受控修改模型。
- 更适合公司统一安装和版本管理。

## 2. 版本策略

当前先建立 Revit 2027 骨架。

原因：

- 你本机已经安装 Revit 2027。
- Revit 2027 使用 .NET 10。
- 本机已安装 .NET SDK 10.0.300。

后续再补：

- Revit 2025：.NET 8。
- Revit 2022 / 2024：.NET Framework 4.8。

## 3. 目录结构

```text
src/
  YangAgent.Revit2027/
    YangAgent.Revit2027.csproj
    App.cs
    Commands/
      AboutCommand.cs
      OpenSettingsCommand.cs
      ExportReportPlaceholderCommand.cs
addins/
  Revit2027/
    YangAgent.Revit2027.addin.template
scripts/
  build-revit2027-addin.ps1
  install-revit2027-addin.ps1
```

## 4. 当前 C# 骨架目标

第一版 DLL 只做这些：

- Revit 启动时创建 `YangAgent` 选项卡。
- 创建 `系统设置` 面板。
- 创建 `导出报告` 面板。
- 放入几个占位按钮。
- 点击按钮显示说明弹窗。
- 打开本机 YangAgent 配置目录。
- 打开默认报告导出目录。

第一版 DLL 不做：

- 不修改模型。
- 不读取真实模型数据。
- 不替代 pyRevit 工具。
- 不实现复杂界面。

## 4.1 当前构建结果

当前 Revit 2027 DLL 骨架已在本机通过 `dotnet build`，并已安装到当前用户 Revit 2027 Addins 目录。

构建环境：

- .NET SDK：10.0.300。
- Revit：2027。
- 目标框架：`net10.0-windows`。
- Addin 清单：`%APPDATA%\Autodesk\Revit\Addins\2027\YangAgent.Revit2027.addin`。

注意：构建时可能出现 `MSB3277` 相关警告，这是 Revit API 引用链和 .NET 引用版本之间的提示。当前骨架没有编译错误，可以继续使用。

当前真实 DLL 功能：

- `系统设置 -> 关于更新`：显示版权和更新链接。
- `系统设置 -> 配置目录`：打开 `%APPDATA%\YangAgent_Revit`。
- `导出报告 -> 报告目录`：打开桌面默认 `YangAgent_Revit_Exports`。
- 其它按钮仍为占位说明，不读取或修改 Revit 模型。

## 5. 后续迁移顺序

建议先迁移：

1. 关于更新。
2. 系统设置窗口。
3. 报告导出路径设置。
4. 模型健康报告。
5. 模型快照导出。
6. dry-run 预览工具。

最后才迁移：

- apply 写入工具。
- 批量改参数。
- 批量重编号。

## 6. 安全规则

C# 插件也必须遵守：

- 默认只读。
- 修改前 dry-run。
- 修改前显示影响数量。
- 修改必须使用 Transaction。
- 高风险操作必须二次确认。
- 所有输出必须有日志。
## Current Multi-Version Boundary

- First phase targets Revit 2024-2027 only.
- Revit 2011-2023 are deferred backlog targets, not current support.
- Revit 2024, 2025/2026, and 2027 should use separate C# projects and separate `.addin` templates.
- Current Revit 2027 DLL scope stays small: ribbon, about, config folder, report folder, and placeholder commands.
- See `docs/revit-version-support-plan.md` for the authoritative version support wording.
