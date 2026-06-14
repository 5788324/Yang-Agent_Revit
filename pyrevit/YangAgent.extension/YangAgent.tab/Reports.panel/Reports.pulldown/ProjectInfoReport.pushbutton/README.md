# Project Info Report

只读导出当前 Revit 项目的基础信息和统计摘要，作为 YangAgent 的项目理解入口之一。

## 输出内容

- 文档标题与路径
- Revit 版本
- 是否为 workshared 文档
- 中央模型路径摘要
- 当前视图
- 视图、图纸、标高、房间、门、窗数量
- 标题栏与工作集数量摘要

## 输出位置

输出到当前 YangAgent 报告目录，并生成：

```text
project_info_report_YYYYMMDD_HHMMSS.md
```

## 安全说明

此工具只读，不开启 Transaction，不修改模型。
