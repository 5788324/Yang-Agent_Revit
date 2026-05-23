# -*- coding: utf-8 -*-
"""Shared language preference helpers for YangAgent pyRevit tools."""

from __future__ import print_function

import codecs
import json
import os


SUPPORTED_LANGUAGES = ["zh", "en"]
SUPPORTED_THEMES = ["light", "dark"]
DEFAULT_VIEW_NAMING_RULES = {
    "prefix_by_view_type": {
        "FloorPlan": ["FP-", "PL-", "A-", "S-", "M-", "E-"],
        "CeilingPlan": ["RCP-", "CP-"],
        "Section": ["SEC-", "SECTION-"],
        "Elevation": ["EL-", "ELEV-"],
        "ThreeD": ["3D-"],
        "DraftingView": ["DR-", "DET-", "DT-"],
        "Legend": ["LG-", "LEG-"],
        "AreaPlan": ["AR-", "AREA-"],
        "EngineeringPlan": ["EP-", "ENG-"],
    },
    "temporary_keywords": [
        u"临时",
        u"测试",
        u"工作",
        u"temp",
        u"test",
        u"working",
        u"copy",
        u"复制",
    ],
}
LANGUAGE_LABELS = {
    "zh": u"中文",
    "en": u"English",
}
THEME_LABELS = {
    "light": u"Light Theme",
    "dark": u"Dark Theme",
}


def _safe_text(value):
    if value is None:
        return u""
    try:
        return unicode(value)  # noqa: F821  # IronPython
    except NameError:
        return str(value)
    except Exception:
        try:
            return str(value)
        except Exception:
            return u""


def get_config_dir():
    root = os.environ.get("APPDATA") or os.path.expanduser("~")
    path = os.path.join(root, "YangAgent_Revit")
    if not os.path.isdir(path):
        os.makedirs(path)
    return path


def get_config_path():
    return os.path.join(get_config_dir(), "settings.json")


def read_settings():
    path = get_config_path()
    if not os.path.isfile(path):
        return {}
    try:
        with codecs.open(path, "r", "utf-8-sig") as stream:
            return json.loads(stream.read())
    except Exception:
        return {}


def write_settings(settings):
    path = get_config_path()
    with codecs.open(path, "w", "utf-8-sig") as stream:
        stream.write(json.dumps(settings, ensure_ascii=False, indent=2))


def _clean_list(values):
    cleaned = []
    if not isinstance(values, list):
        return cleaned
    for value in values:
        text = _safe_text(value).strip()
        if text:
            cleaned.append(text)
    return cleaned


def normalize_language(lang):
    lang = _safe_text(lang).lower().strip()
    if lang in SUPPORTED_LANGUAGES:
        return lang
    if lang in ["chinese", "cn", "zh-cn", "中文"]:
        return "zh"
    if lang in ["english", "en-us"]:
        return "en"
    return "zh"


def get_language(default_lang="zh"):
    settings = read_settings()
    return normalize_language(settings.get("language", default_lang))


def save_language(lang):
    settings = read_settings()
    settings["language"] = normalize_language(lang)
    write_settings(settings)
    return settings["language"]


def normalize_theme(theme):
    theme = _safe_text(theme).lower().strip()
    if theme in SUPPORTED_THEMES:
        return theme
    if theme in ["light theme", "亮色", "浅色"]:
        return "light"
    if theme in ["dark theme", "暗色", "深色"]:
        return "dark"
    return "light"


def get_theme(default_theme="light"):
    settings = read_settings()
    return normalize_theme(settings.get("theme", default_theme))


def save_theme(theme):
    settings = read_settings()
    settings["theme"] = normalize_theme(theme)
    write_settings(settings)
    return settings["theme"]


def get_theme_label(theme):
    return THEME_LABELS.get(normalize_theme(theme), THEME_LABELS["light"])


