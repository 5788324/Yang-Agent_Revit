# API And Data Schema

本文件记录当前主线仍然有效的最小数据结构约束。

它不是完整平台 API 设计，只服务于当前 pyRevit MVP、报告导出、preview/apply 链路和未来受控 MCP 接入。

## 1. 基本原则

所有机器可读输出优先满足这几个规则：

1. 结构稳定。
2. 字段名使用稳定英文。
3. 需要回写或定位元素时，必须带 `element_id`。
4. 用户显示语言可以中英切换，但 JSON key / CSV header 不跟着切换。
5. 当前主线不为“漂亮”破坏机器可读稳定性。

## 2. 输出格式选择

- 复杂层级数据：优先 `JSON`
- 扁平清单、可人工审阅的批次结果：优先 `CSV`
- 给用户阅读、给 AI 解释、给交付留证据：优先 `Markdown`

## 3. Preview / Apply CSV 最小约束

所有会进入 apply 链路的 CSV，都应符合：

- 来自对应 preview，而不是手工拼接
- 文件名符合按钮约定
- 包含稳定英文列名
- `element_id` 可解析
- `dry_run` 在 preview 导出时应为 `true`
- 同一个文件内不允许重复 `element_id`

当前 apply 逻辑应围绕：

```text
preview / dry-run -> confirmation -> apply -> log -> Undo check
```

## 4. Model Snapshot JSON 最小约束

模型快照类 JSON 至少应支持表达：

- 生成时间
- 项目基础信息
- 关键数量统计
- 可选的 warning / issue 列表
- 能被后续 AI 和脚本稳定解析

推荐字段保持英文，例如：

- `generated_at`
- `project_info`
- `statistics`
- `issues`

## 5. Markdown 报告最小约束

所有正式报告或 dry-run 报告应：

- 带生成时间
- 带来源按钮或功能名
- 用稳定标题层级
- 必要时附 summary/table/status block
- 不为了排版牺牲后续 AI 可读性

## 6. 本地设置结构

本地设置文件中的 key 保持稳定英文。

当前高优先级设置包括：

- `language`
- `theme_id`
- `export_dir`

如果某类规则需要配置，例如视图命名规则，也应保持：

- 机器字段英文
- 用户说明可以双语

## 7. 与未来 MCP 的关系

如果以后进入 MCP：

- 先复用这里的稳定数据结构
- 不新增“任意执行代码”接口
- preview 和 apply 仍应是分开的结构化动作

当前阶段不要把这里扩写成大而全平台协议。
