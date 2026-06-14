# -*- coding: utf-8 -*-
"""System Settings for YangAgent."""

from __future__ import print_function

import os
import clr

clr.AddReference("PresentationFramework")
clr.AddReference("PresentationCore")
clr.AddReference("WindowsBase")
import System.Windows.Media as Media

from pyrevit import forms, script
from yang_agent_lang import (
    get_language,
    save_language,
    get_user_profile,
    save_user_profile,
    get_agent_preferences,
    save_agent_preferences,
    ensure_company_standards_template,
    get_company_standards_path,
    save_company_standards_path,
    get_view_naming_rules,
    save_view_naming_rules,
)
from yang_agent_theme import (
    get_theme_id,
    save_theme_id,
    get_theme_labels,
    get_theme_definition,
    hex_to_brush,
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

LABEL_NAMES = [
    "LangLabel",
    "ThemeLabel",
    "NickLabel",
    "AvatarLabel",
    "PreferencesLabel",
    "PreferencesHelp",
    "RevitVersionsLabel",
    "WorkflowLabel",
    "ReviewFocusLabel",
    "SafetyNotesLabel",
    "StandardsLabel",
    "StandardsHelp",
    "ViewRulesLabel",
    "ViewRulesHelp",
    "FloorPlanLabel",
    "CeilingPlanLabel",
    "SectionLabel",
    "ElevationLabel",
    "ThreeDLabel",
    "DraftingViewLabel",
    "LegendLabel",
    "AreaPlanLabel",
    "EngineeringPlanLabel",
    "KeywordsLabel",
    "AboutText",
]

SECTION_NAMES = [
    "IdentitySection",
    "PreferencesSection",
    "StandardsSection",
    "ViewRulesSection",
    "AboutSection",
]

INPUT_NAMES = [
    "NicknameBox",
    "AvatarBox",
    "RevitVersionsBox",
    "WorkflowBox",
    "ReviewFocusBox",
    "SafetyNotesBox",
    "StandardsPathBox",
    "FloorPlanPrefixesBox",
    "CeilingPlanPrefixesBox",
    "SectionPrefixesBox",
    "ElevationPrefixesBox",
    "ThreeDPrefixesBox",
    "DraftingViewPrefixesBox",
    "LegendPrefixesBox",
    "AreaPlanPrefixesBox",
    "EngineeringPlanPrefixesBox",
    "TemporaryKeywordsBox",
]

BUTTON_NAMES = [
    "SaveBtn",
    "BrowseAvatarBtn",
    "BrowseStandardsBtn",
    "CreateStandardsBtn",
]


class SettingsWindow(forms.WPFWindow):
    def __init__(self, xaml_file_name):
        forms.WPFWindow.__init__(self, xaml_file_name)

        self.lang = get_language()
        self.theme_id = get_theme_id()
        self.theme_options = get_theme_labels(self.lang)

        profile = get_user_profile()

        self.ThemeCombo.Items.Clear()
        for theme_id, label in self.theme_options:
            self.ThemeCombo.Items.Add(label)

        self.LanguageCombo.SelectedIndex = 1 if self.lang == "en" else 0
        self._set_theme_combo_selection()

        self.NicknameBox.Text = profile.get("nickname") or ""
        self.AvatarBox.Text = profile.get("avatar_path") or ""
        self.load_agent_preferences()
        self.StandardsPathBox.Text = get_company_standards_path()
        self.load_view_naming_rules()
        self.apply_theme()

    def _set_theme_combo_selection(self):
        for index, option in enumerate(self.theme_options):
            if option[0] == self.theme_id:
                self.ThemeCombo.SelectedIndex = index
                return
        self.ThemeCombo.SelectedIndex = 0

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
            getattr(self, box_name).Text = self.join_values(prefix_rules.get(view_type, []))
        self.TemporaryKeywordsBox.Text = self.join_values(rules.get("temporary_keywords", []))

    def load_agent_preferences(self):
        preferences = get_agent_preferences()
        self.RevitVersionsBox.Text = preferences.get("revit_versions", "")
        self.WorkflowBox.Text = preferences.get("preferred_workflow", "")
        self.ReviewFocusBox.Text = preferences.get("review_focus", "")
        self.SafetyNotesBox.Text = preferences.get("safety_notes", "")

    def theme_changed(self, sender, args):
        if self.ThemeCombo.SelectedIndex == -1:
            return
        self.theme_id = self.theme_options[self.ThemeCombo.SelectedIndex][0]
        self.apply_theme()

    def _apply_foregrounds(self, color):
        for name in LABEL_NAMES:
            getattr(self, name).Foreground = color

    def _apply_section_styles(self, tokens):
        panel_bg = hex_to_brush(Media, tokens["panel_bg"])
        border = hex_to_brush(Media, tokens["border"])
        for name in SECTION_NAMES:
            section = getattr(self, name)
            section.Background = panel_bg
            section.BorderBrush = border

    def _apply_input_styles(self, tokens):
        background = hex_to_brush(Media, tokens["input_bg"])
        foreground = hex_to_brush(Media, tokens["text_primary"])
        border = hex_to_brush(Media, tokens["border"])
        for name in INPUT_NAMES:
            control = getattr(self, name)
            control.Background = background
            control.Foreground = foreground
            control.BorderBrush = border
        self.LanguageCombo.Background = background
        self.LanguageCombo.Foreground = foreground
        self.LanguageCombo.BorderBrush = border
        self.ThemeCombo.Background = background
        self.ThemeCombo.Foreground = foreground
        self.ThemeCombo.BorderBrush = border

    def _apply_button_styles(self, tokens):
        primary_bg = hex_to_brush(Media, tokens["button_bg"])
        primary_fg = hex_to_brush(Media, tokens["button_text"])
        secondary_bg = hex_to_brush(Media, tokens["button_alt_bg"])
        secondary_fg = hex_to_brush(Media, tokens["button_alt_text"])
        border = hex_to_brush(Media, tokens["border"])

        self.SaveBtn.Background = primary_bg
        self.SaveBtn.Foreground = primary_fg
        self.SaveBtn.BorderBrush = primary_bg

        for name in ["BrowseAvatarBtn", "BrowseStandardsBtn", "CreateStandardsBtn"]:
            control = getattr(self, name)
            control.Background = secondary_bg
            control.Foreground = secondary_fg
            control.BorderBrush = border

    def apply_theme(self):
        theme = get_theme_definition(self.theme_id)
        tokens = theme["tokens"]
        self.Background = hex_to_brush(Media, tokens["window_bg"])
        self._apply_foregrounds(hex_to_brush(Media, tokens["text_primary"]))
        self._apply_section_styles(tokens)
        self._apply_input_styles(tokens)
        self._apply_button_styles(tokens)

    def browse_avatar_click(self, sender, args):
        picked = forms.pick_file(
            files_filter="Image Files (*.png;*.jpg;*.jpeg)|*.png;*.jpg;*.jpeg|All Files (*.*)|*.*",
            title="Select avatar / 选择头像",
        )
        if picked:
            self.AvatarBox.Text = picked

    def browse_standards_click(self, sender, args):
        picked = forms.pick_file(
            files_filter="Markdown Files (*.md)|*.md|Text Files (*.txt)|*.txt|All Files (*.*)|*.*",
            title="Select company standards / 选择公司标准文件",
        )
        if picked:
            self.StandardsPathBox.Text = picked

    def create_standards_click(self, sender, args):
        path = ensure_company_standards_template(self.StandardsPathBox.Text)
        self.StandardsPathBox.Text = path
        forms.toast("Company standards template created / 公司标准模板已创建", title="Yang Agent")

    def save_click(self, sender, args):
        new_lang = "zh" if self.LanguageCombo.SelectedIndex == 0 else "en"
        save_language(new_lang)
        save_theme_id(self.theme_id)
        save_user_profile(nickname=self.NicknameBox.Text, avatar_path=self.AvatarBox.Text)
        save_agent_preferences(
            revit_versions=self.RevitVersionsBox.Text,
            preferred_workflow=self.WorkflowBox.Text,
            review_focus=self.ReviewFocusBox.Text,
            safety_notes=self.SafetyNotesBox.Text,
        )
        save_company_standards_path(self.StandardsPathBox.Text)

        prefix_rules = {}
        for view_type, box_name in VIEW_TYPE_BOXES:
            prefix_rules[view_type] = self.split_values(getattr(self, box_name).Text)
        save_view_naming_rules(
            prefix_by_view_type=prefix_rules,
            temporary_keywords=self.split_values(self.TemporaryKeywordsBox.Text),
        )

        forms.toast("Settings saved / 设置已保存", title="Yang Agent")
        self.Close()


def main():
    script_dir = os.path.dirname(__file__)
    xaml_file = os.path.join(script_dir, "ui.xaml")
    SettingsWindow(xaml_file).show_dialog()


if __name__ == "__main__":
    main()
