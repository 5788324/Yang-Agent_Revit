# -*- coding: utf-8 -*-
"""Set YangAgent default language."""

from __future__ import print_function

import traceback

from pyrevit import forms, script
from yang_agent_lang import choose_language, get_config_path, get_language_label, save_language


output = script.get_output()


def main():
    lang = choose_language(forms, message=u"设置默认语言 / Set default language")
    save_language(lang)
    label = get_language_label(lang)
    config_path = get_config_path()

    output.print_md(u"# YangAgent Language Settings")
    output.print_md(u"")
    output.print_md(u"- Default language: `{0}`".format(label))
    output.print_md(u"- Config: `{0}`".format(config_path))

    forms.alert(
        u"默认语言已设置为：{0}\n\nDefault language set to: {0}".format(label),
        title="Yang Agent",
    )


try:
    main()
except Exception:
    err = traceback.format_exc()
    output.print_md(u"# Language Settings failed")
    output.print_md("```text\n{0}\n```".format(err))
    forms.alert(
        u"语言设置失败。请查看 pyRevit 输出窗口。\n\nLanguage settings failed. See pyRevit output for details.",
        title="Yang Agent",
    )
