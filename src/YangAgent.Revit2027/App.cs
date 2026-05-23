using System;
using System.Reflection;
using Autodesk.Revit.UI;

namespace YangAgent.Revit2027;

public class App : IExternalApplication
{
    private const string TabName = "YangAgent";

    public Result OnStartup(UIControlledApplication application)
    {
        try
        {
            TryCreateTab(application, TabName);

            RibbonPanel settingsPanel = EnsurePanel(application, TabName, "系统设置");
            RibbonPanel reportsPanel = EnsurePanel(application, TabName, "导出报告");

            string assemblyPath = Assembly.GetExecutingAssembly().Location;

            AddButton(settingsPanel, "YangAgentAbout", "关于\n更新", assemblyPath, typeof(Commands.AboutCommand).FullName!);
            AddButton(settingsPanel, "YangAgentSettings", "系统\n设置", assemblyPath, typeof(Commands.OpenSettingsCommand).FullName!);
            AddButton(settingsPanel, "YangAgentOpenConfig", "配置\n目录", assemblyPath, typeof(Commands.OpenConfigFolderCommand).FullName!);
            AddButton(reportsPanel, "YangAgentReports", "导出\n报告", assemblyPath, typeof(Commands.ExportReportPlaceholderCommand).FullName!);
            AddButton(reportsPanel, "YangAgentOpenExports", "报告\n目录", assemblyPath, typeof(Commands.OpenExportFolderCommand).FullName!);

            return Result.Succeeded;
        }
        catch (Exception ex)
        {
            Autodesk.Revit.UI.TaskDialog.Show("YangAgent", "YangAgent 启动失败：\n" + ex.Message);
            return Result.Failed;
        }
    }

    public Result OnShutdown(UIControlledApplication application)
    {
        return Result.Succeeded;
    }

    private static void TryCreateTab(UIControlledApplication application, string tabName)
    {
        try
        {
            application.CreateRibbonTab(tabName);
        }
        catch
        {
            // Tab already exists.
        }
    }

    private static RibbonPanel EnsurePanel(UIControlledApplication application, string tabName, string panelName)
    {
        foreach (RibbonPanel panel in application.GetRibbonPanels(tabName))
        {
            if (panel.Name == panelName)
            {
                return panel;
            }
        }

        return application.CreateRibbonPanel(tabName, panelName);
    }

    private static void AddButton(RibbonPanel panel, string name, string text, string assemblyPath, string className)
    {
        PushButtonData data = new(name, text, assemblyPath, className)
        {
            ToolTip = "YangAgent Revit 2027 正式插件骨架。当前为占位按钮，不修改模型。"
        };

        panel.AddItem(data);
    }
}
