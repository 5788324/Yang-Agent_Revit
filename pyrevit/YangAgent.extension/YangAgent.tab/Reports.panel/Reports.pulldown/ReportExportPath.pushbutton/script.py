# -*- coding: utf-8 -*-
"""Set the shared YangAgent report export folder."""

from __future__ import print_function

import traceback

from pyrevit import forms, script
from yang_agent_lang import get_language
from yang_agent_report_style import build_status_block
from yang_agent_settings import get_export_dir, save_export_dir
from yang_agent_theme import get_theme_id


output = script.get_output()


TEXT = {
    "zh": {
        "title": u"报告导出路径",
        "pick": u"选择报告导出目录",
        "current": u"当前导出目录",
        "updated": u"已更新为",
        "cancel": u"已取消，保留当前导出目录。",
        "done": u"报告导出目录已更新。",
        "failed": u"报告导出路径设置失败。请查看 pyRevit 输出窗口。",
    },
    "en": {
        "title": u"Report Export Path",
        "pick": u"Select report export folder",
        "current": u"Current export folder",
        "updated": u"Updated to",
        "cancel": u"Cancelled. Current export folder was kept.",
        "done": u"Report export folder updated.",
        "failed": u"Report Export Path failed. See pyRevit output for details.",
    },
}


def tr(lang, key):
    return TEXT.get(lang, TEXT["zh"]).get(key, TEXT["zh"].get(key, key))


def main():
    lang = get_language()
    current = get_export_dir()
    picked = forms.pick_folder(title=tr(lang, "pick"))
    if not picked:
        output.print_md(u"# {0}".format(tr(lang, "title")))
        output.print_md(u"")
        output.print_md(
            build_status_block(
                get_theme_id(),
                tr(lang, "title"),
                [
                    tr(lang, "cancel"),
                    u"{0}: `{1}`".format(tr(lang, "current"), current),
                ],
            )
        )
        forms.toast(
            u"{0}\n{1}: {2}".format(tr(lang, "cancel"), tr(lang, "current"), current),
            title="Yang Agent",
        )
        return

    save_export_dir(picked)
    output.print_md(u"# {0}".format(tr(lang, "title")))
    output.print_md(u"")
    output.print_md(
        build_status_block(
            get_theme_id(),
            tr(lang, "title"),
            [
                u"{0}: `{1}`".format(tr(lang, "current"), current),
                u"{0}: `{1}`".format(tr(lang, "updated"), picked),
            ],
        )
    )
    forms.toast(u"{0}\n{1}".format(tr(lang, "done"), picked), title="Yang Agent")


try:
    main()
except Exception:
    err = traceback.format_exc()
    output.print_md(u"# Report Export Path failed")
    output.print_md("```text\n{0}\n```".format(err))
    forms.alert(TEXT["zh"]["failed"] + u"\n\n" + TEXT["en"]["failed"], title="Yang Agent")
