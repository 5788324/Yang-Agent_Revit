# -*- coding: utf-8 -*-
"""Set YangAgent theme preference."""

from __future__ import print_function

import traceback

from pyrevit import forms, script
from yang_agent_lang import choose_theme, get_language, get_theme_label, save_theme


output = script.get_output()


TEXT = {
    "zh": {
        "message": u"选择插件主题 / Select plugin theme",
        "done": u"主题已设置为：{0}",
        "title": u"主题设置",
        "failed": u"主题设置失败。请查看 pyRevit 输出窗口。",
    },
    "en": {
        "message": u"Select plugin theme / 选择插件主题",
        "done": u"Theme set to: {0}",
        "title": u"Theme Settings",
        "failed": u"Theme settings failed. See pyRevit output for details.",
    },
}


def tr(lang, key):
    return TEXT.get(lang, TEXT["zh"]).get(key, TEXT["zh"].get(key, key))


def main():
    lang = get_language()
    theme = choose_theme(forms, message=tr(lang, "message"))
    save_theme(theme)
    label = get_theme_label(theme)

    output.print_md(u"# {0}".format(tr(lang, "title")))
    output.print_md(u"")
    output.print_md(u"- `{0}`".format(label))

    forms.alert(tr(lang, "done").format(label), title="Yang Agent")


try:
    main()
except Exception:
    err = traceback.format_exc()
    output.print_md(u"# Theme Settings failed")
    output.print_md("```text\n{0}\n```".format(err))
    forms.alert(TEXT["zh"]["failed"] + u"\n\n" + TEXT["en"]["failed"], title="Yang Agent")
