# C# Source

本目录存放正式 C# 插件源码。

## 当前实际状态

- 当前已落地的 DLL 轨道：`YangAgent.Revit2027/`
- 当前主线重点：仍然是 pyRevit MVP
- DLL 当前只保留轻量入口，不承担大规模业务迁移

## 当前规则

- 不要把“更正式”误当成“现在就该迁移全部功能”
- 只有在有明确个人工作需求、且 pyRevit 路线不够时，再扩大 DLL 范围
- 不同 Revit 版本应保持独立轨道，不要假设一套 DLL 全兼容

## 相关脚本

构建与安装脚本在：

- `scripts/build-revit-addin.ps1`
- `scripts/install-revit-addin.ps1`

Revit 2027 便捷包装脚本在：

- `scripts/build-revit2027-addin.ps1`
- `scripts/install-revit2027-addin.ps1`
