using System;
using System.Collections.Generic;
using System.IO;
using System.Text.Json;
using System.Windows.Media;

namespace YangAgent.Revit2027.DesignSystem;

internal sealed class YangAgentTheme
{
    private static readonly IReadOnlyDictionary<string, string> LegacyThemeMap = new Dictionary<string, string>(StringComparer.OrdinalIgnoreCase)
    {
        ["light"] = "yangagent_core",
        ["dark"] = "dark_pro",
        ["light theme"] = "yangagent_core",
        ["dark theme"] = "dark_pro"
    };

    private static readonly IReadOnlyDictionary<string, YangAgentTheme> Themes = new Dictionary<string, YangAgentTheme>(StringComparer.OrdinalIgnoreCase)
    {
        ["yangagent_core"] = new(
            "yangagent_core",
            "YangAgent Core",
            "#F4F7FB",
            "#FFFFFF",
            "#EAF0F8",
            "#11233A",
            "#4A6077",
            "#B9C8DB",
            "#225D9C",
            "#D9E7F7",
            "#2C7A4B",
            "#9A5C00",
            "#A63A3A",
            "#FFFFFF",
            "#225D9C",
            "#FFFFFF",
            "#E1EBF7",
            "#14304E"),
        ["toolbox_warm"] = new(
            "toolbox_warm",
            "Toolbox Warm",
            "#FAF5EE",
            "#FFFDF9",
            "#F2E8D8",
            "#33261B",
            "#6F5640",
            "#D0BEA5",
            "#9A673B",
            "#F3E6D4",
            "#5A7E45",
            "#A56A21",
            "#A1483B",
            "#FFFDF9",
            "#9A673B",
            "#FFFFFF",
            "#EADCC8",
            "#4A3624"),
        ["dark_pro"] = new(
            "dark_pro",
            "Dark Pro",
            "#1C222B",
            "#242C36",
            "#2B3541",
            "#F3F6FA",
            "#B4C2D0",
            "#465567",
            "#5AA4E8",
            "#203B54",
            "#4EBB74",
            "#E0A84B",
            "#D86A6A",
            "#202832",
            "#5AA4E8",
            "#0F1822",
            "#304050",
            "#EAF1F8")
    };

    private YangAgentTheme(
        string id,
        string displayName,
        string windowBg,
        string panelBg,
        string sectionBg,
        string textPrimary,
        string textSecondary,
        string border,
        string accent,
        string accentSoft,
        string success,
        string warning,
        string danger,
        string inputBg,
        string buttonBg,
        string buttonText,
        string buttonAltBg,
        string buttonAltText)
    {
        Id = id;
        DisplayName = displayName;
        WindowBg = windowBg;
        PanelBg = panelBg;
        SectionBg = sectionBg;
        TextPrimary = textPrimary;
        TextSecondary = textSecondary;
        Border = border;
        Accent = accent;
        AccentSoft = accentSoft;
        Success = success;
        Warning = warning;
        Danger = danger;
        InputBg = inputBg;
        ButtonBg = buttonBg;
        ButtonText = buttonText;
        ButtonAltBg = buttonAltBg;
        ButtonAltText = buttonAltText;
    }

    internal string Id { get; }
    internal string DisplayName { get; }
    internal string WindowBg { get; }
    internal string PanelBg { get; }
    internal string SectionBg { get; }
    internal string TextPrimary { get; }
    internal string TextSecondary { get; }
    internal string Border { get; }
    internal string Accent { get; }
    internal string AccentSoft { get; }
    internal string Success { get; }
    internal string Warning { get; }
    internal string Danger { get; }
    internal string InputBg { get; }
    internal string ButtonBg { get; }
    internal string ButtonText { get; }
    internal string ButtonAltBg { get; }
    internal string ButtonAltText { get; }

    internal Brush WindowBrush => ToBrush(WindowBg);
    internal Brush PanelBrush => ToBrush(PanelBg);
    internal Brush SectionBrush => ToBrush(SectionBg);
    internal Brush TextPrimaryBrush => ToBrush(TextPrimary);
    internal Brush TextSecondaryBrush => ToBrush(TextSecondary);
    internal Brush BorderBrush => ToBrush(Border);
    internal Brush AccentBrush => ToBrush(Accent);
    internal Brush ButtonBrush => ToBrush(ButtonBg);
    internal Brush ButtonTextBrush => ToBrush(ButtonText);
    internal Brush ButtonAltBrush => ToBrush(ButtonAltBg);
    internal Brush ButtonAltTextBrush => ToBrush(ButtonAltText);

    internal static YangAgentTheme Current()
    {
        return Themes[NormalizeThemeId(ReadConfiguredThemeId())];
    }

    internal static string NormalizeThemeId(string? themeId)
    {
        string key = (themeId ?? string.Empty).Trim();
        if (Themes.ContainsKey(key))
        {
            return key;
        }

        if (LegacyThemeMap.TryGetValue(key, out string? mapped))
        {
            return mapped;
        }

        return "yangagent_core";
    }

    private static string? ReadConfiguredThemeId()
    {
        string settingsPath = Path.Combine(YangAgentPaths.ConfigDir, "settings.json");
        if (!File.Exists(settingsPath))
        {
            return null;
        }

        try
        {
            using JsonDocument doc = JsonDocument.Parse(File.ReadAllText(settingsPath));
            JsonElement root = doc.RootElement;
            if (root.TryGetProperty("theme_id", out JsonElement themeId))
            {
                return themeId.GetString();
            }

            if (root.TryGetProperty("theme", out JsonElement legacyTheme))
            {
                return legacyTheme.GetString();
            }
        }
        catch
        {
            return null;
        }

        return null;
    }

    private static Brush ToBrush(string color)
    {
        return (Brush)new BrushConverter().ConvertFromString(color)!;
    }
}
