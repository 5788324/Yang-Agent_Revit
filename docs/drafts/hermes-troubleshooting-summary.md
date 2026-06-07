# 故障排查摘要

> 面向个人用户，覆盖最常见的 4 类问题。
> 完整版见 `docs/troubleshooting.md`

---

## 问题 1：pyRevit 按钮灰色 / 可用性命令载入失败

### 症状

按钮全部灰色，提示类似：

```
Revit无法运行可用性命令 ...
System.TypeLoadException
Could not resolve type ...
```

或

```
无法初始化附加模块
FullClassName 为 Revit 调用附加模块应用程序提供了入口点
```

### 原因

- pyRevit 生成的旧临时 DLL 或 `.cs` 缓存仍然被 Revit 读取。
- 中文目录名在 pyRevit 2027 中可能导致类型解析失败（项目已修复为英文目录名）。
- 旧缓存文件未清理。

### 处理步骤

1. **完全关闭 Revit**（包括 Revit 2025/2026/2027 等所有实例）。
2. 打开任务管理器，确认没有 `Revit.exe` 或 `RevitWorker.exe` 进程。若仍存在进程，优先回到 Revit 正常保存并关闭；不要在有未保存工作时强行结束进程。
3. 运行缓存清理 + 重装：

```powershell
.\scripts\install-pyrevit-extension.ps1 -Force -ClearCache
```

4. 重新打开 Revit。
5. 在 pyRevit 选项卡中点击 **Reload**。

> 如果仍有问题：运行 `.\scripts\clear-pyrevit-yangagent-cache.ps1` 手动清理，再执行第 3 步。

---

## 问题 2：pyRevit 缓存未更新

### 症状

- 改了脚本但按钮行为没变。
- 删了按钮但在 Revit 中还能看到。

### 原因

pyRevit 使用缓存来加速加载。如果缓存没有自动刷新，旧版本的工具仍在生效。

### 处理步骤

1. 关闭 Revit。
2. 运行：

```powershell
.\scripts\install-pyrevit-extension.ps1 -Force -ClearCache
```

3. 重新打开 Revit → pyRevit Reload。

---

## 问题 3：C# DLL 被 Revit 锁定

### 症状

构建时报错：

```
DLL is locked and cannot be overwritten: ...YangAgent.Revit2027.dll.
Locked by Revit process id(s): ...
```

### 原因

Revit 已加载 DLL，Windows 锁定该文件，无法覆盖。

### 处理步骤

1. 保存测试模型。
2. **完全关闭 Revit 2027**。
3. 打开任务管理器 → 确认没有 `Revit.exe`。
4. 重新构建 + 安装：

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\build-revit2027-addin.ps1
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\install-revit2027-addin.ps1
```

> 如果只想验证代码能否编译、暂时不覆盖 DLL：
> ```powershell
> dotnet build .\src\YangAgent.Revit2027\YangAgent.Revit2027.csproj -c Debug -o C:\tmp\YangAgent_Revit2027_build_check
> ```

---

## 问题 4：PowerShell 执行策略

### 症状

运行 `.ps1` 脚本时报错：

```
File ... cannot be loaded because running scripts is disabled on this system.
```

### 原因

Windows PowerShell 默认禁止运行未签名的脚本（`Restricted` 执行策略）。

### 处理步骤

**方法 A（推荐）：临时绕过当前脚本**

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\install-pyrevit-extension.ps1
```

**方法 B：永久改为 RemoteSigned（仅当前用户）**

```powershell
Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned
```

> `RemoteSigned`：本地脚本可直接运行，从网上下载的脚本需要右键"解除锁定"。

---

## 快速诊断流程图

```
按钮灰色 / 报错？
├─ 已关闭所有 Revit？ → 否 → 先关闭
├─ 任务管理器无 Revit.exe？ → 否 → 先正常保存并关闭 Revit
├─ 运行了 -Force -ClearCache？ → 否 → 运行
├─ 重启 Revit 后 Reload 了？ → 否 → Reload
└─ 还不行？ → 手动运行 clear-pyrevit-yangagent-cache.ps1，再重复
```

---

## 相关文档

| 文档 | 内容 |
|------|------|
| `docs/troubleshooting.md` | 完整故障排查（含 C# DLL、pyRevit 缓存位置等） |
| `docs/error-codes.md` | 所有错误码及含义 |
| `README.md` | 安装和构建脚本参考 |
