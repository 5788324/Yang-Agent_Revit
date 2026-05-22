using Autodesk.Revit.Attributes;
using Autodesk.Revit.DB;
using Autodesk.Revit.UI;

namespace YangAgent.Revit2027.Commands;

[Transaction(TransactionMode.Manual)]
public class OpenSettingsCommand : IExternalCommand
{
    public Result Execute(ExternalCommandData commandData, ref string message, ElementSet elements)
    {
        Autodesk.Revit.UI.TaskDialog.Show(
            "YangAgent 系统设置",
            "这里将承载正式 DLL 插件的系统设置。\n\n" +
            "计划功能：\n" +
            "1. 语言：中文 / English\n" +
            "2. 用户简称和头像\n" +
            "3. Light / Dark Theme\n" +
            "4. 报告导出路径\n\n" +
            "当前设置仍由 pyRevit 工具箱负责。");

        return Result.Succeeded;
    }
}
