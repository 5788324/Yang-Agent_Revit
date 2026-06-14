# YangAgent Framework

This folder defines the target framework shape for YangAgent as the only mainline product.

## Framework Layers

- `core`: settings, theme engine, language, logging, export paths, and shared UI/report helpers
- `features`: YangAgent-native tools and later rewritten external tools
- `adapters`: pyRevit, Revit API, C# addin, and external toolbox integration boundaries
- `governance`: task packs, review gates, rewrite rules, and external-tool intake controls
- `design-system`: theme tokens, report styling, icon rules, and naming rules

## Mainline Rule

YangAgent is the only mainline product.

External toolboxes such as Gemini are reference sources only until a tool is rewritten into a YangAgent feature.

## Rewrite Rule

No external tool is merged as a direct patch.

Every accepted external capability must be:

1. inventoried
2. classified
3. assigned a rewrite spec
4. rebuilt inside YangAgent boundaries
5. validated under YangAgent safety rules
