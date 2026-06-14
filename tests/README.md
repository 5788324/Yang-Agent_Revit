# Tests

本目录存放当前主线可复用的测试夹具和测试说明。

## 当前状态

当前测试重点仍然偏离线验证，而不是完整 Revit 自动化。

现有重点包括：

- apply CSV fixture
- preview/apply 输入校验
- preflight 相关检查支持

## 现有夹具

`tests/fixtures/` 当前包含：

- 房间编号 apply 的合法/重复 CSV
- 门窗标记 apply 的合法/重复 CSV

## 当前原则

- 先保证输入校验和离线链路可靠
- 再做 live Revit 验证
- 不把“有 fixture”误当成“真实 Revit 已验证”

## 后续可扩展方向

- 更多错误输入 fixture
- 报告输出结构断言
- 针对共享库的更细粒度离线检查
