# 更新日志 (Changelog)

所有针对本项目的重要修改都会记录在这个文件中。
为了方便版本回滚、团队对接与追溯，每次进行重要的代码或文档修改后，请务必在此记录并及时提交 Git。

日志格式参考 [Keep a Changelog](https://keepachangelog.com/zh-CN/1.0.0/)，本项目版本号遵循 [Semantic Versioning](https://semver.org/lang/zh-CN/)。

## [Unreleased]

### Added (新增)
- 新增 `docs/architecture-design.md` 系统架构设计文档。
- 新增 `docs/api-and-data-schema.md` API与数据结构规范文档。
- 新增 `docs/testing-and-qa.md` 测试与质量保证规范文档。
- 新增 `docs/security-preparations.md` 项目初期安全防范与备份预案。
- 新增 `CHANGELOG.md` 更新日志文档以规范化版本控制。
- 新增 `Preview Missing Room Numbers` dry-run 工具，导出缺少编号房间的 Markdown 和 CSV 清单。
- 新增 `Preview Duplicate Room Numbers` dry-run 工具，导出重复房间编号的 Markdown 和 CSV 清单。
- 新增 `Preview Unplaced Views` dry-run 工具，导出可能未上图视图的 Markdown 和 CSV 清单。
- 新增 `Preview Views By Naming Rules` dry-run 工具，导出视图命名问题 Markdown 和 CSV 清单。
- 新增 `docs/view-naming-rules.md`，说明视图命名规则的本地配置方式。
- 新增 `docs/handoff-2026-05-23.md` 交接记录，方便后续同事接手。
- 新增 `Apply Missing Door Window Marks` 受控修改工具，从 dry-run CSV 写入门窗标记并输出日志。

### Changed (变更)
- 完善初期项目框架与文档体系。
- 将报告工具整理到 `Reports.pulldown`。
- 将语言、用户、主题、关于更新合并为统一的 `SystemSettings` 设置窗口。
- 设置窗口补回头像路径、版权声明和插件更新链接。
- 优化门窗 `Mark/标记` 参数读写，避免 Revit 参数对象布尔误判并增加中英文参数名兜底。
- 优化 `Apply Missing Door Window Marks` 的 dry-run CSV 读取，支持 UTF-8 BOM 表头并在字段校验失败时输出实际字段。
- 修复 Revit 2027 / IronPython 中 `ElementId` 构造函数重载歧义导致应用门窗标记失败的问题。
- 优化房间编号参数读取，避免 Revit 参数对象布尔误判。
- 将视图命名检查规则抽到共享设置，支持通过本机 `settings.json` 调整。

## [1.0.0] - 2026-05-23

### Added
- 发布首个 YangAgent Revit MVP 版本。
- 新增 pyRevit 工具箱基础结构：系统设置、导出报告。
- 新增中英双语设置、用户简称、头像路径、Light/Dark Theme 配置。
- 新增报告导出路径、模型快照、模型健康报告、缺失门窗标记 dry-run 预览。
- 新增 Revit 2027 C# `.addin + .dll` 插件骨架。
- 新增用户说明、开发指南、故障排查、AI 协作流程文档。

### Fixed
- 修复 pyRevit 2027 中文目录名与 `context:` availability 导致按钮灰色的问题。
- 修复 pyRevit 旧缓存导致 FullClassName 加载错误的问题。

## [0.1.0] - 2026-05-22

### Added
- 初始化项目仓库。
- 新增核心方案文档 (`revit-ai-agent-project-plan.md`, `claude-doc-integration-review.md` 等)。
- 新增 pyRevit 工具基础框架：
  - `Export Model Snapshot`
  - `Model Health Report`
  - `Preview Missing Marks`
- 新增 Revit 2027 C# 插件骨架代码。
