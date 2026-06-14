# Delegation Pack: Gemini Project Info Rewrite

Use this if Codex assigns the first Gemini rewrite to another helper.

## Task Identity

- task name: `Rewrite Gemini ProjectInfo into YangAgent report flow`
- assigned agent: `Hermes / Gemini / DeepSeek`
- date: `2026-06-13`
- priority: `high`

## Ownership

- allowed paths:
  - `pyrevit/YangAgent.extension/**`
  - `docs/governance/**`
  - `docs/incoming/**`
- allowed file types:
  - `.py`
  - `.md`
  - `.yaml`
  - `.png`
- target feature id: `yangagent.project_info_report`
- source tool id: `gemini.project_info`
- YangAgent core or external rewrite: `external rewrite`

## Required Outcome

- exact implementation result:
  - a YangAgent read-only report tool that exports project info and basic model/file statistics
- exact docs or reports required:
  - delivery report
  - short implementation summary
- screenshots/logs required:
  - offline check output
  - live Revit screenshot only if the agent is explicitly allowed to use live Revit

## Theme and UI Rules

- required theme preset(s):
  - `yangagent_core`
  - `toolbox_warm`
  - `dark_pro`
- shared theme tokens required:
  - use shared theme and report style helpers only
- report styling requirement:
  - use YangAgent themed intro/status blocks
- naming requirement:
  - feature naming must be YangAgent report language
- forbidden UI shortcuts:
  - no copied Gemini WPF dialog
  - no hardcoded new color palette

## Safety Rules

- read-only or model-changing: `read-only`
- if model-changing, required flow:
  - not applicable
- sandbox-only or not:
  - live checks must use sandbox only

## Validation

- commands allowed:
  - `python tools/check_pyrevit_extension.py`
  - targeted offline syntax validation
  - `python tools/static_checks.py --write-report`
- manual checks allowed:
  - inspect export files
- live Revit allowed or forbidden:
  - forbidden unless Codex explicitly expands the task
- must record unrun checks:
  - yes

## Delivery

- required delivery report path:
  - `docs/incoming/YYYY-MM-DD_agent-project-info_delivery-report.md`
- required registry/spec update:
  - reference `docs/governance/rewrite-spec-gemini-project-info.md`
- questions that must be escalated back to Codex:
  - exact project metrics to keep
  - any temptation to keep Gemini dialog structure
  - any need for model-changing scope
