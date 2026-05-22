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


doc = revit.doc
output = script.get_output()


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


def get_desktop_export_dir():
    desktop = os.path.join(os.path.expanduser("~"), "Desktop")
    if not os.path.isdir(desktop):
        desktop = os.path.expanduser("~")
    export_dir = os.path.join(desktop, "YangAgent_Revit_Exports")
    if not os.path.isdir(export_dir):
        os.makedirs(export_dir)
    return export_dir


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


def format_element_list(elements, max_items):
    lines = []
    count = 0
    for element in elements:
        if count >= max_items:
            break
        name = safe_text(getattr(element, "Name", u""))
        lines.append("- `{0}` {1}".format(element_id_value(element.Id), name))
        count += 1
    if len(elements) > max_items:
        lines.append("- ...还有 {0} 项未显示".format(len(elements) - max_items))
    if not lines:
        lines.append("- 无")
    return lines


def write_report(path, lines):
    with codecs.open(path, "w", "utf-8-sig") as stream:
        stream.write(u"\n".join(lines))


def build_report():
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
    lines.append(u"# Yang Agent Model Health Report")
    lines.append(u"")
    lines.append(u"此报告为只读检查结果，未修改 Revit 模型。")
    lines.append(u"")
    lines.append(u"## 文档信息")
    lines.append(u"")
    lines.append(u"- 文档：{0}".format(safe_text(doc.Title)))
    lines.append(u"- 路径：{0}".format(safe_text(doc.PathName)))
    lines.append(u"- Revit：{0} ({1})".format(safe_text(app.VersionName), safe_text(app.VersionNumber)))
    lines.append(u"- 导出时间：{0}".format(timestamp))
    lines.append(u"- 问题计数：{0}".format(issue_count))
    lines.append(u"")
    lines.append(u"## 房间检查")
    lines.append(u"")
    lines.append(u"- 房间总数：{0}".format(room_result["total"]))
    lines.append(u"- 缺少编号：{0}".format(len(room_result["missing_number"])))
    lines.append(u"- 缺少名称：{0}".format(len(room_result["missing_name"])))
    lines.append(u"- 重复编号组：{0}".format(len(room_result["duplicate_numbers"])))
    lines.append(u"")
    lines.append(u"### 缺少编号的房间")
    lines.extend(format_element_list(room_result["missing_number"], 30))
    lines.append(u"")
    lines.append(u"### 缺少名称的房间")
    lines.extend(format_element_list(room_result["missing_name"], 30))
    lines.append(u"")
    lines.append(u"### 重复房间编号")
    if room_result["duplicate_numbers"]:
        for number in sorted(room_result["duplicate_numbers"].keys()):
            ids = [element_id_value(room.Id) for room in room_result["duplicate_numbers"][number]]
            lines.append(u"- `{0}`: {1}".format(number, u", ".join(ids)))
    else:
        lines.append(u"- 无")
    lines.append(u"")
    lines.append(u"## 门窗标记检查")
    lines.append(u"")
    lines.append(u"- 门总数：{0}".format(door_result["total"]))
    lines.append(u"- 门缺少标记：{0}".format(len(door_result["missing_mark"])))
    lines.append(u"- 窗总数：{0}".format(window_result["total"]))
    lines.append(u"- 窗缺少标记：{0}".format(len(window_result["missing_mark"])))
    lines.append(u"")
    lines.append(u"### 缺少标记的门")
    lines.extend(format_element_list(door_result["missing_mark"], 30))
    lines.append(u"")
    lines.append(u"### 缺少标记的窗")
    lines.extend(format_element_list(window_result["missing_mark"], 30))
    lines.append(u"")
    lines.append(u"## 视图上图检查")
    lines.append(u"")
    lines.append(u"- 可检查视图总数：{0}".format(view_result["reportable_total"]))
    lines.append(u"- 可能未放置到图纸的视图：{0}".format(len(view_result["unplaced"])))
    lines.append(u"")
    lines.append(u"### 可能未上图视图")
    lines.extend(format_element_list(view_result["unplaced"], 50))
    lines.append(u"")
    lines.append(u"## 建议下一步")
    lines.append(u"")
    lines.append(u"1. 把此报告交给 Codex 或 Claude 分析。")
    lines.append(u"2. 先人工确认问题是否符合公司标准。")
    lines.append(u"3. 再为单一问题生成 dry-run 修复脚本。")

    return lines, issue_count


def main():
    if doc is None:
        forms.alert("No active Revit document.", title="Yang Agent")
        return

    export_dir = get_desktop_export_dir()
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_path = os.path.join(export_dir, "model_health_report_{0}.md".format(timestamp))

    lines, issue_count = build_report()
    write_report(report_path, lines)

    output.print_md("# Yang Agent Model Health Report")
    output.print_md("")
    output.print_md("Report completed. No model changes were made.")
    output.print_md("")
    output.print_md("- Issues counted: {0}".format(issue_count))
    output.print_md("- Report: `{0}`".format(report_path))

    forms.alert(
        "Model health report generated.\n\nNo model changes were made.\n\nIssues counted: {0}\n\n{1}".format(
            issue_count,
            report_path,
        ),
        title="Yang Agent",
    )


try:
    main()
except Exception:
    err = traceback.format_exc()
    output.print_md("# Model Health Report failed")
    output.print_md("```text\n{0}\n```".format(err))
    forms.alert("Model Health Report failed. See pyRevit output for details.", title="Yang Agent")
