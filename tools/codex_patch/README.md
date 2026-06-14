# Codex Desktop Patch Helper

本目录不是 YangAgent Revit 的主线功能代码。

## 当前定位

这里存放的是针对本机 Codex Desktop / MSIX 环境的辅助修补脚本。

它与以下内容不同：

- 不属于 `pyrevit` 主线实现
- 不属于 Revit C# DLL 主线实现
- 不属于 sandbox preflight 必需链路

## 当前规则

- 只有在处理 Codex Desktop 本机环境问题时才考虑使用
- 不要把这里的脚本当作 YangAgent 产品能力
- 不要把这里的脚本纳入日常 Revit 功能开发范围

## 与主线的关系

YangAgent 当前主线仍然是：

```text
pyRevit MVP usable in a sandbox model
```

这个目录只保留为本机工具性旁支。
