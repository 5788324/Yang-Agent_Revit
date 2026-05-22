# 故障排查

## 1. Revit 中看不到 YangAgent

先确认 Revit 中能看到 `pyRevit` 选项卡。

如果没有，说明 pyRevit 没有安装或没有加载。

## 2. 按钮都是灰色，提示“可用性命令载入失败”

典型报错：

```text
Revit无法运行可用性命令 ...
System.TypeLoadException
Could not resolve type ...
```

原因：

- pyRevit 会根据 `.panel` 和 `.pushbutton` 目录名生成临时 DLL 类型。
- 中文目录名可能导致 pyRevit 2027 生成的 availability 类型无法解析。
- `bundle.yaml` 中的 `context:` 会触发 availability 命令生成。

项目修复：

- `.panel` 目录已改为英文 ASCII：`Settings.panel`、`Reports.panel`。
- 按钮目录保持英文 ASCII。
- 中文显示名放在 `bundle.yaml` 的 `title`。
- 已移除 `context:` 声明。

用户处理步骤：

1. 关闭 Revit。
2. 更新仓库到最新版本。
3. 清理 pyRevit 缓存中旧的 YangAgent 临时 DLL。
4. 重新打开 Revit。
5. 在 pyRevit 中 reload。

如果不确定缓存位置，可以在用户临时目录或 pyRevit 缓存目录里搜索：

```text
*YangAgent*.dll
```

删除旧缓存后，pyRevit 会重新编译工具箱。

## 3. 提示“外部工具-完整类名称错误”

典型报错：

```text
无法初始化附加模块“导出路径”
FullClassName 为 Revit 调用附加模块应用程序提供了入口点
必须确保该类实现 Autodesk.Revit.UI.IExternalCommand
```

原因通常不是业务脚本没有实现 `IExternalCommand`。pyRevit 会自动把 `script.py` 包装成 Revit 外部命令，这个错误多半来自旧的 pyRevit 临时 DLL 或旧 `.addin` 缓存仍在被 Revit 读取。

处理步骤：

1. 完全关闭 Revit。
2. 更新仓库到最新版本。
3. 执行缓存清理脚本：

```powershell
.\scripts\clear-pyrevit-yangagent-cache.ps1
```

4. 重新安装或刷新 pyRevit extension：

```powershell
.\scripts\install-pyrevit-extension.ps1 -Force -ClearCache
```

5. 重新打开 Revit，并执行 pyRevit Reload。

项目修复：

- `.panel` 目录使用无中文英文名。
- `.pushbutton` 目录使用无空格英文名。
- UI 中文显示名只放在 `bundle.yaml` 的 `title` 中。

## 4. 仍然无法点击

请检查：

- `pyrevit/YangAgent.extension/YangAgent.tab` 下是否只有英文 `.panel` 目录。
- `.pushbutton` 目录是否是无空格英文名。
- `bundle.yaml` 中是否没有 `context:`。
- Revit 是否已经完全重启。
- pyRevit 是否已经 reload。
