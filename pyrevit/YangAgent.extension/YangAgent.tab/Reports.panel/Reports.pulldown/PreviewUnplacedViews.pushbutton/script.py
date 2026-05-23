# -*- coding: utf-8 -*-
"""Preview views that may not be placed on sheets.

This tool is dry-run only. It does not modify the model and does not open a Transaction.
"""

from __future__ import print_function

import codecs
import csv
import os
import traceback
from datetime import datetime

import clr

clr.AddReference("RevitAPI")
clr.AddReference("RevitAPIUI")

from Autodesk.Revit.DB import (  # noqa: E402
    FilteredElementCollector,
    View,
    ViewSheet,
)
from pyrevit import forms, revit, script  # noqa: E402
from yang_agent_lang import get_export_dir, get_or_choose_language  # noqa: E402


doc = revit.doc
output = script.get_output()


TEXT = {
    "zh": {
        "alert_title": u"Yang Agent",
        "no_doc": u"没有打开的 Revit 文档。",
        "title": u"# Yang Agent 未上图视图预览",
        "read_only": u"此报告为 dry-run 预览，未修改 Revit 模型。",
        "summary": u"## 汇总",
        "document": u"- 文档：{0}",
        "exported_at": u"- 导出时间：{0}",
        "reportable_total": u"- 可检查视图总数：{0}",
        "unplaced_total": u"- 可能未上图视图：{0}",
        "details": u"## 可能未上图视图",
        "none": u"- 无",
        "next_steps": u"## 建议下一步",
        "step_1": u"1. 人工确认这些视图是否确实需要放到图纸。",
        "step_2": u"2. 对临时视图、工作视图、分析视图进行人工筛选。",
        "step_3": u"3. 如需自动处理，先制定公司视图命名和上图规则。",
        "output_done": u"预览完成。此工具未修改模型。",
        "output_unplaced": u"- 可能未上图视图：{0}",
        "output_report": u"- 报告：`{0}`",
        "output_csv": u"- CSV：`{0}`",
        "alert_done": u"未上图视图预览已生成。\n\n此工具未修改模型。\n\n可能未上图视图：{0}\n\n{1}",
        "failed_title": u"# 未上图视图预览失败",
        "failed_alert": u"未上图视图预览失败。请查看 pyRevit 输出窗口。",
    },
    "en": {
        "alert_title": u"Yang Agent",
        "no_doc": u"No active Revit document.",
        "title": u"# Yang Agent Unplaced Views Preview",
        "read_only": u"This is a dry-run preview. No Revit model changes were made.",
        "summary": u"## Summary",
        "document": u"- Document: {0}",
        "exported_at": u"- Exported at: {0}",
        "reportable_total": u"- Reportable views: {0}",
        "unplaced_total": u"- Views possibly not placed on sheets: {0}",
        "details": u"## Views Possibly Not Placed On Sheets",
        "none": u"- None",
        "next_steps": u"## Suggested Next Steps",
        "step_1": u"1. Confirm whether these views should be placed on sheets.",
        "step_2": u"2. Manually filter temporary, working, and analysis views.",
        "step_3": u"3. Define company view naming and sheet placement rules before automation.",
        "output_done": u"Preview completed. No model changes were made.",
        "output_unplaced": u"- Views possibly not placed on sheets: {0}",
        "output_report": u"- Report: `{0}`",
        "output_csv": u"- CSV: `{0}`",
        "alert_done": u"Unplaced views preview generated.\n\nNo model changes were made.\n\nViews possibly not placed on sheets: {0}\n\n{1}",
        "failed_title": u"# Unplaced Views Preview failed",
        "failed_alert": u"Unplaced Views Preview failed. See pyRevit output for details.",
    },
}


def tr(lang, key):
    return TEXT.get(lang, TEXT["zh"]).get(key, TEXT["zh"].get(key, key))


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


def element_id_value(element_id):
    if element_id is None:
        return u""
    try:
        return safe_text(element_id.IntegerValue)
    except Exception:
        return safe_text(element_id)


def get_placed_view_ids():
    placed_ids = set()
    sheets = FilteredElementCollector(doc).OfClass(ViewSheet).ToElements()
    for sheet in sheets:
        try:
            view_ids = sheet.GetAllPlacedViews()
            for view_id in view_ids:
                placed_ids.add(element_id_value(view_id))
        except Exception:
            continue
    return placed_ids


