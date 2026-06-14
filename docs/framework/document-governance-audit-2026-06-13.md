# Document Governance Audit - 2026-06-13

This file records the second-round documentation governance pass for the active repository.

Repository:

```text
G:\Codex\YangAgent Revit\YangAgent Revit
```

## Purpose

The repository now has enough docs that speed is starting to fall.

The goal of this audit is:

- define which docs are authoritative;
- define which docs are operational support only;
- define which docs are historical reference only;
- define which docs are cleanup candidates;
- avoid deleting still-useful context by accident.

## Current Rule

Do not delete a retained project doc until it has been read at least once and classified.

This pass completed that first classification step.

## Tier A - Current Authority

Use these first when documents conflict:

1. `README.md`
2. `docs/product-brief.md`
3. `docs/project-rules.md`
4. `docs/framework/daily-ops-routine.md`
5. `docs/handoff-new-chat-2026-06-07.md`
6. `docs/next-steps.md`
7. current relevant `docs/worklogs/worklog-YYYY-MM-DD.md`

These docs define the active product direction, workflow, and daily handoff behavior.

## Tier B - Active Operational Support

Keep current and readable. These support implementation, review, validation, or collaboration:

- `docs/agent-development-rules.md`
- `docs/agent-operating-model.md`
- `docs/agent-task-template.md`
- `docs/agent-delivery-report-template.md`
- `docs/agent-review-checklist.md`
- `docs/daily-agent-log-template.md`
- `docs/sandbox-pyrevit-mvp-runbook.md`
- `docs/sandbox-pyrevit-mvp-checklist.md`
- `docs/sandbox-pyrevit-mvp-feedback-template.md`
- `docs/sandbox-snowdon-live-pack-2026-06-13.md`
- `docs/external-toolbox-intake.md`
- `docs/reviews/gemini-toolbox-initial-inventory-2026-06-13.md`
- everything under `docs/design-system/`
- everything under `docs/governance/`

## Tier C - Historical Reference, Keep But Downgrade

These still contain useful history, but they should not drive current implementation without confirmation from Tier A or Tier B docs:

- `docs/architecture-design.md`
- `docs/dll-addin-development-plan.md`
- `docs/claude-doc-integration-review.md`
- `docs/colleague-quickstart.md`
- `docs/revit-ai-agent-project-plan.md`
- `docs/agent-development-roadmap.md`
- `docs/handoff-2026-05-23.md`
- `docs/handoff-new-chat-2026-05-23.md`
- older worklogs before the current sprint

Action:

- retain for now;
- add or preserve clear historical-reference labeling;
- do not cite them as active authority in new task packs.

## Tier D - Working Drafts And Generated Reports

These are useful, but should not be mistaken for project rules:

- everything under `docs/drafts/`
- generated validation outputs such as:
  - `docs/drafts/sandbox-preflight-report.md`
  - `docs/drafts/static-check-report.md`

Action:

- keep while they support active review or preflight evidence;
- prune stale drafts after the information has been promoted elsewhere;
- do not link them as core project guidance from authority docs.

## Tier E - Cleanup Candidates

These need a follow-up pass, not immediate deletion:

### Candidate group 1: superseded Hermes coordination docs

- `docs/hermes-agent-brief.md`
- `docs/hermes-capability-assessment.md`
- `docs/hermes-deepseek-prompt.md`
- `docs/hermes-next-tasks.md`

Reason:

- they reflect an older Hermes role that was docs-only or read-only;
- the current repository already has stronger governance under:
  - `docs/agent-*.md`
  - `docs/governance/*.md`
  - `docs/governance/hermes-deepseek-implementation-pack-2026-06-13.md`

Recommended next action:

- either rewrite these into aligned short forms;
- or archive/delete them after extracting any still-useful wording.

### Candidate group 2: older handoff packs with outdated path/version assumptions

- `docs/handoff-2026-05-23.md`
- `docs/handoff-new-chat-2026-05-23.md`

Reason:

- they still refer to earlier path and workflow assumptions;
- they are useful as historical evidence, not as startup docs.

