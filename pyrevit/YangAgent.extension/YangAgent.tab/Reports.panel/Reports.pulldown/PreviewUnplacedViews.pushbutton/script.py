# -*- coding: utf-8 -*-
"""Preview views that may not be placed on sheets in read-only dry-run mode."""

from __future__ import print_function

import codecs
import csv
import os
import traceback
from datetime import datetime

import clr

clr.AddReference("RevitAPI")
clr.AddReference("RevitAPIUI")

from Autodesk.Revit.DB import FilteredElementCollector, View, ViewSheet  # noqa: E402
from pyrevit import forms, revit, script  # noqa: E402
from yang_agent_lang import get_or_choose_language  # noqa: E402
from yang_agent_report_style import build_intro_block, build_status_block  # noqa: E402
from yang_agent_settings import get_export_dir  # noqa: E402
from yang_agent_theme import get_theme_id  # noqa: E402


doc = revit.doc
output = script.get_output()


TEXT = {
    "zh": {
        "language_message": u"选择报告语言 / Select report language",
        "alert_title": u"Yang Agent",
        "no_doc": u"没有打开的 Revit 文档。",
        "report_title": u"# Yang Agent 预览未上图视图",
        "read_only_note": u"这是 dry-run 只读预览，不会修改 Revit 模型。",
        "summary_heading": u"统计摘要",
        "document": u"文档：{0}",
        "exported_at": u"导出时间：{0}",
        "reportable_total": u"纳入检查的视图数量：{0}",
        "unplaced_total": u"可能未上图的视图数量：{0}",
        "detail_heading": u"可能未上图的视图明细",
        "next_steps_heading": u"建议下一步",
        "next_step_1": u"先人工确认这些视图是否本来就不需要上图，例如工作视图、临时视图或分析视图。",
        "next_step_2": u"如果项目存在依赖视图、图例或特殊出图规则，需要再做人工筛选。",
        "next_step_3": u"正式自动化前，应先固化视图命名和出图范围规则。",
        "none": u"无",
        "output_title": u"# Yang Agent 预览未上图视图",
        "output_done": u"预览完成。该工具未修改模型。",
        "output_unplaced": u"- 可能未上图的视图数量：{0}",
        "output_report": u"- 报告：`{0}`",
        "output_csv": u"- CSV：`{0}`",
        "alert_done": u"未上图视图预览已生成。\n\n该工具未修改模型。\n\n可能未上图的视图数量：{0}\n\n{1}",
        "failed_title": u"# 未上图视图预览失败",
        "failed_alert": u"未上图视图预览失败。请查看 pyRevit 输出窗口。",
    },
    "en": {
        "language_message": u"Select report language / 选择报告语言",
        "alert_title": u"Yang Agent",
        "no_doc": u"No active Revit document.",
        "report_title": u"# Yang Agent Unplaced Views Preview",
        "read_only_note": u"This is a dry-run read-only preview. No Revit model changes were made.",
        "summary_heading": u"Summary",
        "document": u"Document: {0}",
        "exported_at": u"Exported at: {0}",
        "reportable_total": u"Views checked: {0}",
        "unplaced_total": u"Views possibly not placed on sheets: {0}",
        "detail_heading": u"Views Possibly Not Placed On Sheets",
        "next_steps_heading": u"Suggested Next Steps",
        "next_step_1": u"Confirm whether these views are intentionally excluded from sheets, such as working or analysis views.",
        "next_step_2": u"Dependent views, legends, or custom sheet rules may still need manual review.",
        "next_step_3": u"Stabilize view naming and sheet placement rules before further automation.",
        "none": u"None",
        "output_title": u"# Yang Agent Unplaced Views Preview",
        "output_done": u"Preview completed. No model changes were made.",
        "output_unplaced": u"- Views possibly not placed on sheets: {0}",
        "output_report": u"- Report: `{0}`",
        "output_csv": u"- CSV: `{0}`",
        "alert_done": u"Unplaced views preview generated.\n\nNo model changes were made.\n\nViews possibly not placed on sheets: {0}\n\n{1}",
        "failed_title": u"# Unplaced Views Preview failed",
        "failed_alert": u"Unplaced Views Preview failed. See pyRevit output for details.",
    },
}


ALLOWED_VIEW_TYPES = [
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
            for view_id in sheet.GetAllPlacedViews():
                placed_ids.add(element_id_value(view_id))
        except Exception:
            pass
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
    return safe_text(view.ViewType) in ALLOWED_VIEW_TYPES


def collect_preview_rows():
    placed_ids = get_placed_view_ids()
    reportable_count = 0
    unplaced = []
    views = FilteredElementCollector(doc).OfClass(View).ToElements()
    for view in views:
        if not is_reportable_view(view):
            continue

        reportable_count += 1
        view_id = element_id_value(view.Id)
        if view_id in placed_ids:
            continue

        unplaced.append(
            {
                "dry_run": "true",
                "element_id": view_id,
                "category": "View",
                "view_name": safe_text(view.Name),
                "view_type": safe_text(view.ViewType),
                "status": "PossiblyUnplaced",
            }
        )
    return reportable_count, unplaced


def build_report_lines(lang, reportable_count, unplaced):
    theme_id = get_theme_id()
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    summary_lines = [
        tr(lang, "document").format(safe_text(doc.Title)),
        tr(lang, "exported_at").format(timestamp),
        tr(lang, "reportable_total").format(reportable_count),
        tr(lang, "unplaced_total").format(len(unplaced)),
    ]
    next_step_lines = [
        tr(lang, "next_step_1"),
        tr(lang, "next_step_2"),
        tr(lang, "next_step_3"),
    ]

    lines = []
    lines.append(build_intro_block(theme_id, tr(lang, "report_title"), tr(lang, "read_only_note")))
    lines.append(u"")
    lines.append(build_status_block(theme_id, tr(lang, "summary_heading"), summary_lines))
    lines.append(u"")
    lines.append(u"## {0}".format(tr(lang, "detail_heading")))
    lines.append(u"")

    if not unplaced:
        lines.append(u"- {0}".format(tr(lang, "none")))
    else:
        for row in unplaced:
            lines.append(
                u"- ElementId `{0}` | {1} | {2}".format(
                    row["element_id"],
                    row["view_type"] or tr(lang, "none"),
                    row["view_name"] or tr(lang, "none"),
                )
            )

    lines.append(u"")
    lines.append(build_status_block(theme_id, tr(lang, "next_steps_heading"), next_step_lines))
    return lines


def write_markdown(path, lines):
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
    lang = choose_language()
    if doc is None:
        forms.alert(tr(lang, "no_doc"), title=tr(lang, "alert_title"))
        return

    export_dir = get_export_dir()
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_path = os.path.join(export_dir, "unplaced_views_{0}.md".format(timestamp))
    csv_path = os.path.join(export_dir, "unplaced_views_{0}.csv".format(timestamp))

    reportable_count, unplaced = collect_preview_rows()
    write_markdown(report_path, build_report_lines(lang, reportable_count, unplaced))
    write_csv(csv_path, unplaced)

    output.print_md(tr(lang, "output_title"))
    output.print_md(u"")
    output.print_md(tr(lang, "output_done"))
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
