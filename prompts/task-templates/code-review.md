# Revit Code Review Template

请以 Revit / pyRevit 代码审查者身份检查代码。

优先审这些问题：

1. 是否违反 Revit API 执行上下文或线程约束
2. 是否缺少 `Transaction` 或误用 `Transaction`
3. 是否可能误改、误删、误保存模型
4. 是否有版本兼容风险
5. 是否存在空值、参数缺失、单位处理等常见错误
6. 是否缺少日志、错误提示、确认链路
7. 是否符合当前 YangAgent 安全规则
8. 如果是 pyRevit，是否兼容 IronPython 风格约束

审查输出应优先包含：

- 风险点
- 可能的行为回归
- 缺失的验证
- 是否适合进入 sandbox live 测试

待审代码：

```text
{代码}
```
