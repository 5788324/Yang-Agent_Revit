# Changelog

This file records meaningful project changes that still matter to the current repository state.

The project is still in an early MVP phase, so this changelog is intentionally concise.

## [Unreleased]

### Added

- shared theme engine modules:
  - `pyrevit/YangAgent.extension/lib/yang_agent_settings.py`
  - `pyrevit/YangAgent.extension/lib/yang_agent_theme.py`
  - `pyrevit/YangAgent.extension/lib/yang_agent_report_style.py`
- `Project Info Report` pyRevit button
- governance framework under:
  - `docs/framework/`
  - `docs/design-system/`
  - `docs/governance/`
- daily ops and document-governance rules
- offline syntax-check helper:
  - `tools/check_offline_python_syntax.py`

### Changed

- current repo direction is now explicitly a personal Revit AI assistant, not a company platform
- document authority order has been simplified and tightened
- many older planning and architecture docs were downgraded to historical-reference stubs
- `docs/drafts/` was pruned to keep only current generated evidence plus its README
- sandbox testing, troubleshooting, error-code, and handoff docs were rewritten into current readable versions
- top-level and auxiliary READMEs/templates were normalized to current project rules
- `pyrevit/YangAgent.extension/lib/yang_agent_lang.py` was cleaned up to remove garbled Chinese text in shared language defaults

### Fixed

- offline preflight now avoids unreliable `py_compile` cache writes by using source-only syntax checking
- stale Hermes draft clutter was removed after its useful content was promoted into current docs
- shared language helper text no longer contains garbled Chinese defaults

## Historical Note

Older milestone-style entries from the repository bootstrap phase were intentionally removed from this file once they stopped being reliable day-to-day guidance.

Historical progress is still preserved in:

- `docs/worklogs/`
- current handoff/startup docs
- Git history
