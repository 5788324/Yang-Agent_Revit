# pyRevit MVP Sandbox Feedback Template

Use this template after a real sandbox-model run.

This file exists so the first live Revit blocker comes back with enough detail for Codex to act immediately.

## One Run, One Entry

Create one filled copy of this template for each failed button or blocking step.

If multiple buttons fail, record the first blocker first.

## Template

```text
Date:

Runbook step number:

Revit version:

Model name:

Button or step name:

First failing button in sequence:

Failure type:
- gray button
- clickable but fails
- no output files
- output files wrong or incomplete
- apply completed but Undo/result unclear
- other

Exact visible error text:

Preflight report path:

Static check warning count:

Export directory path:

Was pyRevit visible before the run?
- yes / no

Was YangAgent visible before the run?
- yes / no

Was pyRevit reload already tried?
- yes / no

Was full Revit restart already tried?
- yes / no

Was `.\scripts\install-pyrevit-extension.ps1 -Force -ClearCache` already tried?
- yes / no

Any output files created?
- yes / no

If yes, list file names:

Does this blocker prevent all later steps?
- yes / no
- not sure

What happened immediately before the failure?

Screenshots or copied output text:

Anything else important:
```

## Minimum Required Fields

If time is limited, at minimum capture:

- runbook step number
- Revit version
- model name
- button name
- first failing button in sequence
- failure type
- exact visible error text
- preflight report path
- whether reload / restart / clear-cache were already tried
- whether any output files were created

## First Blocker Rule

Do not summarize several problems into one vague note.

Record the first blocking issue clearly, then stop and hand it to Codex for triage.

Always include the runbook step number so Codex can map the failure to the exact execution sequence.
