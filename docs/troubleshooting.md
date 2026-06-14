# 故障排查

本文件只保留当前 MVP 阶段最常见、最高频的问题。

适用范围：

- 仓库路径：`G:\Codex\YangAgent Revit\YangAgent Revit`
- 当前主线：`pyrevit/YangAgent.extension`
- 当前重点：Sandbox 测试模型中的 pyRevit MVP

## 1. Revit 里看不到 `YangAgent` 选项卡

先确认：

1. Revit 里是否能看到 `pyRevit` 选项卡。
2. `pyrevit/YangAgent.extension` 是否已经安装或链接到 pyRevit。
3. 当前机器是否已经重启过 Revit，而不是只在仓库里改了文件。

优先处理：

- 如果连 `pyRevit` 都看不到，先排 pyRevit 安装或加载问题。
- 如果能看到 `pyRevit`，但看不到 `YangAgent`，优先检查 extension 安装、缓存和目录命名。

## 2. 按钮是灰色，或提示可用性命令加载失败

典型现象：

- 按钮显示但不可点击；
- Revit/pyRevit 提示 `System.TypeLoadException`；
- 提示 availability 类或命令包装类无法加载。

当前已知高频原因：

- `.panel` 或 `.pushbutton` 目录命名不符合 pyRevit 约束；
- 旧缓存中的临时 DLL 仍在被 Revit 使用；
- `bundle.yaml` 历史写法触发了旧可用性命令缓存。

当前项目约束：

- `.panel`、`.pushbutton` 目录名只用英文 ASCII；
- 中文显示名只放在 `bundle.yaml` 的 `title`；
- 不要随意恢复旧的 `context` 写法，除非明确验证需要。

处理步骤：

1. 完全关闭 Revit。
2. 确认仓库已经更新到当前主线。
3. 清理 pyRevit 的 YangAgent 相关缓存。
4. 重新打开 Revit。
5. 在 pyRevit 中执行 `Reload`。

如果要手动搜索缓存，可搜：

```text
*YangAgent*.dll
*YangAgent*.cs
*YangAgent*.pickle
```

## 3. 启动时报 `FullClassName` / `IExternalCommand` 相关错误

典型报错：

```text
Failed to initialize the add-in ...
The FullClassName provides the entry point ...
must implement Autodesk.Revit.UI.IExternalCommand
```

这类问题在当前项目里通常不代表业务脚本真的没实现 `IExternalCommand`，更常见原因是：

- pyRevit 旧临时 DLL 还在；
- Revit 仍锁着旧缓存；
- 历史 `.addin` 或旧构建残留仍被扫描。

优先处理：

1. 完全关闭 Revit。
2. 确认任务管理器里没有 `Revit.exe`、`RevitWorker.exe`。
3. 清理 pyRevit / YangAgent 相关缓存。
4. 重新打开 Revit 后再测。

如果问题出在新按钮上，优先怀疑缓存，不要先怀疑业务脚本本身。

## 4. `System Settings` 能开，其他按钮打不开

这通常说明：

- extension 主体已经被识别；
- 问题更可能在单个按钮脚本、按钮目录、共享库 import 或缓存。

排查顺序：

1. 先试 `Project Info Report` 这类最轻量、只读按钮。
2. 再试 `Model Health Report`。
3. 再试 preview 类按钮。
4. 最后才试 apply 类按钮。

如果只有单个按钮失败，记录：

- 按钮名；
- 原始错误文本；
- 是否有导出文件生成；
- 同一面板的其他按钮是否正常。

## 5. Apply 类按钮执行前就失败

先确认是不是输入文件问题，而不是 Revit API 问题。

当前 Apply 安全链路要求：

```text
preview/dry-run -> human confirmation -> apply -> log -> Undo check
```

先检查：

- 选择的 CSV 是否来自当前 preview；
- 文件名是否匹配约定；
- `element_id` 是否重复；
- `dry_run` 是否仍为 `true`；
- 是否在 sandbox 模型里测试。

离线先跑：

```powershell
python tools\run_sandbox_preflight.py --write-report
```

如需进一步看错误码，直接查：

- `docs/error-codes.md`

## 6. 报告导出路径不对，或找不到文件

先看 `System Settings` 中的导出路径设置。

当前已知测试报告目录：

```text
G:\Codex\YangAgent Revit\YangAgent Revit\Gemini 资料\Revit 测试模型\报告
```

排查顺序：

1. 在 `System Settings` 中确认当前导出目录。
2. 重新执行一个只读导出按钮，例如 `Project Info Report`。
3. 按修改时间排序查看目标目录。
4. 如果按钮显示成功但目录没有新文件，再回看 pyRevit 输出。

## 7. C# DLL 构建时提示 DLL 被锁定

典型现象：

```text
DLL is locked and cannot be overwritten
```

原因：

- Revit 正在占用当前 DLL；
- Windows 不允许覆盖已加载的程序集。

处理步骤：

1. 保存测试模型。
2. 完全关闭 Revit 2027。
3. 确认没有残留 `Revit.exe`。
4. 再执行构建或安装脚本。

如果只是验证能否编译，而不想覆盖当前 DLL，可改用单独输出目录。

## 8. 什么时候该停，不要继续乱试

出现以下任一情况，先停：

- 不是 sandbox 模型；
- apply 按钮已经准备改模型，但你还没看影响范围；
- 同一个错误连续重复，且没有新增证据；
- Revit 已经弹出模型修改相关确认，但你不清楚会改什么；
- 你无法确认当前按钮是 preview 还是 apply。

当前策略不是一次跑完所有按钮，而是尽快拿到第一个真实 blocker，然后定点修复。
