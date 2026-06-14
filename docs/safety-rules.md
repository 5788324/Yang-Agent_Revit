# YangAgent Revit 安全规则

这份文档定义当前主线的最低安全边界。

当前项目定位：

- 个人自用 Revit AI 助手
- 当前主线是 pyRevit MVP
- 先在 sandbox 模型里跑通
- 不直接碰生产模型

## 1. 默认只读

除非工具名字、说明和交互流程明确表示会修改模型，否则一律按只读工具处理。

只读工具允许做：

- 读取当前文档信息
- 读取视图、图纸、房间、门、窗等模型数据
- 导出 JSON / CSV / Markdown 报告
- 生成 AI 分析提示包
- 生成 dry-run 预览结果

只读工具不允许做：

- 修改参数
- 重命名元素
- 删除元素
- 创建新元素
- 保存中心模型

## 2. 模型修改必须走固定链路

所有改模型工具必须遵守：

```text
preview / dry-run -> human confirmation -> apply -> log -> Undo note
```

最低要求：

- 先给出预览结果
- 明确影响元素数量
- 明确给出 `ElementId`
- 明确当前模型名
- 用户二次确认后才 apply
- 生成日志文件
- 说明 Undo 是否已实际验证

缺任一项，都不能算合格的模型修改工具。

## 3. 禁止直接改生产模型

开发、测试、第一次运行、外部 AI 交付验证，都只能用：

- `*_sandbox.rvt`
- `*_test.rvt`
- 本地可丢弃副本

禁止：

- 直接在正式项目模型上试新功能
- 直接在中心模型上试新功能
- 直接在云模型上试新功能

## 4. 批量修改必须可审计

批量修改前必须能回答这些问题：

- 会改多少个元素？
- 具体是哪些 `ElementId`？
- 改哪个参数？
- 原值是什么？
- 建议值是什么？

批量修改后必须留下：

- Markdown 日志
- CSV 结果或等价结构化结果
- applied / skipped / failed 统计

## 5. Revit API 事务规则

所有真正写模型的操作必须放进 `Transaction`。

要求：

- 事务名清晰
- 失败时可中止
- 不在只读工具里开启事务

pyRevit 工具当前规则：

- 只读工具：不使用 `Transaction`
- apply 工具：使用 `with revit.Transaction(...)`

## 6. 高风险操作当前默认不做

当前主线默认不接受这些能力进入可用状态：

- 无确认删除元素
- 广泛批量重命名且无预览
- 自动修改中心模型
- 自动处理链接模型
- 动态执行任意 Python/C# 代码去改模型
- MCP 直接暴露任意写模型接口
- 自动启动后台服务后直接写模型

这些以后如要做，必须单独设计安全壳。

## 7. 外部 AI 安全边界

Hermes / Gemini / DeepSeek 等外部辅助体：

- 可以读代码
- 可以写局部草稿
- 可以写文档和审查报告
- 可以在被授权范围内改某个按钮目录

但它们不能：

- 自行定义模型修改行为
- 跳过预览链路
- 改共享安全规则后不回报
- 宣称 live Revit 已验证，除非有证据

## 8. 数据边界

客户模型和项目数据默认留在本地。

优先输出到本地文件：

- JSON
- CSV
- Markdown

没有明确批准前，不默认发到外部服务。

## 9. 当前最重要的验证口径

当前阶段最重要的不是“功能多”，而是：

- 能在 sandbox 里稳定打开
- 只读报告能稳定导出
- preview 工具能稳定给出结果
- apply 工具能在受控链路下运行
- Undo 至少在 sandbox 中实际测过

## 10. 相关文档

- `docs/product-brief.md`
- `docs/project-rules.md`
- `docs/testing-and-qa.md`
- `docs/sandbox-pyrevit-mvp-runbook.md`
- `docs/sandbox-pyrevit-mvp-checklist.md`
- `docs/error-codes.md`
