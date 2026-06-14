# 开发指南

这份文档面向当前主线开发。

当前目标不是大而全的平台，而是先把 `YangAgent` 做成可在 sandbox 模型里稳定工作的 pyRevit MVP。

## 1. 当前主线

当前优先级：

1. pyRevit 工具可加载
2. 只读报告可导出
3. preview 工具可稳定运行
4. apply 工具走安全链路
5. live sandbox 验证可复现

当前不优先：

- 全量 Gemini 迁移
- 大规模 C# 重构
- MCP 写模型
- 企业化部署

## 2. 当前仓库路径

唯一主开发路径：

```text
G:\Codex\YangAgent Revit\YangAgent Revit
```

不要回旧路径继续开发。

## 3. pyRevit 目录约束

pyRevit 结构示意：

```text
pyrevit/
  YangAgent.extension/
    lib/
    YangAgent.tab/
      Settings.panel/
      Reports.panel/
```

规则：

- `.panel`、`.pulldown`、`.pushbutton` 目录名用英文 ASCII
- 目录名不要带空格
- 面向用户的中英文标题放在 `bundle.yaml`
- 只在按钮目录内改自己负责的功能

## 4. pyRevit 脚本编码规则

按 IronPython 2.7 兼容风格写：

- 不用 f-string
- 不用类型注解
- 不用 walrus 运算符
- 中文文本显式处理编码
- CSV / JSON 输出保持稳定

## 5. 当前共享库

优先复用现有共享库：

- `pyrevit/YangAgent.extension/lib/yang_agent_lang.py`
- `pyrevit/YangAgent.extension/lib/yang_agent_apply.py`
- `pyrevit/YangAgent.extension/lib/yang_agent_settings.py`
- `pyrevit/YangAgent.extension/lib/yang_agent_theme.py`
- `pyrevit/YangAgent.extension/lib/yang_agent_report_style.py`

当前约束：

- 普通按钮实现可以 import 这些共享库
- 不要随手改共享 `lib`
- 如果必须扩共享库接口，先回报再改

## 6. 导出与设置规则

不要硬编码用户桌面路径。

统一走：

```python
from yang_agent_settings import get_export_dir
```

主题统一走：

```python
from yang_agent_theme import get_theme_id
```

报告样式统一走：

```python
from yang_agent_report_style import build_intro_block, build_status_block
```

## 7. 按钮类型规则

### 7.1 Report 类

- 只读
- 输出到统一导出目录
- 文件名前缀稳定
- Markdown 可中英双语或中文优先

### 7.2 Preview 类

- 只读 dry-run
- 不开事务
- 输出数量、`ElementId`、人工可判断信息
- 明确这不是直接 apply

### 7.3 Apply 类

必须遵守：

```text
preview -> confirmation -> apply -> log -> Undo note
```

并且要：

- 读 preview CSV
- 校验文件名和字段
- 校验重复 `element_id`
- 显示影响数量
- 用户确认后才写入

## 8. 当前按钮范围

当前主线按钮包括：

- `System Settings`
- `Project Info Report`
- `Report Export Path`
- `Export Model Snapshot`
- `Model Health Report`
- `Export Regression Checklist`
- `Export AI Review Prompt`
- `Preview Missing Marks`
- `Preview Missing Room Numbers`
- `Preview Duplicate Room Numbers`
- `Preview Unplaced Views`
- `Preview View Naming Rules`
- `Apply Missing Door Window Marks`
- `Apply Missing Room Numbers`

## 9. 离线检查

从仓库根目录运行：

```powershell
python tools\check_pyrevit_extension.py
python tools\run_sandbox_preflight.py --write-report
python tools\static_checks.py --write-report
```

必要时补跑：

```powershell
python tools\check_offline_python_syntax.py
```

## 10. live 验证原则

离线通过不等于 Revit 里真的可用。

只要涉及：

- 按钮注册
- pyRevit 缓存
- Revit UI
- Transaction
- Undo

就必须用 sandbox 模型 live 验证。

## 11. 文档与交接要求

每天都要维护：

- `docs/worklogs/worklog-YYYY-MM-DD.md`
- `docs/next-steps.md`
- `docs/new-chat-startup-YYYY-MM-DD.md`

开工先看：

- `README.md`
- `docs/framework/daily-ops-routine.md`
- `docs/handoff-new-chat-2026-06-07.md`
- 当天 worklog

## 12. 外部 AI 协作

Hermes / DeepSeek 可以做：

- 局部按钮草稿
- 文档整理
- 审查报告
- 低风险补丁

但必须：

- 有 task pack
- 有 delivery report
- 有 operation log
- 不碰共享架构边界

## 13. 相关文档

- `docs/product-brief.md`
- `docs/project-rules.md`
- `docs/safety-rules.md`
- `docs/testing-and-qa.md`
- `docs/agent-development-rules.md`
- `docs/framework/daily-ops-routine.md`
