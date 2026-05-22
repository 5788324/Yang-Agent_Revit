# Model Health Report

只读生成模型健康检查报告。

## 检查内容

- 房间缺少编号。
- 房间缺少名称。
- 房间编号重复。
- 门缺少标记。
- 窗缺少标记。
- 可能未放置到图纸的视图。

## 输出位置

默认输出到桌面：

```text
YangAgent_Revit_Exports/
```

生成文件：

```text
model_health_report_YYYYMMDD_HHMMSS.md
```

## 安全说明

此工具不修改模型，不开启 Transaction。
