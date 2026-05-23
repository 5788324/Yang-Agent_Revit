# -*- coding: utf-8 -*-
"""System Settings for Yang Agent."""

from __future__ import print_function

import os
import clr
clr.AddReference('PresentationFramework')
clr.AddReference('PresentationCore')
clr.AddReference('WindowsBase')
import System.Windows.Media as Media

from pyrevit import forms, script
from yang_agent_lang import (
    get_language, save_language, 
    get_theme, save_theme, 
    get_user_profile, save_user_profile,
    get_view_naming_rules, save_view_naming_rules
)


VIEW_TYPE_BOXES = [
    ("FloorPlan", "FloorPlanPrefixesBox"),
    ("CeilingPlan", "CeilingPlanPrefixesBox"),
    ("Section", "SectionPrefixesBox"),
    ("Elevation", "ElevationPrefixesBox"),
    ("ThreeD", "ThreeDPrefixesBox"),
    ("DraftingView", "DraftingViewPrefixesBox"),
    ("Legend", "LegendPrefixesBox"),
    ("AreaPlan", "AreaPlanPrefixesBox"),
    ("EngineeringPlan", "EngineeringPlanPrefixesBox"),
]

class SettingsWindow(forms.WPFWindow):
    def __init__(self, xaml_file_name):
        forms.WPFWindow.__init__(self, xaml_file_name)
        
        # Load initial settings
        self.lang = get_language()
        self.theme = get_theme()
        profile = get_user_profile()
        
        # Set combo boxes
        if self.lang == "en":
            self.LanguageCombo.SelectedIndex = 1
        else:
            self.LanguageCombo.SelectedIndex = 0
            
        if self.theme == "dark":
            self.ThemeCombo.SelectedIndex = 1
        else:
            self.ThemeCombo.SelectedIndex = 0
            
        self.NicknameBox.Text = profile.get("nickname") or ""
        self.AvatarBox.Text = profile.get("avatar_path") or ""
        self.load_view_naming_rules()
        
        self.apply_theme()

    def join_values(self, values):
        return ", ".join(values or [])

    def split_values(self, text):
        cleaned = []
        for part in (text or "").replace(u"|", u",").split(u","):
            value = part.strip()
            if value:
                cleaned.append(value)
        return cleaned

    def load_view_naming_rules(self):
        rules = get_view_naming_rules()
        prefix_rules = rules.get("prefix_by_view_type", {})
        for view_type, box_name in VIEW_TYPE_BOXES:
            box = getattr(self, box_name)
            box.Text = self.join_values(prefix_rules.get(view_type, []))
        self.TemporaryKeywordsBox.Text = self.join_values(rules.get("temporary_keywords", []))
        
    def theme_changed(self, sender, args):
        if hasattr(self, "ThemeCombo") and self.ThemeCombo.SelectedIndex != -1:
            if self.ThemeCombo.SelectedIndex == 1:
                self.theme = "dark"
            else:
                self.theme = "light"
            self.apply_theme()
        
    def apply_theme(self):
        if self.theme == "dark":
            bg_color = Media.SolidColorBrush(Media.Color.FromRgb(40, 40, 40))
            fg_color = Media.SolidColorBrush(Media.Color.FromRgb(240, 240, 240))
        else:
            bg_color = Media.SolidColorBrush(Media.Color.FromRgb(245, 245, 245))
            fg_color = Media.SolidColorBrush(Media.Color.FromRgb(10, 10, 10))
            
        self.Background = bg_color
        self.LangLabel.Foreground = fg_color
        self.ThemeLabel.Foreground = fg_color
        self.NickLabel.Foreground = fg_color
        self.AvatarLabel.Foreground = fg_color
        self.ViewRulesLabel.Foreground = fg_color
        self.ViewRulesHelp.Foreground = fg_color
        self.FloorPlanLabel.Foreground = fg_color
        self.CeilingPlanLabel.Foreground = fg_color
        self.SectionLabel.Foreground = fg_color
        self.ElevationLabel.Foreground = fg_color
        self.ThreeDLabel.Foreground = fg_color
        self.DraftingViewLabel.Foreground = fg_color
        self.LegendLabel.Foreground = fg_color
        self.AreaPlanLabel.Foreground = fg_color
        self.EngineeringPlanLabel.Foreground = fg_color
        self.KeywordsLabel.Foreground = fg_color
        self.AboutText.Foreground = fg_color

    def browse_avatar_click(self, sender, args):
        picked = forms.pick_file(
            files_filter="Image Files (*.png;*.jpg;*.jpeg)|*.png;*.jpg;*.jpeg|All Files (*.*)|*.*",
            title="Select avatar / 选择头像"
        )
        if picked:
            self.AvatarBox.Text = picked

    def save_click(self, sender, args):
        new_lang = "zh" if self.LanguageCombo.SelectedIndex == 0 else "en"
        save_language(new_lang)
        save_theme(self.theme)
        save_user_profile(
            nickname=self.NicknameBox.Text,
            avatar_path=self.AvatarBox.Text
        )

        prefix_rules = {}
        for view_type, box_name in VIEW_TYPE_BOXES:
            box = getattr(self, box_name)
            prefix_rules[view_type] = self.split_values(box.Text)
        save_view_naming_rules(
            prefix_by_view_type=prefix_rules,
            temporary_keywords=self.split_values(self.TemporaryKeywordsBox.Text)
        )
        
        forms.toast(
            "Settings Saved / 设置已保存", 
            title="Yang Agent"
        )
        self.Close()

def main():
    script_dir = os.path.dirname(__file__)
    xaml_file = os.path.join(script_dir, "ui.xaml")
    SettingsWindow(xaml_file).show_dialog()

if __name__ == "__main__":
    main()
