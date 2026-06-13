# Gemini Toolbox Initial Inventory - 2026-06-13

## Source

Local source path:

```text
G:\Codex\YangAgent Revit\YangAgent Revit\Gemini 资料\YangTools_SourceCode
```

Repository status:

- The source is treated as a local external toolbox.
- It is excluded from Git through `.git/info/exclude`.
- It must not be merged directly into YangAgent Revit.

## High-Level Verdict

Decision: `needs changes`

Recommended strategy:

- Do not continue developing this toolbox as the YangAgent mainline.
- Do not copy the whole C# project into the main project.
- Use it as a feature idea library.
- Select useful daily-work tools and rewrite them in YangAgent style.

Reason:

- The toolbox mixes many unrelated tools, MCP, dynamic Python execution, WPF UI, model transactions, batch operations, and auto deployment.
- This is too risky for the current personal pyRevit MVP.
- Several useful workflows are worth keeping, but the safety shell must be rebuilt.

## Project Structure Found

- Solution: `YangTools.Revit.sln`
- Main project: `src\YangTools.Revit\YangTools.Revit.csproj`
- Revit addin manifest: `src\YangTools.Revit\YangTools.Revit.addin`
- Main startup: `src\YangTools.Revit\App.cs`
- Command folder: `src\YangTools.Revit\Commands\`
- UI folder: `src\YangTools.Revit\UI\`
- Core folder: `src\YangTools.Revit\Core\`
- MCP folder: `src\YangTools.Revit\Mcp\`

## Version / Build Notes

The project declares configurations for Revit 2021-2027:

- 2021-2024: `net48`
- 2025-2026: `net8.0-windows`
- 2027: `net10.0-windows`

Important risk:

- The project has an AfterBuild target that copies files into the per-version `%AppData%\Autodesk\Revit\Addins` folder.
- Do not run a normal build until auto deployment is disabled or the output is redirected.

## Major Risk Findings

| Risk | Evidence | Decision |
| --- | --- | --- |
| Auto-start MCP server | `App.cs` creates `McpHttpServer` and starts it on Revit startup | Do not reuse directly |
| Dynamic Python execution | `IronPython` reference and `CopilotPanel` extracts/executes Python code | Reject for current mainline |
| Broad model-changing surface | Many commands and WPF windows use `Transaction`, `TransactionGroup`, `doc.Delete`, `LoadFamily`, `SaveAs` | Rewrite only selected tools |
| Auto deploy to live Revit Addins | `CopyToRevitAddins` target in `.csproj` | Disable before any build |
| Too many tools at once | 25+ `IExternalCommand` classes | Inventory first, no bulk migration |

## Initial Tool Classification

| Tool / Area | Likely purpose | Risk | Class | Recommendation |
| --- | --- | --- | --- | --- |
| `ProjectInfoCommand` | Project/file statistics | Read-only or low-risk | A | Good early reference |
| `ChineseCheckCommand` | Check Chinese text/names | Mixed; includes delete actions in UI | B/C | Keep check idea; remove or gate delete behavior |
| `SheetManagerCommand` | Sheet/revision management | Model-changing | B | Useful, but rewrite with preview/confirm/apply |
| `LevelModifierCommand` | Modify element levels | Model-changing | B/C | Useful for work, but requires strict preview and sandbox validation |
| `TextModifierCommand` | Find/replace/format text | Model-changing | B | Candidate after dry-run CSV/report design |
| `MergeTextCommand` | Merge selected text | Model-changing | B | Candidate small tool if user needs it |
| `AlignTextToLineCommand` | Align text to virtual line | Model-changing | B | Candidate small tool; needs selection preview |
| `AlignTextToTextCommand` | Align text to target text | Model-changing | B | Candidate small tool; needs selection preview |
| `DistributeTextCommand` | Distribute text spacing | Model-changing | B | Candidate small tool; needs preview count |
| `DimTextOverrideCommand` | Override dimension text | Model-changing | B/C | Useful but risky; require explicit warning |
| `ViewGraphicCleanerCommand` | Clear by-element graphic overrides | Model-changing | B | Candidate if scoped to active view and preview list |
| `VisibilityCopierCommand` | Copy view visibility/overrides | Model-changing | B/C | Useful but needs strong target-view confirmation |
| `PasteCadCommand` | Paste/import CAD data | External data/model change | C | Defer |
| `BatchTaskCommand` | Batch link/export via JSON | Batch model/file operations | C | Defer |
| `ProjectAssetManagerCommand` | Manage project assets, delete/rename/import | High-risk model changes | C | Defer; mine ideas only |
| `FamilyManagerCommand` | Rename/delete/load/save families/types | High-risk family/model operations | C | Defer |
| `FamilyInstanceManagerCommand` | Manage family instances | Model-changing | C | Defer |
| `FaceBasedConverterCommand` | Convert face-based family instances | High-risk model transformation | C | Defer |
| `BooleanGeometryCommand` | Boolean geometry / family work | High-risk geometry/family operations | C | Defer |
| `EntityGeneratorCommand` | Generate loft/entity geometry | High-risk model/family generation | C | Defer |
| `LinearPlacementCommand` | Place family instances along line | Model generation | C | Defer until placement safety pattern exists |
| `SectionByLineCommand` | Create section by line | Model/view creation | B/C | Defer; possible future candidate |
| `MicroToolCommand` | Run project micro tools | Unknown dynamic tool runner | C/X | Reject unless fully specified |
| `CopilotCommand` / `CopilotPanel` | AI assistant panel with Python execution | Dynamic model execution | X | Reject for current mainline |
| `McpStatusCommand` / `McpHttpServer` | MCP server/status | Background automation | X for now | Do not reuse until MCP safety design exists |
| `HelloWorldCommand` / `SampleWindowCommand` | Demo/test commands | Demo only | X | Discard |
| `RibbonSettingsCommand` | Configure ribbon visibility | UI utility | D | Not needed until C# toolbox is mainline |

## Best First Candidates

If the user wants fast daily-work value, prioritize:

1. `ProjectInfoCommand` idea as a read-only report.
2. `TextModifierCommand` / text tools as small dry-run-first pyRevit tools.
3. `SheetManagerCommand` only after the user provides the exact sheet/titleblock workflow.
4. `LevelModifierCommand` only in sandbox and only after a preview report is designed.

## Rejected For Current Mainline

Do not migrate now:

- `CopilotPanel` dynamic Python execution.
- MCP server auto-start behavior.
- Batch task engine.
- Family manager delete/load/save operations.
- Boolean/entity generation tools.
- Any auto-deploy build behavior.

## Checks Run

From the G path repository:

```powershell
git status --short --branch
python tools\check_pyrevit_extension.py
python -m py_compile tools\static_checks.py tools\validate_apply_csv.py tools\check_pyrevit_extension.py tools\run_sandbox_preflight.py
python tools\static_checks.py --write-report
```

Results:

- Git status clean before this report.
- pyRevit extension check: `0 errors, 0 warnings`.
- Python compile: pass after running with G path write permission.
- Static checks: `0 errors, 11 warnings`.

## Next Actions

1. Ask the user which Gemini toolbox tools they actually use at work.
2. Build one small safe tool first instead of migrating the toolbox.
3. Prefer pyRevit unless the feature clearly needs C#.
4. Keep all selected tools under the project safety rule: preview / confirmation / apply / log / Undo note.
