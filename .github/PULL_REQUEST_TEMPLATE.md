## PR 描述 (Description)

请简要描述此 PR 做了什么修改，解决了什么问题或添加了什么新功能。

Fixes # (如果关联了 Issue，请填 Issue 编号)

## 测试情况 (Testing)

请说明你在什么环境下测试了该功能：
- Revit 版本：[如 2027]
- pyRevit 版本：[如 4.8.14]
- 是否在真实的 `.rvt` 测试模型中进行过干运行 (dry-run) 或真实修改测试？

## 清单 (Checklist)

提交前请确认以下项：
- [ ] 代码在目标 Revit 版本中无报错 (No Traceback)
- [ ] Python 脚本兼容 IronPython 2.7 (没有 f-string，没有 type hints)
- [ ] `bundle.yaml` 没有使用 `context:` 字段
- [ ] 若涉及到模型修改，已确保包含二次确认逻辑并使用了 Revit Transaction
- [ ] UI / 提示信息符合中英双语规范
- [ ] 已在 `docs/worklogs/` 提交了今日工作日志
- [ ] 如果是重要更新，已更新 `CHANGELOG.md`
