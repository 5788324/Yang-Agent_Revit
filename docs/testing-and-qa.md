# 测试与质量保证

这份文档定义当前主线的验证口径。

当前原则很简单：

- 先过离线检查
- 再在 sandbox 模型里 live 验证
- 第一个 blocker 优先
- 不在一个回合里同时追很多问题

## 1. 测试环境

只用测试模型：

- `*_sandbox.rvt`
- `*_test.rvt`
- 本地可丢弃副本

不要用：

- 正式项目模型
- 中心模型
- 云上正式模型

## 2. 当前 Definition of Done

一个功能要算基本可交付，至少满足：

1. 仓库离线检查通过
2. 按钮能在 Revit 里被正常加载
3. 输出文件或 UI 结果符合预期
4. 错误信息可读
5. 如果改模型，则满足：
   `preview -> confirmation -> apply -> log -> Undo note`

## 3. 当前离线检查

从仓库根目录运行：

```powershell
python tools\check_pyrevit_extension.py
python tools\run_sandbox_preflight.py --write-report
python tools\static_checks.py --write-report
```

当前期望：

- `check_pyrevit_extension.py`：`0 errors`
- sandbox preflight：全部 `PASS`
- static checks：`0 errors`

必要时补跑：

```powershell
python tools\check_offline_python_syntax.py
```

## 4. live Revit 验证

只要行为依赖以下任一项，就必须 live 测：

- pyRevit 按钮注册
- Revit UI
- Revit 模型内容
- Transaction
- Undo
- pyRevit 缓存

## 5. 建议 live 验证顺序

按这个顺序最省时间：

1. `System Settings`
2. `Project Info Report`
3. `Export Model Snapshot`
4. `Model Health Report`
5. `Export Regression Checklist`
6. `Export AI Review Prompt`
7. 各 preview 按钮
8. 各 apply 按钮
9. 每个 apply 后立即测一次 Undo

详细执行用：

- `docs/sandbox-pyrevit-mvp-runbook.md`
- `docs/sandbox-pyrevit-mvp-checklist.md`
- `docs/sandbox-pyrevit-mvp-feedback-template.md`

## 6. apply 工具验证要求

对每个 apply 工具，至少验证：

- 只能读取对应 preview CSV
- 文件名校验有效
- 字段校验有效
- 重复 `element_id` 能拦截
- 用户确认有效
- 结果日志生成
- Undo 至少测一次

## 7. 回归测试

需要固定验证一组当前主线按钮，不要求一次性扩太多新场景。

当前最重要的是：

- 基础报告按钮不坏
- preview 链路不坏
- apply 安全壳不坏
- 中英切换不坏
- 导出路径和共享主题不破

## 8. 失败时怎么处理

只抓第一个 blocker。

记录：

- 按钮名
- Runbook 步骤号
- 精确报错
- 是否生成输出文件
- Revit 版本
- 模型名
- 是否已 reload / restart / clear cache

不要在同一轮失败里混进很多二级问题。

## 9. 外部 AI 的测试口径

Hermes / DeepSeek 可以：

- 跑离线检查
- 整理测试清单
- 写 review

但它们不能把“离线通过”写成“live 可用”。

如果没有 Revit live 证据，只能写：

- offline checked
- live not verified

## 10. 当前重点模型

当前更有内容的 sandbox 模型：

```text
G:\Codex\YangAgent Revit\YangAgent Revit\Gemini 资料\Revit 测试模型\Snowdon Towers Sample Architectural_sandbox.rvt
```

当前报告目录：

```text
G:\Codex\YangAgent Revit\YangAgent Revit\Gemini 资料\Revit 测试模型\报告
```

## 11. 相关文档

- `docs/safety-rules.md`
- `docs/developer-guide.md`
- `docs/error-codes.md`
- `docs/sandbox-pyrevit-mvp-runbook.md`
- `docs/sandbox-pyrevit-mvp-checklist.md`
- `docs/sandbox-pyrevit-mvp-feedback-template.md`
