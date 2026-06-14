# Gemini Rewrite Spec: Project Info

## Source

- source tool id: `gemini.project_info`
- source toolbox: `Gemini`
- source path: `Gemini 资料/YangTools_SourceCode/src/YangTools.Revit/Commands/ProjectInfoCommand.cs`
- original purpose: show project/file statistics and basic project information in a Revit dialog

## YangAgent Target

- target feature id: `yangagent.project_info_report`
- target feature name: `Project Info Report`
- feature family: `reports`
- yangagent core or external rewrite: `external rewrite`

## Rewrite Boundary

- business intent to keep:
  - quick read-only project summary
  - basic file/project statistics
  - human-readable output for daily work
- source implementation to discard:
  - Gemini-owned WPF window structure
  - Gemini naming/grouping
  - any direct dependency on Gemini ribbon/UI conventions
- UI to rebuild:
  - rebuild as YangAgent report-first flow
  - prefer exportable Markdown/CSV summary over modal-only window
- terminology to rename:
  - `文件统计` -> `Project Info Report`
  - any Gemini toolbox wording -> YangAgent report language

## Theme and UI Requirements

- required theme preset support:
  - `yangagent_core`
  - `toolbox_warm`
  - `dark_pro`
- required shared tokens:
  - window/panel background
  - primary and secondary text
  - border
  - accent
  - report accent and report surface
- report styling requirement:
  - use shared themed intro/status block helpers
  - keep report readable in plain Markdown even if HTML blocks are ignored
- icon or naming requirement:
  - use YangAgent report naming
  - icon should read as read-only project/report info, not Gemini toolbox utility

## Safety Requirements

- read-only or model-changing: `read-only`
- preview requirement: not required
- confirmation requirement: not required
- apply requirement: not allowed
- log requirement:
  - exported report path must be shown
  - document and Revit version must be recorded
- Undo note requirement: not applicable because no model change is allowed

## Validation Expectation

- offline checks:
  - `python tools/check_pyrevit_extension.py`
  - targeted offline syntax validation for the new feature script
  - `python tools/static_checks.py --write-report`
- live Revit expectation:
  - button opens or exports successfully in sandbox Revit
  - generated report file contains document title, path, basic statistics, and no model-change claims
- sandbox model requirement:
  - any local sandbox/test model
- blocker conditions:
  - any modal-only implementation without export path
  - any write transaction
  - any copied Gemini WPF styling as-is
