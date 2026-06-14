# YangAgent Theme Engine

## Purpose

The YangAgent theme engine is the only supported theme source for YangAgent UI.

It exists to:

- replace ad-hoc `light/dark` logic
- support multiple branded presets
- let future rewritten Gemini tools plug into the same visual system

## Stable Interface

Each theme must provide:

- `theme_id`
- bilingual display label
- window background
- panel background
- section background
- primary text
- secondary text
- border
- accent
- accent soft
- success
- warning
- danger
- input background
- primary button background/text
- secondary button background/text
- report accent
- report surface

## Compatibility

Legacy settings are mapped as:

- `light` -> `yangagent_core`
- `dark` -> `dark_pro`

Unknown values fall back to `yangagent_core`.

## Current Implementation Rule

- feature code may ask for a theme definition
- feature code may not define independent color systems
- user-defined arbitrary palette editing is out of scope for now
