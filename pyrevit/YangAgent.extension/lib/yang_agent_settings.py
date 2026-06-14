# -*- coding: utf-8 -*-
"""Shared settings and local config helpers for YangAgent."""

from __future__ import print_function

import codecs
import json
import os


def safe_text(value):
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
    with codecs.open(get_config_path(), "w", "utf-8-sig") as stream:
        stream.write(json.dumps(settings, ensure_ascii=False, indent=2))


def get_default_export_dir():
    desktop = os.path.join(os.path.expanduser("~"), "Desktop")
    if not os.path.isdir(desktop):
        desktop = os.path.expanduser("~")
    return os.path.join(desktop, "YangAgent_Revit_Exports")


def get_export_dir():
    settings = read_settings()
    export_dir = safe_text(settings.get("export_dir", ""))
    if not export_dir:
        export_dir = get_default_export_dir()
    if not os.path.isdir(export_dir):
        os.makedirs(export_dir)
    return export_dir


def save_export_dir(path):
    settings = read_settings()
    settings["export_dir"] = safe_text(path).strip()
    write_settings(settings)
    return settings["export_dir"]
