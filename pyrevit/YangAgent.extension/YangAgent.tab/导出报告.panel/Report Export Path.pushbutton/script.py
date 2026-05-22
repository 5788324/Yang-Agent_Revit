# -*- coding: utf-8 -*-
"""Set YangAgent report export folder."""

from __future__ import print_function

import traceback

from pyrevit import forms, script
from yang_agent_lang import get_export_dir, get_language, save_export_dir


output = script.get_output()


TEXT = {
    "zh": {
        "title": u"报告导出路径",
        "pick": u"选择报告导出目录",
        "current": u"当前导出目录",
        "done": u"报告导出目录已设置为：\n{0}",
        "cancel": u"已取消。当前导出目录保持不变：\n{0}",
        "failed": u"导出路径设置失败。请查看 pyRevit 输出窗口。",
    },
    "en": {
        "title": u"Report Export Path",
        "pick": u"Select report export folder",
        "current": u"Current export folder",
        "done": u"Report export folder set to:\n{0}",
        "cancel": u"Cancelled. Current export folder remains:\n{0}",
        "failed": u"Report export path failed. See pyRevit output for details.",
    },
}


def tr(lang, key):
    return TEXT.get(lang, TEXT["zh"]).get(key, TEXT["zh"].get(key, key))


def main():
    lang = get_language()
    current = get_export_dir()
    picked = forms.pick_folder(title=tr(lang, "pick"))
    if not picked:
        forms.alert(tr(lang, "cancel").format(current), title="Yang Agent")
        return

    save_export_dir(picked)
    output.print_md(u"# {0}".format(tr(lang, "title")))
    output.print_md(u"")
    output.print_md(u"- {0}: `{1}`".format(tr(lang, "current"), picked))
    forms.alert(tr(lang, "done").format(picked), title="Yang Agent")


try:
    main()
except Exception:
    err = traceback.format_exc()
    output.print_md(u"# Report Export Path failed")
    output.print_md("```text\n{0}\n```".format(err))
    forms.alert(TEXT["zh"]["failed"] + u"\n\n" + TEXT["en"]["failed"], title="Yang Agent")
