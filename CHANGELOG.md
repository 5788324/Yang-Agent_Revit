# 更新日志 (Changelog)

所有针对本项目的重要修改都会记录在这个文件中。
为了方便版本回滚、团队对接与追溯，每次进行重要的代码或文档修改后，请务必在此记录并及时提交 Git。

日志格式参考 [Keep a Changelog](https://keepachangelog.com/zh-CN/1.0.0/)，本项目版本号遵循 [Semantic Versioning](https://semver.org/lang/zh-CN/)。

## [Unreleased]

### Added (新增)
- 新增 `docs/architecture-design.md` 系统架构设计文档。
- 新增 `docs/api-and-data-schema.md` API与数据结构规范文档。
- 新增 `docs/testing-and-qa.md` 测试与质量保证规范文档。
- 新增 `CHANGELOG.md` 更新日志文档以规范化版本控制。

### Changed (变更)
- 完善初期项目框架与文档体系。

## [0.1.0] - 2026-05-22

### Added
- 初始化项目仓库。
- 新增核心方案文档 (`revit-ai-agent-project-plan.md`, `claude-doc-integration-review.md` 等)。
- 新增 pyRevit 工具基础框架：
  - `Export Model Snapshot`
  - `Model Health Report`
  - `Preview Missing Marks`
- 新增 Revit 2027 C# 插件骨架代码。
