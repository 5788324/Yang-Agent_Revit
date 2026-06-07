using Autodesk.Revit.Attributes;
using Autodesk.Revit.DB;
using Autodesk.Revit.UI;

namespace YangAgent.Revit2027.Commands;

[Transaction(TransactionMode.Manual)]
public class ExportReportPlaceholderCommand : IExternalCommand
{
    public Result Execute(ExternalCommandData commandData, ref string message, ElementSet elements)
    {
        TaskDialog.Show(
            "YangAgent Export Reports",
            "This is a placeholder for future DLL report export commands.\n\n" +
            "Recommended migration order:\n" +
            "1. Model health report\n" +
            "2. Model snapshot export\n" +
            "3. Door/window mark dry-run preview\n\n" +
            "For now, report generation remains in the pyRevit toolbox.");

        return Result.Succeeded;
    }
}
