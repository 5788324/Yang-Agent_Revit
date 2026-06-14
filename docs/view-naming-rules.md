# 视图命名规则

这份文档说明 `Preview View Naming Rules` 当前使用的规则来源和使用方式。

## 1. 当前作用

`Preview View Naming Rules` 是只读检查工具。

它会检查：

- 视图名是否包含临时关键词
- 常见视图类型是否缺少推荐前缀
- 是否存在明显不规范的命名问题

它不会直接重命名视图。

## 2. 规则保存位置

当前规则保存到本机设置：

```text
%APPDATA%\YangAgent_Revit\settings.json
```

不需要手工编辑时，推荐直接在 Revit 里改：

```text
YangAgent -> System Settings
```

## 3. 当前规则结构

规则核心包括两部分：

- `prefix_by_view_type`
- `temporary_keywords`

示例：

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

## 4. 推荐维护方式

优先在 `System Settings` 里维护：

- 不同视图类型的推荐前缀
- 临时关键词列表

多前缀之间用英文逗号分隔更稳。

## 5. 当前使用原则

这套规则是“审查建议”，不是绝对真理。

也就是说：

- 被标出来不一定就是错误
- 没被标出来也不等于完全合规

它更适合做：

- 命名整理前的清单
- 团队标准讨论前的初筛
- 模型健康报告中的一个维度

## 6. 与 ModelHealthReport 的关系

当前 `ModelHealthReport` 可以汇总视图命名问题，但它不应该依赖“先手动跑过 preview 按钮”。

更合理的做法是：

- 读取同一套规则
- 在自己的脚本里做等价检查
- 把结果汇总进健康报告

## 7. 当前注意事项

- 规则 key 保持英文稳定
- 用户可见文本可以中文
- 如果公司标准和默认规则冲突，以实际工作规则为准
- 修改规则后，重新运行 `Preview View Naming Rules` 才能看到效果

## 8. 相关文档

- `docs/user-guide.md`
- `docs/developer-guide.md`
- `docs/sandbox-pyrevit-mvp-runbook.md`
- `docs/error-codes.md`
