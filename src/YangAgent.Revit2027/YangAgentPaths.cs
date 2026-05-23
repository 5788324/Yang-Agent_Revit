using System;
using System.IO;

namespace YangAgent.Revit2027;

internal static class YangAgentPaths
{
    internal static string ConfigDir
    {
        get
        {
            string root = Environment.GetFolderPath(Environment.SpecialFolder.ApplicationData);
            string path = Path.Combine(root, "YangAgent_Revit");
            Directory.CreateDirectory(path);
            return path;
        }
    }

    internal static string DefaultExportDir
    {
        get
        {
            string desktop = Environment.GetFolderPath(Environment.SpecialFolder.DesktopDirectory);
            string path = Path.Combine(desktop, "YangAgent_Revit_Exports");
            Directory.CreateDirectory(path);
            return path;
        }
    }
}
