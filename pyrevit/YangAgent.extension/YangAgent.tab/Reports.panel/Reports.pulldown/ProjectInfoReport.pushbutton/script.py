# -*- coding: utf-8 -*-
"""Export a read-only project information report."""

from __future__ import print_function

import codecs
import os
import traceback
from datetime import datetime

import clr

clr.AddReference("RevitAPI")
clr.AddReference("RevitAPIUI")

from Autodesk.Revit.DB import (  # noqa: E402
    BuiltInCategory,
    FilteredElementCollector,
    FilteredWorksetCollector,
    Level,
    ModelPathUtils,
    RevitLinkInstance,
    View,
    ViewSheet,
)
from pyrevit import forms, revit, script  # noqa: E402
from yang_agent_lang import get_or_choose_language  # noqa: E402
from yang_agent_report_style import build_intro_block, build_status_block  # noqa: E402
from yang_agent_settings import get_export_dir  # noqa: E402
from yang_agent_theme import get_theme_id  # noqa: E402


doc = revit.doc
output = script.get_output()


TEXT = {
    "zh": {
        "language_message": u"\u9009\u62e9\u62a5\u544a\u8bed\u8a00 / Select report language",
        "alert_title": u"Yang Agent",
        "no_doc": u"\u6ca1\u6709\u6253\u5f00\u7684 Revit \u6587\u6863\u3002",
        "report_title": u"# Yang Agent \u9879\u76ee\u4fe1\u606f\u62a5\u544a",
        "read_only_note": u"\u6b64\u62a5\u544a\u4e3a\u53ea\u8bfb\u6458\u8981\uff0c\u672a\u4fee\u6539 Revit \u6a21\u578b\u3002",
        "document_info": u"## \u6587\u6863\u4fe1\u606f",
        "document": u"- \u6587\u6863\uff1a{0}",
        "path": u"- \u8def\u5f84\uff1a{0}",
        "revit": u"- Revit\uff1a{0} ({1})",
        "exported_at": u"- \u5bfc\u51fa\u65f6\u95f4\uff1a{0}",
        "current_view": u"- \u5f53\u524d\u89c6\u56fe\uff1a{0}",
        "workshared": u"- Workshared\uff1a{0}",
        "central_path": u"- \u4e2d\u592e\u6a21\u578b\uff1a{0}",
        "stats": u"## \u7edf\u8ba1\u6458\u8981",
        "views": u"- \u89c6\u56fe\u603b\u6570\uff1a{0}",
        "sheets": u"- \u56fe\u7eb8\u603b\u6570\uff1a{0}",
        "levels": u"- \u6807\u9ad8\u603b\u6570\uff1a{0}",
        "rooms": u"- \u623f\u95f4\u603b\u6570\uff1a{0}",
        "doors": u"- \u95e8\u603b\u6570\uff1a{0}",
        "windows": u"- \u7a97\u603b\u6570\uff1a{0}",
        "titleblocks": u"- \u6807\u9898\u680f\u603b\u6570\uff1a{0}",
        "links": u"- Revit \u94fe\u63a5\u5b9e\u4f8b\uff1a{0}",
        "worksets": u"- \u5de5\u4f5c\u96c6\u603b\u6570\uff1a{0}",
        "next_steps": u"## \u5efa\u8bae\u4e0b\u4e00\u6b65",
        "next_step_1": u"1. \u7528\u8fd9\u4e2a\u62a5\u544a\u5feb\u901f\u5224\u65ad\u9879\u76ee\u89c4\u6a21\u548c\u57fa\u7840\u7ed3\u6784\u3002",
        "next_step_2": u"2. \u5982\u9700\u66f4\u8be6\u7ec6\u5206\u6790\uff0c\u518d\u8fd0\u884c\u6a21\u578b\u5feb\u7167\u6216\u6a21\u578b\u5065\u5eb7\u62a5\u544a\u3002",
        "next_step_3": u"3. \u7ee7\u7eed\u4f18\u5148\u4f7f\u7528\u53ea\u8bfb\u62a5\u544a\u548c\u5feb\u7167\u5de5\u5177\uff0c\u518d\u51b3\u5b9a\u662f\u5426\u505a\u540e\u7eed\u6df1\u5ea6\u5206\u6790\u3002",
        "yes": u"\u662f",
        "no": u"\u5426",
        "none": u"\u65e0",
        "output_title": u"# Yang Agent \u9879\u76ee\u4fe1\u606f\u62a5\u544a",
        "output_done": u"\u9879\u76ee\u4fe1\u606f\u62a5\u544a\u751f\u6210\u5b8c\u6210\u3002\u6b64\u5de5\u5177\u672a\u4fee\u6539\u6a21\u578b\u3002",
        "output_report": u"- \u62a5\u544a\uff1a`{0}`",
        "alert_done": u"\u9879\u76ee\u4fe1\u606f\u62a5\u544a\u5df2\u751f\u6210\u3002\n\n\u6b64\u5de5\u5177\u672a\u4fee\u6539\u6a21\u578b\u3002\n\n{0}",
        "failed_title": u"# \u9879\u76ee\u4fe1\u606f\u62a5\u544a\u5931\u8d25",
        "failed_alert": u"\u9879\u76ee\u4fe1\u606f\u62a5\u544a\u5931\u8d25\u3002\u8bf7\u67e5\u770b pyRevit \u8f93\u51fa\u7a97\u53e3\u3002",
    },
    "en": {
        "language_message": u"Select report language / \u9009\u62e9\u62a5\u544a\u8bed\u8a00",
        "alert_title": u"Yang Agent",
        "no_doc": u"No active Revit document.",
        "report_title": u"# Yang Agent Project Info Report",
        "read_only_note": u"This is a read-only summary. No Revit model changes were made.",
        "document_info": u"## Document Info",
        "document": u"- Document: {0}",
        "path": u"- Path: {0}",
        "revit": u"- Revit: {0} ({1})",
        "exported_at": u"- Exported at: {0}",
        "current_view": u"- Current view: {0}",
        "workshared": u"- Workshared: {0}",
        "central_path": u"- Central model: {0}",
        "stats": u"## Summary Stats",
        "views": u"- Total views: {0}",
        "sheets": u"- Total sheets: {0}",
        "levels": u"- Total levels: {0}",
        "rooms": u"- Total rooms: {0}",
        "doors": u"- Total doors: {0}",
        "windows": u"- Total windows: {0}",
        "titleblocks": u"- Total title blocks: {0}",
        "links": u"- Revit link instances: {0}",
        "worksets": u"- Total worksets: {0}",
        "next_steps": u"## Suggested Next Steps",
        "next_step_1": u"1. Use this report to understand basic project scale and structure.",
        "next_step_2": u"2. Run model snapshot or model health report for deeper analysis.",
        "next_step_3": u"3. Continue using read-only reports and snapshots first before deciding on deeper analysis.",
        "yes": u"Yes",
        "no": u"No",
        "none": u"None",
        "output_title": u"# Yang Agent Project Info Report",
        "output_done": u"Project info report completed. No model changes were made.",
        "output_report": u"- Report: `{0}`",
        "alert_done": u"Project info report generated.\n\nNo model changes were made.\n\n{0}",
        "failed_title": u"# Project Info Report failed",
        "failed_alert": u"Project Info Report failed. See pyRevit output for details.",
    },
}