Recommended next action:

- keep as historical only;
- do not use for new chat startup.
- downgraded in this pass to explicit historical-reference stubs.

### Candidate group 3: docs with encoding or display-readability problems

Observed in terminal review:

- several older Chinese-heavy docs display as garbled text in the current shell session;
- this may be true file-encoding damage, display decoding mismatch, or mixed historical saves.

High-impact candidates to normalize first:

- `docs/safety-rules.md`
- `docs/developer-guide.md`
- `docs/testing-and-qa.md`
- `docs/user-guide.md`
- `docs/view-naming-rules.md`
- `docs/troubleshooting.md`
- `docs/error-codes.md`
- `docs/sandbox-snowdon-live-pack-2026-06-13.md`
- `docs/sandbox-pyrevit-mvp-runbook.md`
- `docs/sandbox-pyrevit-mvp-checklist.md`
- `docs/handoff-new-chat-2026-06-07.md`
- several older handoff/worklog/history docs

Recommended next action:

- rewrite or normalize the most user-facing/high-authority files first;
- do not spend time repairing low-value historical drafts before active docs.

Completed in this pass:

- `docs/safety-rules.md`
- `docs/developer-guide.md`
- `docs/testing-and-qa.md`
- `docs/user-guide.md`
- `docs/view-naming-rules.md`
- `docs/troubleshooting.md`
- `docs/error-codes.md`
- `docs/sandbox-snowdon-live-pack-2026-06-13.md`
- `docs/sandbox-pyrevit-mvp-runbook.md`
- `docs/sandbox-pyrevit-mvp-checklist.md`
- `docs/handoff-new-chat-2026-06-07.md`
- `CHANGELOG.md`
- `pyrevit/YangAgent.extension/README.md`
- `tests/README.md`
- `prompts/task-templates/code-review.md`
- `prompts/task-templates/pyrevit-tool.md`
- `.github/PULL_REQUEST_TEMPLATE.md`
- `.github/ISSUE_TEMPLATE/bug_report.md`
- `.github/ISSUE_TEMPLATE/feature_request.md`
- `pyrevit/YangAgent.extension/lib/yang_agent_lang.py`
- `pyrevit/YangAgent.extension/YangAgent.tab/Reports.panel/Reports.pulldown/ModelHealthReport.pushbutton/script.py`
- `tools/codex_patch/README.md`
- `pyrevit/YangAgent.extension/YangAgent.tab/Reports.panel/Reports.pulldown/ReportExportPath.pushbutton/script.py`
- `pyrevit/YangAgent.extension/YangAgent.tab/Reports.panel/Reports.pulldown/ExportAIReviewPrompt.pushbutton/script.py`
- `pyrevit/YangAgent.extension/YangAgent.tab/Reports.panel/Reports.pulldown/ApplyMissingDoorWindowMarks.pushbutton/script.py`
- `pyrevit/YangAgent.extension/YangAgent.tab/Reports.panel/Reports.pulldown/ApplyMissingRoomNumbers.pushbutton/script.py`
- `pyrevit/YangAgent.extension/YangAgent.tab/Settings.panel/SystemSettings.pushbutton/ui.xaml`
- `pyrevit/YangAgent.extension/YangAgent.tab/Reports.panel/Reports.pulldown/PreviewDuplicateRoomNumbers.pushbutton/script.py`
- `pyrevit/YangAgent.extension/YangAgent.tab/Reports.panel/Reports.pulldown/PreviewMissingRoomNumbers.pushbutton/script.py`
- `pyrevit/YangAgent.extension/YangAgent.tab/Reports.panel/Reports.pulldown/PreviewMissingDoorWindowMarks.pushbutton/script.py`
- `pyrevit/YangAgent.extension/YangAgent.tab/Reports.panel/Reports.pulldown/PreviewUnplacedViews.pushbutton/script.py`
- `pyrevit/YangAgent.extension/YangAgent.tab/Reports.panel/Reports.pulldown/PreviewViewNamingRules.pushbutton/script.py`
- `pyrevit/YangAgent.extension/YangAgent.tab/Reports.panel/Reports.pulldown/ExportRegressionChecklist.pushbutton/script.py`
- `pyrevit/YangAgent.extension/YangAgent.tab/Reports.panel/Reports.pulldown/ExportModelSnapshot.pushbutton/script.py`
- `pyrevit/YangAgent.extension/YangAgent.tab/Reports.panel/Reports.pulldown/ProjectInfoReport.pushbutton/README.md`
- report pulldown root `bundle.yaml`
- multiple report button `bundle.yaml` files for preview/apply/export surfaces

