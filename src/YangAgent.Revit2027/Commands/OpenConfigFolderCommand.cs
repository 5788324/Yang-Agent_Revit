using System.Diagnostics;
using Autodesk.Revit.Attributes;
using Autodesk.Revit.DB;
using Autodesk.Revit.UI;

namespace YangAgent.Revit2027.Commands;

[Transaction(TransactionMode.Manual)]
public class OpenConfigFolderCommand : IExternalCommand
{
    public Result Execute(ExternalCommandData commandData, ref string message, ElementSet elements)
    {
        Process.Start(new ProcessStartInfo
        {
            FileName = YangAgentPaths.ConfigDir,
            UseShellExecute = true
        });

        return Result.Succeeded;
    }
}