def is_reportable_view(view):
    if view is None:
        return False
    try:
        if view.IsTemplate:
            return False
    except Exception:
        return False
    if isinstance(view, ViewSheet):
        return False

    view_type = safe_text(view.ViewType)
    allowed = [
        "FloorPlan",
        "CeilingPlan",
        "Section",
        "Elevation",
        "ThreeD",
        "DraftingView",
        "Legend",
        "AreaPlan",
        "EngineeringPlan",
    ]
    return view_type in allowed


def collect_preview_rows():
    placed_ids = get_placed_view_ids()
    views = FilteredElementCollector(doc).OfClass(View).ToElements()
    reportable_count = 0
    unplaced = []

    for view in views:
        if not is_reportable_view(view):
            continue

        reportable_count += 1
        view_id = element_id_value(view.Id)
        if view_id in placed_ids:
            continue

        unplaced.append({
            "dry_run": "true",
            "element_id": view_id,
            "category": "View",
            "view_name": safe_text(view.Name),
            "view_type": safe_text(view.ViewType),
            "status": "PossiblyUnplaced",
        })

    return reportable_count, unplaced


def write_markdown(path, lang, reportable_count, unplaced):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    lines = []
    lines.append(tr(lang, "title"))
    lines.append(u"")
    lines.append(tr(lang, "read_only"))
    lines.append(u"")
    lines.append(tr(lang, "summary"))
    lines.append(u"")
    lines.append(tr(lang, "document").format(safe_text(doc.Title)))
    lines.append(tr(lang, "exported_at").format(timestamp))
    lines.append(tr(lang, "reportable_total").format(reportable_count))
    lines.append(tr(lang, "unplaced_total").format(len(unplaced)))
    lines.append(u"")
    lines.append(tr(lang, "details"))
    lines.append(u"")

    if not unplaced:
        lines.append(tr(lang, "none"))
    else:
        for row in unplaced:
            lines.append(
                u"- `{0}` {1} | {2}".format(
                    row["element_id"],
                    row["view_type"],
                    row["view_name"],
                )
            )

    lines.append(u"")
    lines.append(tr(lang, "next_steps"))
    lines.append(u"")
    lines.append(tr(lang, "step_1"))
    lines.append(tr(lang, "step_2"))
    lines.append(tr(lang, "step_3"))

    with codecs.open(path, "w", "utf-8-sig") as stream:
        stream.write(u"\n".join(lines))


def write_csv(path, rows):
    fieldnames = [
        "dry_run",
        "element_id",
        "category",
        "view_name",
        "view_type",
        "status",
    ]
    with open(path, "wb") as raw_stream:
        raw_stream.write(codecs.BOM_UTF8)
        writer = csv.DictWriter(raw_stream, fieldnames=fieldnames)
        header = {}
        for field in fieldnames:
            header[field] = field.encode("utf-8")
        writer.writerow(header)
        for row in rows:
            encoded = {}
            for field in fieldnames:
                encoded[field] = safe_text(row.get(field, u"")).encode("utf-8")
            writer.writerow(encoded)


def main():
    lang = get_or_choose_language(forms)

    if doc is None:
        forms.alert(tr(lang, "no_doc"), title=tr(lang, "alert_title"))
        return

    export_dir = get_export_dir()
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_path = os.path.join(export_dir, "unplaced_views_{0}.md".format(timestamp))
    csv_path = os.path.join(export_dir, "unplaced_views_{0}.csv".format(timestamp))

    reportable_count, unplaced = collect_preview_rows()
    write_markdown(report_path, lang, reportable_count, unplaced)
    write_csv(csv_path, unplaced)

    output.print_md(tr(lang, "title"))
    output.print_md(u"")
    output.print_md(tr(lang, "output_done"))
    output.print_md(u"")
    output.print_md(tr(lang, "output_unplaced").format(len(unplaced)))
    output.print_md(tr(lang, "output_report").format(report_path))
    output.print_md(tr(lang, "output_csv").format(csv_path))

    forms.toast(
        tr(lang, "alert_done").format(len(unplaced), report_path),
        title=tr(lang, "alert_title"),
    )


try:
    main()
except Exception:
    err = traceback.format_exc()
    output.print_md(TEXT["zh"]["failed_title"] + u" / " + TEXT["en"]["failed_title"].replace("# ", u""))
    output.print_md("```text\n{0}\n```".format(err))
    forms.alert(TEXT["zh"]["failed_alert"] + u"\n\n" + TEXT["en"]["failed_alert"], title="Yang Agent")
