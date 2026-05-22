using Autodesk.Revit.Attributes;
using Autodesk.Revit.DB;
using Autodesk.Revit.UI;

namespace YangAgent.Revit2027.Commands;

[Transaction(TransactionMode.Manual)]
public class AboutCommand : IExternalCommand
{
    public Result Execute(ExternalCommandData commandData, ref string message, ElementSet elements)
    {
        Autodesk.Revit.UI.TaskDialog.Show(
            "YangAgent",
            "YangAgent Revit 2027\n\n" +
            "版权声明：由 Yang 开发，工具为 Codex。\n\n" +
            "更新链接：\nhttps://github.com/5788324/Yang-Agent_Revit\n\n" +
            "当前 DLL 插件为正式插件骨架，不修改模型。");

        return Result.Succeeded;
    }
}