These were rewritten into current clean versions aligned with the active repository direction.

## Immediate Cleanup Already Completed

Confirmed safe cleanup in this pass:

- removed workspace `tmp/`
- removed `tools/__pycache__/`
- removed stray `.pyc` cache output under the pyRevit button tree
- deleted stale Hermes draft-only documents under `docs/drafts/`

These were temporary/cache artifacts, not project source.

## Repository Skeleton Confirmed In This Pass

The active repository structure is now clear enough for future handoff without re-mining older docs:

- `pyrevit/YangAgent.extension/`
  - mainline implementation surface
  - shared libs under `lib/`
  - UI entrypoints under `YangAgent.tab/Settings.panel` and `Reports.panel`
- `src/YangAgent.Revit2027/`
  - lightweight C# DLL track only
- `scripts/`
  - pyRevit install/refresh
  - cache clear
  - generic and 2027-specific DLL build/install wrappers
- `tools/`
  - offline syntax check
  - pyRevit extension checker
  - sandbox preflight
  - static checks
  - apply CSV validation
- `tests/fixtures/`
  - valid/duplicate CSV fixtures for room and mark apply validation
- `mcp/revit-context/`
  - placeholder only, not active delivery
- `samples/`
  - placeholder for future concepts/examples, currently not mainline
- `standards/`
  - lightweight placeholder standards, not full BIM standard library yet
- `prompts/`
  - prompt templates and system guidance, now normalized to current rules
- `.github/`
  - issue and PR templates normalized to current sandbox/personal-use workflow
- `tools/codex_patch/`
  - explicitly marked as local Codex Desktop patch helper, not YangAgent mainline product code

## Drafts State After Cleanup

`docs/drafts/` is now reduced to:

- `README.md`
- `sandbox-preflight-report.md`
- `static-check-report.md`

This is the intended state for now: one draft rules file plus generated evidence outputs.

Historical note:

- older worklogs may still mention deleted Hermes draft filenames as part of true historical record;
- these references do not mean the deleted draft docs should be restored.

Code-quality note:

- the governance pass uncovered a real implementation-layer issue, not just documentation debt:
  - `pyrevit/YangAgent.extension/lib/yang_agent_lang.py` contained garbled Chinese defaults and labels
  - this file was rewritten into a clean current version
  - `ModelHealthReport.pushbutton/script.py` also contained garbled Chinese UI/report text and was rewritten
  - the same cleanup pattern was then applied to `ReportExportPath`, `ExportAIReviewPrompt`, `ApplyMissingDoorWindowMarks`, `ApplyMissingRoomNumbers`, and the `SystemSettings` XAML surface
  - the same cleanup pattern was then extended to the remaining high-traffic report/preview scripts and their `bundle.yaml` button metadata
  - future cleanup should continue checking shared libs and active button scripts, not only docs

## Next Governance Actions

1. Normalize active Chinese-facing docs that currently display garbled in terminal output.
2. Rewrite or retire the old Hermes-specific coordination docs so there is one current rule set.
3. Add explicit `historical reference only` labeling to any retained old handoff/planning doc that still lacks it.
4. Prune stale drafts once their useful content has been promoted into authority or support docs.
5. Keep daily handoff docs current so future chats do not need to mine old handoffs.
6. Continue reviewing any remaining active support docs or active UI/resource files one by one until all high-frequency surfaces have current wording and readable encoding.
7. After document cleanup, shift attention back to code review, live validation, and bounded external-agent deliveries instead of creating more parallel planning docs.
