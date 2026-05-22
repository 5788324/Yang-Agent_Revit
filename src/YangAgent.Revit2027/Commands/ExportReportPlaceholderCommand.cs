using Autodesk.Revit.Attributes;
using Autodesk.Revit.DB;
using Autodesk.Revit.UI;

namespace YangAgent.Revit2027.Commands;

[Transaction(TransactionMode.Manual)]
public class ExportReportPlaceholderCommand : IExternalCommand
{
    public Result Execute(ExternalCommandData commandData, ref string message, ElementSet elements)
    {
        Autodesk.Revit.UI.TaskDialog.Show(
            "YangAgent 导出报告",
            "这里将承载正式 DLL 插件的报告导出功能。\n\n" +
            "迁移顺序建议：\n" +
            "1. 模型健康报告\n" +
            "2. 模型快照导出\n" +
            "3. 门窗缺失标记 dry-run\n\n" +
            "当前报告功能仍由 pyRevit 工具箱负责。");

        return Result.Succeeded;
    }
}
