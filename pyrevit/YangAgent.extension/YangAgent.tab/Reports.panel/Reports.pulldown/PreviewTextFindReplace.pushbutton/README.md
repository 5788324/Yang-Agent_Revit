# 预览文本查找替换

查找并预览 `TextNote` 中的文本替换候选结果。该按钮只做 `dry-run`，不会修改模型。

## 输入

- 查找文本：要搜索的文本内容
- 替换文本：替换后的文本内容，可留空
- 区分大小写：选择是否精确区分大小写

## 输出

- Markdown 报告：替换候选汇总和下一步建议
- CSV 文件：`text_find_replace_candidates_*.csv`

## 安全边界

- 只读 `dry-run`，不修改任何 `TextNote` 元素
- 不开启 `Transaction`
- 生成的 CSV 只用于人工审查和后续 apply 工具输入
