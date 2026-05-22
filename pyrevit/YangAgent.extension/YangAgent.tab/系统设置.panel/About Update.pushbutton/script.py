# -*- coding: utf-8 -*-
"""Show YangAgent copyright and update link."""

from __future__ import print_function

import traceback

from pyrevit import forms, script
from yang_agent_lang import get_language, get_user_profile, get_theme


output = script.get_output()
UPDATE_URL = "https://github.com/5788324/Yang-Agent_Revit"


TEXT = {
    "zh": {
        "title": u"关于 YangAgent",
        "copyright": u"版权声明：由 Yang 开发，工具为 Codex。",
        "update": u"插件更新链接",
        "theme": u"当前主题",
        "nickname": u"用户简称",
        "message": u"由 Yang 开发，工具为 Codex。\n\n更新链接：\n{0}",
        "failed": u"关于信息打开失败。请查看 pyRevit 输出窗口。",
    },
    "en": {
        "title": u"About YangAgent",
        "copyright": u"Copyright: Developed by Yang, powered by Codex.",
        "update": u"Plugin update link",
        "theme": u"Current theme",
        "nickname": u"Nickname",
        "message": u"Developed by Yang, powered by Codex.\n\nUpdate link:\n{0}",
        "failed": u"About failed. See pyRevit output for details.",
    },
}


def tr(lang, key):
    return TEXT.get(lang, TEXT["zh"]).get(key, TEXT["zh"].get(key, key))


def main():
    lang = get_language()
    profile = get_user_profile()
    theme = get_theme()

    output.print_md(u"# {0}".format(tr(lang, "title")))
    output.print_md(u"")
    output.print_md(tr(lang, "copyright"))
    output.print_md(u"")
    output.print_md(u"- {0}: `{1}`".format(tr(lang, "nickname"), profile.get("nickname", "")))
    output.print_md(u"- {0}: `{1}`".format(tr(lang, "theme"), theme))
    output.print_md(u"- {0}: {1}".format(tr(lang, "update"), UPDATE_URL))

    forms.alert(tr(lang, "message").format(UPDATE_URL), title="Yang Agent")


try:
    main()
except Exception:
    err = traceback.format_exc()
    output.print_md(u"# About failed")
    output.print_md("```text\n{0}\n```".format(err))
    forms.alert(TEXT["zh"]["failed"] + u"\n\n" + TEXT["en"]["failed"], title="Yang Agent")
