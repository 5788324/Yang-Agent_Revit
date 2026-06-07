using System;
using System.Reflection;
using Autodesk.Revit.UI;

namespace YangAgent.Revit2027;

public class App : IExternalApplication
{
    private const string TabName = "YangAgent";
    private const string SettingsPanelName = "Settings";
    private const string ReportsPanelName = "Reports";

    public Result OnStartup(UIControlledApplication application)
    {
        try
        {
            TryCreateTab(application, TabName);

            RibbonPanel settingsPanel = EnsurePanel(application, TabName, SettingsPanelName);
            RibbonPanel reportsPanel = EnsurePanel(application, TabName, ReportsPanelName);

            string assemblyPath = Assembly.GetExecutingAssembly().Location;

            AddButton(settingsPanel, "YangAgentAbout", "About\nUpdate", assemblyPath, typeof(Commands.AboutCommand).FullName!);
            AddButton(settingsPanel, "YangAgentSettings", "System\nSettings", assemblyPath, typeof(Commands.OpenSettingsCommand).FullName!);
            AddButton(settingsPanel, "YangAgentOpenConfig", "Config\nFolder", assemblyPath, typeof(Commands.OpenConfigFolderCommand).FullName!);
            AddButton(reportsPanel, "YangAgentReports", "Export\nReports", assemblyPath, typeof(Commands.ExportReportPlaceholderCommand).FullName!);
            AddButton(reportsPanel, "YangAgentOpenExports", "Reports\nFolder", assemblyPath, typeof(Commands.OpenExportFolderCommand).FullName!);

            return Result.Succeeded;
        }
        catch (Exception ex)
        {
            TaskDialog.Show("YangAgent", "YA-CS-STARTUP-001: YangAgent startup failed.\n\n" + ex.Message);
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
            ToolTip = "YangAgent Revit 2027 DLL skeleton. Current commands do not modify the Revit model."
        };

        panel.AddItem(data);
    }
}
