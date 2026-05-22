# C# 插件源码

正式 C# 插件代码放在此目录。

建议结构：

```text
YangAgent.Revit.Common/
YangAgent.Revit2024/
YangAgent.Revit2025/
YangAgent.Revit2027/
```

当前 MVP 优先使用 pyRevit 只读工具，C# Bridge 在后续阶段实现。

当前已新增：

```text
YangAgent.Revit2027/
```

这是 Revit 2027 `.addin + .dll` 正式插件骨架，目标框架为 `net10.0-windows`。

构建：

```powershell
.\scripts\build-revit2027-addin.ps1
```

安装：

```powershell
.\scripts\install-revit2027-addin.ps1
```