def choose_language():
    try:
        return get_or_choose_language(forms, message=TEXT["zh"]["language_message"])
    except Exception:
        return "zh"


def tr(lang, key):
    return TEXT.get(lang, TEXT["zh"]).get(key, TEXT["zh"].get(key, key))


def safe_text(value):
    if value is None:
        return u""
    try:
        return unicode(value)  # noqa: F821
    except NameError:
        return str(value)
    except Exception:
        try:
            return str(value)
        except Exception:
            return u""


def count_by_category(category):
    return (
        FilteredElementCollector(doc)
        .OfCategory(category)
        .WhereElementIsNotElementType()
        .GetElementCount()
    )


def count_by_class(cls):
    return FilteredElementCollector(doc).OfClass(cls).GetElementCount()


def get_workset_count():
    try:
        return len(list(FilteredWorksetCollector(doc).ToWorksets()))
    except Exception:
        return 0


def get_central_model_path(lang):
    try:
        if not doc.IsWorkshared:
            return tr(lang, "none")
        model_path = doc.GetWorksharingCentralModelPath()
        if model_path is None:
            return tr(lang, "none")
        path_text = ModelPathUtils.ConvertModelPathToUserVisiblePath(model_path)
        if safe_text(path_text).strip():
            return safe_text(path_text)
    except Exception:
        pass
    return tr(lang, "none")


