# Security Preparations

> Historical support note.
>
> The active security boundary is defined primarily by `docs/project-rules.md` and `docs/safety-rules.md`.

## Current Minimum Security Position

- do not test on production models
- do not commit `.rvt`, `.rfa`, secrets, or local `%APPDATA%` config
- model-changing tools must keep dry-run, confirmation, log, and Undo checks
- external AI outputs are draft until Codex review
- MCP or bridge layers must not expose arbitrary code execution

## Why This File Is No Longer Primary

This file came from an earlier preparation phase with broader company-style backup and rollout wording.

Current repo governance now covers most of that more concretely through:

- daily ops
- worklogs and startup docs
- sandbox testing rules
- apply safety gates

## Keep This File For

- quick reminders when reviewing old safety assumptions
- comparing older “preparation” language with current working rules
