# -*- coding: utf-8 -*-
"""Shared theme engine for YangAgent windows and reports."""

from __future__ import print_function

from yang_agent_settings import read_settings, write_settings, safe_text


THEME_IDS = ["yangagent_core", "toolbox_warm", "dark_pro"]
LEGACY_THEME_MAP = {
    "light": "yangagent_core",
    "dark": "dark_pro",
    "light theme": "yangagent_core",
    "dark theme": "dark_pro",
    u"亮色": "yangagent_core",
    u"浅色": "yangagent_core",
    u"暗色": "dark_pro",
    u"深色": "dark_pro",
}

THEMES = {
    "yangagent_core": {
        "id": "yangagent_core",
        "labels": {
            "zh": u"YangAgent Core",
            "en": u"YangAgent Core",
        },
        "tokens": {
            "window_bg": "#F4F7FB",
            "panel_bg": "#FFFFFF",
            "section_bg": "#EAF0F8",
            "text_primary": "#11233A",
            "text_secondary": "#4A6077",
            "border": "#B9C8DB",
            "accent": "#225D9C",
            "accent_soft": "#D9E7F7",
            "success": "#2C7A4B",
            "warning": "#9A5C00",
            "danger": "#A63A3A",
            "input_bg": "#FFFFFF",
            "button_bg": "#225D9C",
            "button_text": "#FFFFFF",
            "button_alt_bg": "#E1EBF7",
            "button_alt_text": "#14304E",
            "report_accent": "#225D9C",
            "report_surface": "#EEF4FB",
        },
    },
    "toolbox_warm": {
        "id": "toolbox_warm",
        "labels": {
            "zh": u"Toolbox Warm",
            "en": u"Toolbox Warm",
        },
        "tokens": {
            "window_bg": "#FAF5EE",
            "panel_bg": "#FFFDF9",
            "section_bg": "#F2E8D8",
            "text_primary": "#33261B",
            "text_secondary": "#6F5640",
            "border": "#D0BEA5",
            "accent": "#9A673B",
            "accent_soft": "#F3E6D4",
            "success": "#5A7E45",
            "warning": "#A56A21",
            "danger": "#A1483B",
            "input_bg": "#FFFDF9",
            "button_bg": "#9A673B",
            "button_text": "#FFFFFF",
            "button_alt_bg": "#EADCC8",
            "button_alt_text": "#4A3624",
            "report_accent": "#9A673B",
            "report_surface": "#FBF4EA",
        },
    },
    "dark_pro": {
        "id": "dark_pro",
        "labels": {
            "zh": u"Dark Pro",
            "en": u"Dark Pro",
        },
        "tokens": {
            "window_bg": "#1C222B",
            "panel_bg": "#242C36",
            "section_bg": "#2B3541",
            "text_primary": "#F3F6FA",
            "text_secondary": "#B4C2D0",
            "border": "#465567",
            "accent": "#5AA4E8",
            "accent_soft": "#203B54",
            "success": "#4EBB74",
            "warning": "#E0A84B",
            "danger": "#D86A6A",
            "input_bg": "#202832",
            "button_bg": "#5AA4E8",
            "button_text": "#0F1822",
            "button_alt_bg": "#304050",
            "button_alt_text": "#EAF1F8",
            "report_accent": "#5AA4E8",
            "report_surface": "#202A35",
        },
    },
}


def _normalize_key(theme_id):
    return safe_text(theme_id).lower().strip()


def normalize_theme_id(theme_id, default_theme="yangagent_core"):
    key = _normalize_key(theme_id)
    if key in THEMES:
        return key
    if key in LEGACY_THEME_MAP:
        return LEGACY_THEME_MAP[key]
    return default_theme


def get_theme_id(default_theme="yangagent_core"):
    settings = read_settings()
    if "theme_id" in settings:
        return normalize_theme_id(settings.get("theme_id"), default_theme)
    if "theme" in settings:
        return normalize_theme_id(settings.get("theme"), default_theme)
    return default_theme


def save_theme_id(theme_id):
    settings = read_settings()
    normalized = normalize_theme_id(theme_id)
    settings["theme_id"] = normalized
    settings["theme"] = normalized
    write_settings(settings)
    return normalized


def get_theme_definition(theme_id=None):
    return THEMES[normalize_theme_id(theme_id or get_theme_id())]


def get_theme_labels(lang="zh"):
    normalized_lang = "en" if safe_text(lang).lower().strip() == "en" else "zh"
    labels = []
    for theme_id in THEME_IDS:
        labels.append((theme_id, THEMES[theme_id]["labels"][normalized_lang]))
    return labels


def hex_to_brush(Media, color_value):
    color_text = safe_text(color_value).lstrip("#")
    if len(color_text) == 8:
        return Media.SolidColorBrush(
            Media.Color.FromArgb(
                int(color_text[0:2], 16),
                int(color_text[2:4], 16),
                int(color_text[4:6], 16),
                int(color_text[6:8], 16),
            )
        )
    return Media.SolidColorBrush(
        Media.Color.FromRgb(
            int(color_text[0:2], 16),
            int(color_text[2:4], 16),
            int(color_text[4:6], 16),
        )
    )
