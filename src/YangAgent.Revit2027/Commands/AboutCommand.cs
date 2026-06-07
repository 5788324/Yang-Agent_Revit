using Autodesk.Revit.Attributes;
using Autodesk.Revit.DB;
using Autodesk.Revit.UI;

namespace YangAgent.Revit2027.Commands;

[Transaction(TransactionMode.Manual)]
public class AboutCommand : IExternalCommand
{
    public Result Execute(ExternalCommandData commandData, ref string message, ElementSet elements)
    {
        TaskDialog.Show(
            "YangAgent",
            "YangAgent Revit 2027\n\n" +
            "Personal Revit assistant by Yang, developed with AI assistance.\n\n" +
            "Repository:\nhttps://github.com/5788324/Yang-Agent_Revit\n\n" +
            "Current DLL scope: ribbon skeleton, folder shortcuts, and placeholder commands only.\n" +
            "This command does not read or modify the Revit model.");

        return Result.Succeeded;
    }
}
