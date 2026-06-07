using Autodesk.Revit.Attributes;
using Autodesk.Revit.DB;
using Autodesk.Revit.UI;

namespace YangAgent.Revit2027.Commands;

[Transaction(TransactionMode.Manual)]
public class OpenSettingsCommand : IExternalCommand
{
    public Result Execute(ExternalCommandData commandData, ref string message, ElementSet elements)
    {
        TaskDialog.Show(
            "YangAgent System Settings",
            "This is a placeholder for the future DLL settings window.\n\n" +
            "Planned settings:\n" +
            "1. Language: Chinese / English\n" +
            "2. User profile and avatar path\n" +
            "3. Light / Dark theme\n" +
            "4. AI work preferences and company standards file\n" +
            "5. Report export path\n\n" +
            "For now, use the Config Folder button and the pyRevit System Settings tool.");

        return Result.Succeeded;
    }
}