def build_report(lang):
    app = doc.Application
    theme_id = get_theme_id()
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    try:
        current_view = safe_text(doc.ActiveView.Name)
    except Exception:
        current_view = tr(lang, "none")

    is_workshared = False
    try:
        is_workshared = doc.IsWorkshared
    except Exception:
        pass

    stats_lines = [
        tr(lang, "views").format(count_by_class(View)),
        tr(lang, "sheets").format(count_by_class(ViewSheet)),
        tr(lang, "levels").format(count_by_class(Level)),
        tr(lang, "rooms").format(count_by_category(BuiltInCategory.OST_Rooms)),
        tr(lang, "doors").format(count_by_category(BuiltInCategory.OST_Doors)),
        tr(lang, "windows").format(count_by_category(BuiltInCategory.OST_Windows)),
        tr(lang, "titleblocks").format(count_by_category(BuiltInCategory.OST_TitleBlocks)),
        tr(lang, "links").format(count_by_class(RevitLinkInstance)),
        tr(lang, "worksets").format(get_workset_count()),
    ]

    lines = []
    lines.append(build_intro_block(theme_id, tr(lang, "report_title"), tr(lang, "read_only_note")))
    lines.append(u"")
    lines.append(tr(lang, "document_info"))
    lines.append(u"")
    lines.append(tr(lang, "document").format(safe_text(doc.Title)))
    lines.append(tr(lang, "path").format(safe_text(doc.PathName)))
    lines.append(tr(lang, "revit").format(safe_text(app.VersionName), safe_text(app.VersionNumber)))
    lines.append(tr(lang, "exported_at").format(timestamp))
    lines.append(tr(lang, "current_view").format(current_view))
    lines.append(tr(lang, "workshared").format(tr(lang, "yes") if is_workshared else tr(lang, "no")))
    lines.append(tr(lang, "central_path").format(get_central_model_path(lang)))
    lines.append(u"")
    lines.append(build_status_block(theme_id, tr(lang, "stats").replace("## ", ""), stats_lines))
    lines.append(u"")
    lines.append(
        build_status_block(
            theme_id,
            tr(lang, "next_steps").replace("## ", ""),
            [
                tr(lang, "next_step_1").replace("1. ", ""),
                tr(lang, "next_step_2").replace("2. ", ""),
                tr(lang, "next_step_3").replace("3. ", ""),
            ],
        )
    )
    return lines


def write_report(path, lines):
    with codecs.open(path, "w", "utf-8-sig") as stream:
        stream.write(u"\n".join(lines))


def main():
    lang = choose_language()
    if doc is None:
        forms.alert(tr(lang, "no_doc"), title=tr(lang, "alert_title"))
        return

    export_dir = get_export_dir()
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_path = os.path.join(export_dir, "project_info_report_{0}.md".format(timestamp))

    lines = build_report(lang)
    write_report(report_path, lines)

    output.print_md(tr(lang, "output_title"))
    output.print_md("")
    output.print_md(tr(lang, "output_done"))
    output.print_md(tr(lang, "output_report").format(report_path))

    forms.toast(tr(lang, "alert_done").format(report_path), title=tr(lang, "alert_title"))


try:
    main()
except Exception:
    err = traceback.format_exc()
    output.print_md(TEXT["zh"]["failed_title"] + u" / " + TEXT["en"]["failed_title"].replace("# ", u""))
    output.print_md("```text\n{0}\n```".format(err))
    forms.alert(TEXT["zh"]["failed_alert"] + u"\n\n" + TEXT["en"]["failed_alert"], title="Yang Agent")
