# 视图命名规则配置

`预览视图命名` 工具默认使用一套保守规则检查视图名称。

规则保存在本机设置文件中：

```text
%APPDATA%\YangAgent_Revit\settings.json
```

如果没有配置，工具会使用默认规则。

## 默认规则

```json
{
  "view_naming_rules": {
    "prefix_by_view_type": {
      "FloorPlan": ["FP-", "PL-", "A-", "S-", "M-", "E-"],
      "CeilingPlan": ["RCP-", "CP-"],
      "Section": ["SEC-", "SECTION-"],
      "Elevation": ["EL-", "ELEV-"],
      "ThreeD": ["3D-"],
      "DraftingView": ["DR-", "DET-", "DT-"],
      "Legend": ["LG-", "LEG-"],
      "AreaPlan": ["AR-", "AREA-"],
      "EngineeringPlan": ["EP-", "ENG-"]
    },
    "temporary_keywords": [
      "临时",
      "测试",
      "工作",
      "temp",
      "test",
      "working",
      "copy",
      "复制"
    ]
  }
}
```

## 调整建议

- 先让 BIM 负责人确认公司视图命名标准。
- 只修改 `prefix_by_view_type` 和 `temporary_keywords`。
- JSON key 保持英文，不要改成中文。
- 修改后重新运行 `导出报告 -> 预览视图命名`。
- 确认规则稳定后，再考虑开发真正修改视图名称的 apply 工具。
