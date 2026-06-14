# YangAgent pyRevit Extension

这是当前仓库的主线实现入口。

## 当前结构

- `lib/`
  - 共享逻辑
  - 语言、设置、主题、报告样式、apply helper
- `YangAgent.tab/Settings.panel/`
  - 系统设置入口
- `YangAgent.tab/Reports.panel/Reports.pulldown/`
  - 报告、预览、低风险 apply 工具

## 当前功能类型

### 设置类

- `System Settings`

### 只读导出 / 报告类

- `Project Info Report`
- `Export Model Snapshot`
- `Model Health Report`
- `Export Regression Checklist`
- `Export AI Review Prompt`

### Preview / dry-run 类

- `Preview Missing Door Window Marks`
- `Preview Missing Room Numbers`
- `Preview Duplicate Room Numbers`
- `Preview Unplaced Views`
- `Preview View Naming Rules`

### 低风险 apply 类

- `Apply Missing Door Window Marks`
- `Apply Missing Room Numbers`

## 当前规则

- 报告和 preview 工具默认只读
- apply 工具必须读取对应 dry-run CSV
- apply 工具必须在 `Transaction` 中执行
- 所有模型修改必须保留日志与 Undo 检查语义
- 用户可见文本支持中文和 English
- 机器可读字段保持稳定英文

## 当前优先级

这个 extension 的目标不是“功能越多越好”，而是先把 sandbox 模型里的主链路跑通并稳定下来。
