# 应用门窗标记

此工具会修改 Revit 模型。

使用前必须先运行 `预览缺失标记`，并人工检查生成的 `missing_door_window_marks_*.csv`。

安全机制：

- 只读取 dry-run CSV。
- 只接受 `missing_door_window_marks_*.csv` 文件。
- 只处理 `Door` 和 `Window` 行。
- 只写入仍为空的 `Mark/标记` 参数。
- 执行前显示影响数量并要求二次确认。
- 所有修改放在一个 Revit Transaction 中，方便撤销。
- 执行后输出 Markdown 和 CSV 日志。
- 常见错误代码见 `docs/error-codes.md`。
