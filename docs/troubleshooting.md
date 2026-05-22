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

## 3. 仍然无法点击

请检查：

- `pyrevit/YangAgent.extension/YangAgent.tab` 下是否只有英文 `.panel` 目录。
- `bundle.yaml` 中是否没有 `context:`。
- Revit 是否已经完全重启。
- pyRevit 是否已经 reload。
