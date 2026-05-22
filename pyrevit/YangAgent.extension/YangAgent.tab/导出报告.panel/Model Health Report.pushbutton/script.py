# -*- coding: utf-8 -*-
"""Generate a read-only Revit model health report.

This pyRevit tool does not modify the model and does not open a Transaction.
It writes a Markdown report to Desktop/YangAgent_Revit_Exports.
"""

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
    BuiltInParameter,
    FilteredElementCollector,
    View,
    ViewSheet,
)
from Autodesk.Revit.DB.Architecture import Room  # noqa: E402
from pyrevit import forms, revit, script  # noqa: E402
from yang_agent_lang import get_export_dir, get_or_choose_language  # noqa: E402


doc = revit.doc
output = script.get_output()


TEXT = {
    "zh": {
        "language_message": u"选择报告语言 / Select report language",
        "alert_title": u"Yang Agent",
        "no_doc": u"没有打开的 Revit 文档。",
        "report_title": u"# Yang Agent 模型健康报告",
        "read_only_note": u"此报告为只读检查结果，未修改 Revit 模型。",
        "document_info": u"## 文档信息",
        "document": u"- 文档：{0}",
        "path": u"- 路径：{0}",
        "revit": u"- Revit：{0} ({1})",
        "exported_at": u"- 导出时间：{0}",
        "issue_count": u"- 问题计数：{0}",
        "room_check": u"## 房间检查",
        "room_total": u"- 房间总数：{0}",
        "room_missing_number": u"- 缺少编号：{0}",
        "room_missing_name": u"- 缺少名称：{0}",
        "room_duplicate_groups": u"- 重复编号组：{0}",
        "missing_room_numbers": u"### 缺少编号的房间",
        "missing_room_names": u"### 缺少名称的房间",
        "duplicate_room_numbers": u"### 重复房间编号",
        "door_window_check": u"## 门窗标记检查",
        "door_total": u"- 门总数：{0}",
        "door_missing": u"- 门缺少标记：{0}",
        "window_total": u"- 窗总数：{0}",
        "window_missing": u"- 窗缺少标记：{0}",
        "missing_doors": u"### 缺少标记的门",
        "missing_windows": u"### 缺少标记的窗",
        "view_check": u"## 视图上图检查",
        "view_total": u"- 可检查视图总数：{0}",
        "view_unplaced": u"- 可能未放置到图纸的视图：{0}",
        "unplaced_views": u"### 可能未上图视图",
        "next_steps": u"## 建议下一步",
        "next_step_1": u"1. 把此报告交给 Codex 或 Claude 分析。",
        "next_step_2": u"2. 先人工确认问题是否符合公司标准。",
        "next_step_3": u"3. 再为单一问题生成 dry-run 修复脚本。",
        "none": u"- 无",
        "more_items": u"- ...还有 {0} 项未显示",
        "output_title": u"# Yang Agent 模型健康报告",
        "output_done": u"报告生成完成。此工具未修改模型。",
        "output_issues": u"- 问题计数：{0}",
        "output_report": u"- 报告：`{0}`",
        "alert_done": u"模型健康报告已生成。\n\n此工具未修改模型。\n\n问题计数：{0}\n\n{1}",
        "failed_title": u"# 模型健康报告失败",
        "failed_alert": u"模型健康报告失败。请查看 pyRevit 输出窗口。",
    },
    "en": {
        "language_message": u"Select report language / 选择报告语言",
        "alert_title": u"Yang Agent",
        "no_doc": u"No active Revit document.",
        "report_title": u"# Yang Agent Model Health Report",
        "read_only_note": u"This is a read-only report. No Revit model changes were made.",
        "document_info": u"## Document Info",
        "document": u"- Document: {0}",
        "path": u"- Path: {0}",
        "revit": u"- Revit: {0} ({1})",
        "exported_at": u"- Exported at: {0}",
        "issue_count": u"- Issue count: {0}",
        "room_check": u"## Room Check",
        "room_total": u"- Total rooms: {0}",
        "room_missing_number": u"- Missing numbers: {0}",
        "room_missing_name": u"- Missing names: {0}",
        "room_duplicate_groups": u"- Duplicate number groups: {0}",
        "missing_room_numbers": u"### Rooms Missing Numbers",
        "missing_room_names": u"### Rooms Missing Names",
        "duplicate_room_numbers": u"### Duplicate Room Numbers",
        "door_window_check": u"## Door and Window Mark Check",
        "door_total": u"- Total doors: {0}",
        "door_missing": u"- Doors missing marks: {0}",
        "window_total": u"- Total windows: {0}",
        "window_missing": u"- Windows missing marks: {0}",
        "missing_doors": u"### Doors Missing Marks",
        "missing_windows": u"### Windows Missing Marks",
        "view_check": u"## View Placement Check",
        "view_total": u"- Reportable views: {0}",
        "view_unplaced": u"- Views possibly not placed on sheets: {0}",
        "unplaced_views": u"### Views Possibly Not Placed On Sheets",
        "next_steps": u"## Suggested Next Steps",
        "next_step_1": u"1. Ask Codex or Claude to analyze this report.",
        "next_step_2": u"2. Confirm the findings against company standards.",
        "next_step_3": u"3. Generate a dry-run repair script for one issue type at a time.",
        "none": u"- None",
        "more_items": u"- ...{0} more items not shown",
        "output_title": u"# Yang Agent Model Health Report",
        "output_done": u"Report completed. No model changes were made.",
        "output_issues": u"- Issues counted: {0}",
        "output_report": u"- Report: `{0}`",
        "alert_done": u"Model health report generated.\n\nNo model changes were made.\n\nIssues counted: {0}\n\n{1}",
        "failed_title": u"# Model Health Report failed",
        "failed_alert": u"Model Health Report failed. See pyRevit output for details.",
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


def get_param_as_text(element, built_in_param):
    try:
        param = element.get_Parameter(built_in_param)
        if not param:
            return u""
        return safe_text(param.AsValueString() or param.AsString() or param.AsDouble() or param.AsInteger())
    except Exception:
        return u""


def is_blank(value):
    return safe_text(value).strip() == u""


def collect_rooms():
    rooms = []
    collector = FilteredElementCollector(doc).OfCategory(
        BuiltInCategory.OST_Rooms
    ).WhereElementIsNotElementType()
    for element in collector.ToElements():
        if isinstance(element, Room):
            rooms.append(element)
    return rooms


def collect_family_instances_by_category(built_in_category):
    return list(
        FilteredElementCollector(doc)
        .OfCategory(built_in_category)
        .WhereElementIsNotElementType()
        .ToElements()
    )


def check_rooms():
    rooms = collect_rooms()
    missing_number = []
    missing_name = []
    duplicate_map = {}

    for room in rooms:
        number = get_param_as_text(room, BuiltInParameter.ROOM_NUMBER)
        name = get_param_as_text(room, BuiltInParameter.ROOM_NAME)

        if is_blank(number):
            missing_number.append(room)
        else:
            duplicate_map.setdefault(number, []).append(room)

        if is_blank(name):
            missing_name.append(room)

    duplicate_numbers = {}
    for number in duplicate_map:
        if len(duplicate_map[number]) > 1:
            duplicate_numbers[number] = duplicate_map[number]

    return {
        "total": len(rooms),
        "missing_number": missing_number,
        "missing_name": missing_name,
        "duplicate_numbers": duplicate_numbers,
    }


def check_marks(category, built_in_category):
    elements = collect_family_instances_by_category(built_in_category)
    missing_mark = []
    for element in elements:
        mark = get_param_as_text(element, BuiltInParameter.ALL_MODEL_MARK)
        if is_blank(mark):
            missing_mark.append(element)
    return {
        "category": category,
        "total": len(elements),
        "missing_mark": missing_mark,
    }


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


def check_unplaced_views():
    placed_ids = get_placed_view_ids()
    views = FilteredElementCollector(doc).OfClass(View).ToElements()
    unplaced = []
    reportable_count = 0

    for view in views:
        if not is_reportable_view(view):
            continue
        reportable_count += 1
        if element_id_value(view.Id) not in placed_ids:
            unplaced.append(view)

    return {
        "reportable_total": reportable_count,
        "unplaced": unplaced,
    }


def format_element_list(elements, max_items, lang):
    lines = []
    count = 0
    for element in elements:
        if count >= max_items:
            break
        name = safe_text(getattr(element, "Name", u""))
        lines.append("- `{0}` {1}".format(element_id_value(element.Id), name))
        count += 1
    if len(elements) > max_items:
        lines.append(tr(lang, "more_items").format(len(elements) - max_items))
    if not lines:
        lines.append(tr(lang, "none"))
    return lines


def write_report(path, lines):
    with codecs.open(path, "w", "utf-8-sig") as stream:
        stream.write(u"\n".join(lines))


def build_report(lang):
    app = doc.Application
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    room_result = check_rooms()
    door_result = check_marks("Doors", BuiltInCategory.OST_Doors)
    window_result = check_marks("Windows", BuiltInCategory.OST_Windows)
    view_result = check_unplaced_views()

    issue_count = (
        len(room_result["missing_number"])
        + len(room_result["missing_name"])
        + len(room_result["duplicate_numbers"])
        + len(door_result["missing_mark"])
        + len(window_result["missing_mark"])
        + len(view_result["unplaced"])
    )

    lines = []
    lines.append(tr(lang, "report_title"))
    lines.append(u"")
    lines.append(tr(lang, "read_only_note"))
    lines.append(u"")
    lines.append(tr(lang, "document_info"))
    lines.append(u"")
    lines.append(tr(lang, "document").format(safe_text(doc.Title)))
    lines.append(tr(lang, "path").format(safe_text(doc.PathName)))
    lines.append(tr(lang, "revit").format(safe_text(app.VersionName), safe_text(app.VersionNumber)))
    lines.append(tr(lang, "exported_at").format(timestamp))
    lines.append(tr(lang, "issue_count").format(issue_count))
    lines.append(u"")
    lines.append(tr(lang, "room_check"))
    lines.append(u"")
    lines.append(tr(lang, "room_total").format(room_result["total"]))
    lines.append(tr(lang, "room_missing_number").format(len(room_result["missing_number"])))
    lines.append(tr(lang, "room_missing_name").format(len(room_result["missing_name"])))
    lines.append(tr(lang, "room_duplicate_groups").format(len(room_result["duplicate_numbers"])))
    lines.append(u"")
    lines.append(tr(lang, "missing_room_numbers"))
    lines.extend(format_element_list(room_result["missing_number"], 30, lang))
    lines.append(u"")
    lines.append(tr(lang, "missing_room_names"))
    lines.extend(format_element_list(room_result["missing_name"], 30, lang))
    lines.append(u"")
    lines.append(tr(lang, "duplicate_room_numbers"))
    if room_result["duplicate_numbers"]:
        for number in sorted(room_result["duplicate_numbers"].keys()):
            ids = [element_id_value(room.Id) for room in room_result["duplicate_numbers"][number]]
            lines.append(u"- `{0}`: {1}".format(number, u", ".join(ids)))
    else:
        lines.append(tr(lang, "none"))
    lines.append(u"")
    lines.append(tr(lang, "door_window_check"))
    lines.append(u"")
    lines.append(tr(lang, "door_total").format(door_result["total"]))
    lines.append(tr(lang, "door_missing").format(len(door_result["missing_mark"])))
    lines.append(tr(lang, "window_total").format(window_result["total"]))
    lines.append(tr(lang, "window_missing").format(len(window_result["missing_mark"])))
    lines.append(u"")
    lines.append(tr(lang, "missing_doors"))
    lines.extend(format_element_list(door_result["missing_mark"], 30, lang))
    lines.append(u"")
    lines.append(tr(lang, "missing_windows"))
    lines.extend(format_element_list(window_result["missing_mark"], 30, lang))
    lines.append(u"")
    lines.append(tr(lang, "view_check"))
    lines.append(u"")
    lines.append(tr(lang, "view_total").format(view_result["reportable_total"]))
    lines.append(tr(lang, "view_unplaced").format(len(view_result["unplaced"])))
    lines.append(u"")
    lines.append(tr(lang, "unplaced_views"))
    lines.extend(format_element_list(view_result["unplaced"], 50, lang))
    lines.append(u"")
    lines.append(tr(lang, "next_steps"))
    lines.append(u"")
    lines.append(tr(lang, "next_step_1"))
    lines.append(tr(lang, "next_step_2"))
    lines.append(tr(lang, "next_step_3"))

    return lines, issue_count


def main():
    lang = choose_language()

    if doc is None:
        forms.alert(tr(lang, "no_doc"), title=tr(lang, "alert_title"))
        return

    export_dir = get_export_dir()
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_path = os.path.join(export_dir, "model_health_report_{0}.md".format(timestamp))

    lines, issue_count = build_report(lang)
    write_report(report_path, lines)

    output.print_md(tr(lang, "output_title"))
    output.print_md("")
    output.print_md(tr(lang, "output_done"))
    output.print_md("")
    output.print_md(tr(lang, "output_issues").format(issue_count))
    output.print_md(tr(lang, "output_report").format(report_path))

    forms.alert(
        tr(lang, "alert_done").format(
            issue_count,
            report_path,
        ),
        title=tr(lang, "alert_title"),
    )


try:
    main()
except Exception:
    err = traceback.format_exc()
    output.print_md(TEXT["zh"]["failed_title"] + u" / " + TEXT["en"]["failed_title"].replace("# ", u""))
    output.print_md("```text\n{0}\n```".format(err))
    forms.alert(TEXT["zh"]["failed_alert"] + u"\n\n" + TEXT["en"]["failed_alert"], title="Yang Agent")
