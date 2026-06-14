## Summary

简要说明这次改了什么，以及为什么要改。

## Scope

- [ ] 文档
- [ ] pyRevit
- [ ] C# DLL
- [ ] 工具/脚本
- [ ] 治理/流程

## Validation

请写清楚你实际做过哪些验证：

- Revit 版本：
- pyRevit 版本：
- 是否只做离线验证：
- 是否在 sandbox 模型里验证：
- 运行过哪些命令：

## Safety

如果涉及模型修改，请说明：

- 是否先有 preview / dry-run
- 是否有人类确认
- 是否有日志
- 是否考虑 Undo

## Checklist

- [ ] 当前改动符合 YangAgent 当前主线，而不是旧平台化方向
- [ ] 如果是 pyRevit，兼容 IronPython 风格约束
- [ ] 如果涉及模型修改，遵守 `preview -> confirmation -> apply -> log -> Undo check`
- [ ] 没有提交生产模型、客户数据、密钥或本地配置
- [ ] 已更新必要文档或 worklog
