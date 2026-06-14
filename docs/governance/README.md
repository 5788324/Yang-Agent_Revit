# YangAgent Governance

This folder holds the executable governance layer for external tools and helper agents.

Use these files together:

- `tool-registry.md`
- `rewrite-spec-template.md`
- `acceptance-gate-template.md`
- `delegation-pack-template.md`

## Governance Model

- Codex is the only architecture owner and final reviewer.
- External agents may execute bounded tasks only from an approved task pack.
- External toolboxes are reviewed and rewritten into YangAgent features.
- No external feature reaches mainline without passing the acceptance gate.
