# YangAgent Design System

This folder defines the shared visual system for YangAgent and any later external rewrite.

## Current Theme Presets

- `yangagent_core`
- `toolbox_warm`
- `dark_pro`

## Design System Rules

- New UI must not hardcode color values in feature code.
- New windows must read theme tokens from the shared theme engine.
- New reports should use the shared report styling helpers.
- New icons should follow YangAgent icon semantics:
  - read-only
  - model-changing
  - warning/risk
  - system/settings
- Rewritten external tools must adopt YangAgent naming and visual language.

## Priority

Revit native Ribbon chrome is not the first theming target.

Prioritize:

1. tool windows
2. report/export styling
3. icon language
4. naming tone