def save_user_profile(nickname=None, avatar_path=None):
    settings = read_settings()
    if nickname is not None:
        settings["nickname"] = _safe_text(nickname).strip()
    if avatar_path is not None:
        settings["avatar_path"] = _safe_text(avatar_path).strip()
    write_settings(settings)
    return settings


def get_user_profile():
    settings = read_settings()
    return {
        "nickname": _safe_text(settings.get("nickname", "")),
        "avatar_path": _safe_text(settings.get("avatar_path", "")),
    }


def get_view_naming_rules():
    settings = read_settings()
    rules = settings.get("view_naming_rules")
    if not isinstance(rules, dict):
        return DEFAULT_VIEW_NAMING_RULES

    prefix_rules = rules.get("prefix_by_view_type")
    if not isinstance(prefix_rules, dict):
        prefix_rules = DEFAULT_VIEW_NAMING_RULES["prefix_by_view_type"]

    cleaned_prefix_rules = {}
    for view_type in DEFAULT_VIEW_NAMING_RULES["prefix_by_view_type"]:
        values = prefix_rules.get(view_type)
        cleaned = _clean_list(values)
        if not cleaned:
            cleaned = DEFAULT_VIEW_NAMING_RULES["prefix_by_view_type"][view_type]
        cleaned_prefix_rules[view_type] = cleaned

    keywords = _clean_list(rules.get("temporary_keywords"))
    if not keywords:
        keywords = DEFAULT_VIEW_NAMING_RULES["temporary_keywords"]

    return {
        "prefix_by_view_type": cleaned_prefix_rules,
        "temporary_keywords": keywords,
    }


def save_view_naming_rules(prefix_by_view_type=None, temporary_keywords=None):
    settings = read_settings()
    current = get_view_naming_rules()
    if prefix_by_view_type is not None:
        current["prefix_by_view_type"] = prefix_by_view_type
    if temporary_keywords is not None:
        current["temporary_keywords"] = temporary_keywords
    settings["view_naming_rules"] = current
    write_settings(settings)
    return current


def save_export_dir(path):
    settings = read_settings()
    settings["export_dir"] = _safe_text(path).strip()
    write_settings(settings)
    return settings["export_dir"]


def get_default_export_dir():
    desktop = os.path.join(os.path.expanduser("~"), "Desktop")
    if not os.path.isdir(desktop):
        desktop = os.path.expanduser("~")
    return os.path.join(desktop, "YangAgent_Revit_Exports")


def get_export_dir():
    settings = read_settings()
    export_dir = _safe_text(settings.get("export_dir", ""))
    if not export_dir:
        export_dir = get_default_export_dir()
    if not os.path.isdir(export_dir):
        os.makedirs(export_dir)
    return export_dir


def get_language_label(lang):
    return LANGUAGE_LABELS.get(normalize_language(lang), LANGUAGE_LABELS["zh"])


def choose_theme(forms, message=None, default_theme="light"):
    selected = forms.CommandSwitchWindow.show(
        [THEME_LABELS["light"], THEME_LABELS["dark"]],
        message=message or u"选择主题 / Select theme",
    )
    if selected == THEME_LABELS["dark"]:
        return "dark"
    if selected == THEME_LABELS["light"]:
        return "light"
    return normalize_theme(default_theme)


def choose_language(forms, message=None, default_lang="zh"):
    selected = forms.CommandSwitchWindow.show(
        [LANGUAGE_LABELS["zh"], LANGUAGE_LABELS["en"]],
        message=message or u"选择语言 / Select language",
    )
    if selected == LANGUAGE_LABELS["en"]:
        return "en"
    if selected == LANGUAGE_LABELS["zh"]:
        return "zh"
    return normalize_language(default_lang)


def get_or_choose_language(forms, message=None):
    settings = read_settings()
    saved = settings.get("language")
    if saved:
        return normalize_language(saved)
    lang = choose_language(forms, message=message)
    save_language(lang)
    return lang
