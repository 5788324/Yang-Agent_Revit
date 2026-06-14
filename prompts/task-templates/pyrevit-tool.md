# pyRevit Tool Template

请根据下面需求生成或修改 pyRevit 工具。

## 硬规则

1. 先说明该工具是否会修改模型
2. 如果会修改模型，必须先提供 preview 或 dry-run
3. 所有修改必须放在 `Transaction` 中
4. 批量修改前必须输出影响数量和关键元素信息
5. 代码兼容 IronPython 2.7 风格
6. 避免 f-string、类型注解、walrus 运算符
7. 输出完整 pyRevit bundle 结构
8. 给出使用说明和测试步骤
9. 支持中文和 English
10. 用户可见输出跟随语言设置
11. JSON key 和机器字段保持稳定英文

## 当前项目语境

- 当前主线是 sandbox 可用的 pyRevit MVP
- 先收敛到实用、安全、可验证
- 不要为了“架构完整”引入不必要复杂度

需求：

```text
{用户需求}
```
