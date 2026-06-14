# Preview Chinese Content

Scan the active Revit document for Chinese (CJK) characters across families, parameters, materials, text notes, views, and project info. Read-only preview.

## Scan Coverage

- Family names
- FamilySymbol names and parameter names/values
- Material names
- TextNote text content
- FamilyInstance parameter names/values (first 5000)
- Project Parameter definitions
- View names (excluding templates)
- ProjectInfo fields

## Output

- Markdown report with themed styling
- CSV with element_id, category, content_type, chinese_text, element_name

## Safety

- Read-only — no model changes
- No Transaction opened
- No elements deleted or modified
