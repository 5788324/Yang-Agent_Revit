# -*- coding: utf-8 -*-
"""Generate a read-only Revit model health report."""

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
    StorageType,
    View,
    ViewSheet,
)
from Autodesk.Revit.DB.Architecture import Room  # noqa: E402
from pyrevit import forms, revit, script  # noqa: E402
from yang_agent_lang import get_or_choose_language, get_view_naming_rules  # noqa: E402
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
        "report_title": u"# Yang Agent 模型健康报告",
        "read_only_note": u"这是只读检查报告，不会修改 Revit 模型。",
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
        "room_duplicate_groups": u"- 重复编号组数：{0}",
        "missing_room_numbers": u"### 缺少编号的房间",
        "missing_room_names": u"### 缺少名称的房间",
        "duplicate_room_numbers": u"### 重复房间编号",
        "door_window_check": u"## 门窗标记检查",
        "door_total": u"- 门总数：{0}",
        "door_missing": u"- 缺少标记的门：{0}",
        "window_total": u"- 窗总数：{0}",
        "window_missing": u"- 缺少标记的窗：{0}",
        "missing_doors": u"### 缺少标记的门",
        "missing_windows": u"### 缺少标记的窗",
        "view_check": u"## 视图上图检查",
        "view_total": u"- 可检查视图总数：{0}",
        "view_unplaced": u"- 可能未放到图纸的视图：{0}",
        "unplaced_views": u"### 可能未上图的视图",
        "view_naming_check": u"## 视图命名检查",
        "view_naming_total": u"- 纳入检查的视图：{0}",
        "view_naming_blank": u"- 空白名称：{0}",
        "view_naming_temp": u"- 含临时关键词：{0}",
        "view_naming_prefix": u"- 缺少推荐前缀：{0}",
        "view_naming_detail": u"### 命名问题明细",
        "naming_blank_label": u"空白名称",
        "naming_temp_label": u"临时关键词",
        "naming_prefix_label": u"缺少推荐前缀",
        "risk_notes": u"## 风险提示",
        "risk_none": u"未检测到高风险项。",
        "risk_high": u"高风险：以下类别的问题数量较高，建议优先处理：",
        "risk_unplaced_high": u"未上图视图 ({0} 个)：可能导致图纸缺失。",
        "risk_missing_marks_high": u"门窗缺少标记 ({0} 个)：可能影响明细表统计。",
        "risk_missing_rooms_high": u"房间缺少编号 ({0} 个)：可能影响面积统计和图纸标注。",
        "risk_duplicate_rooms_high": u"房间编号重复 ({0} 组)：会导致面积和统计错误。",
        "risk_naming_issues_high": u"视图命名问题 ({0} 个)：可能导致视图管理混乱。",
        "next_steps": u"## 建议下一步",
        "next_step_1": u"1. 把这份报告交给 Codex 或 Claude 继续分析。",
        "next_step_2": u"2. 先人工确认这些问题是否真的违反当前标准。",
        "next_step_3": u"3. 只针对一种问题生成 dry-run 修复工具，再决定是否 apply。",
        "none": u"- 无",
        "more_items": u"- 还有 {0} 项未显示",
        "output_title": u"# Yang Agent 模型健康报告",
        "output_done": u"报告生成完成。本工具未修改模型。",
        "output_issues": u"- 问题计数：{0}",
        "output_report": u"- 报告：`{0}`",
        "alert_done": u"模型健康报告已生成。\n\n本工具未修改模型。\n\n问题计数：{0}\n\n{1}",
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
        "view_naming_check": u"## View Naming Check",
        "view_naming_total": u"- Views checked: {0}",
        "view_naming_blank": u"- Blank names: {0}",
        "view_naming_temp": u"- Temporary keywords: {0}",
        "view_naming_prefix": u"- Missing recommended prefix: {0}",
        "view_naming_detail": u"### Naming Issue Details",
        "naming_blank_label": u"Blank name",
        "naming_temp_label": u"Temporary keyword",
        "naming_prefix_label": u"Missing recommended prefix",
        "risk_notes": u"## Risk Notes",
        "risk_none": u"No high-risk items detected.",
        "risk_high": u"High risk: the following categories show elevated issue counts. Consider addressing these first:",
        "risk_unplaced_high": u"Unplaced views ({0}): may result in missing sheets.",
        "risk_missing_marks_high": u"Doors/windows missing marks ({0}): may affect schedule accuracy.",
        "risk_missing_rooms_high": u"Rooms missing numbers ({0}): may affect area calculations and annotation.",
        "risk_duplicate_rooms_high": u"Duplicate room numbers ({0} groups): may cause area and schedule errors.",
        "risk_naming_issues_high": u"View naming issues ({0}): may cause view management confusion.",
        "next_steps": u"## Suggested Next Steps",
        "next_step_1": u"1. Ask Codex or Claude to analyze this report.",
        "next_step_2": u"2. Confirm the findings against current standards.",
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


FALLBACK_TEMPORARY_KEYWORDS = [
    u"临时",
    u"测试",
    u"工作",
    u"复制",
    u"temp",
    u"test",
    u"working",
    u"copy",
]

RISK_THRESHOLD = 5


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


def get_param_text(param):
    if param is None:
        return u""
    try:
        storage_type = param.StorageType
    except Exception:
        storage_type = None
    if storage_type == StorageType.String:
        try:
            value = param.AsString()
            return safe_text(value) if value is not None else u""
        except Exception:
            return u""
    if storage_type == StorageType.Integer:
        try:
            return safe_text(param.AsInteger())
        except Exception:
            return u""
    if storage_type == StorageType.Double:
        try:
            return safe_text(param.AsDouble())
        except Exception:
            return u""
    try:
        value = param.AsString()
        if value is not None:
            return safe_text(value)
    except Exception:
        pass
    try:
        value = param.AsValueString()
        if value is not None:
            return safe_text(value)
    except Exception:
        pass
    return u""


def get_param_as_text(element, built_in_param):
    try:
        param = element.get_Parameter(built_in_param)
        if param is None:
            return u""
        return get_param_text(param)
    except Exception:
        return u""


def get_lookup_param(element, names):
    for name in names:
        try:
            param = element.LookupParameter(name)
            if param is not None:
                return param
        except Exception:
            continue
    return None


def get_mark_as_text(element):
    try:
        param = element.get_Parameter(BuiltInParameter.ALL_MODEL_MARK)
        if param is not None:
            return get_param_text(param)
    except Exception:
        pass
    return get_param_text(get_lookup_param(element, ["Mark", u"标记"]))


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


def check_marks(built_in_category):
    elements = collect_family_instances_by_category(built_in_category)
    missing_mark = []
    for element in elements:
        if is_blank(get_mark_as_text(element)):
            missing_mark.append(element)
    return {
        "total": len(elements),
        "missing_mark": missing_mark,
    }


def get_placed_view_ids():
    placed_ids = set()
    sheets = FilteredElementCollector(doc).OfClass(ViewSheet).ToElements()
    for sheet in sheets:
        try:
            for view_id in sheet.GetAllPlacedViews():
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
    return safe_text(view.ViewType) in allowed


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


def get_effective_view_naming_rules():
    rules = get_view_naming_rules()
    keywords = []
    seen = set()
    for keyword in list(rules.get("temporary_keywords", [])) + FALLBACK_TEMPORARY_KEYWORDS:
        text = safe_text(keyword).strip()
        lowered = text.lower()
        if text and lowered not in seen:
            keywords.append(text)
            seen.add(lowered)
    return {
        "prefix_by_view_type": rules.get("prefix_by_view_type", {}),
        "temporary_keywords": keywords,
    }


def is_namable_view(view, rules):
    if view is None:
        return False
    try:
        if view.IsTemplate:
            return False
    except Exception:
        return False
    if isinstance(view, ViewSheet):
        return False
    return safe_text(view.ViewType) in rules["prefix_by_view_type"]


def get_naming_issue(view_name, view_type, rules):
    name = safe_text(view_name).strip()
    if is_blank(name):
        return "BlankName", ""

    lowered = name.lower()
    for keyword in rules["temporary_keywords"]:
        keyword_text = safe_text(keyword).strip()
        if keyword_text and keyword_text.lower() in lowered:
            return "TemporaryKeyword", keyword_text

    prefixes = rules["prefix_by_view_type"].get(view_type, [])
    upper_name = name.upper()
    for prefix in prefixes:
        if upper_name.startswith(safe_text(prefix).upper()):
            return "", ""
    return "MissingRecommendedPrefix", u"|".join([safe_text(prefix) for prefix in prefixes])


def check_view_naming():
    rules = get_effective_view_naming_rules()
    issues_by_type = {
        "BlankName": [],
        "TemporaryKeyword": [],
        "MissingRecommendedPrefix": [],
    }
    reportable_count = 0

    views = FilteredElementCollector(doc).OfClass(View).ToElements()
    for view in views:
        if not is_namable_view(view, rules):
            continue
        reportable_count += 1

        view_type = safe_text(view.ViewType)
        view_name = safe_text(getattr(view, "Name", u""))
        issue_type, expected = get_naming_issue(view_name, view_type, rules)
        if not issue_type:
            continue

        issues_by_type[issue_type].append({
            "element_id": element_id_value(view.Id),
            "view_name": view_name,
            "view_type": view_type,
            "expected_rule": expected,
        })

    return {
        "reportable_total": reportable_count,
        "issues_by_type": issues_by_type,
    }


def get_naming_label(lang, issue_type):
    labels = {
        "BlankName": tr(lang, "naming_blank_label"),
        "TemporaryKeyword": tr(lang, "naming_temp_label"),
        "MissingRecommendedPrefix": tr(lang, "naming_prefix_label"),
    }
    return labels.get(issue_type, safe_text(issue_type))


def build_risk_notes(lang, room_result, door_result, window_result, view_result, naming_result):
    risks = []

    unplaced_count = len(view_result["unplaced"])
    if unplaced_count >= RISK_THRESHOLD:
        risks.append(tr(lang, "risk_unplaced_high").format(unplaced_count))

    missing_marks = len(door_result["missing_mark"]) + len(window_result["missing_mark"])
    if missing_marks >= RISK_THRESHOLD:
        risks.append(tr(lang, "risk_missing_marks_high").format(missing_marks))

    missing_rooms = len(room_result["missing_number"])
    if missing_rooms >= RISK_THRESHOLD:
        risks.append(tr(lang, "risk_missing_rooms_high").format(missing_rooms))

    duplicate_groups = len(room_result["duplicate_numbers"])
    if duplicate_groups > 0:
        risks.append(tr(lang, "risk_duplicate_rooms_high").format(duplicate_groups))

    naming_total = sum([len(items) for items in naming_result["issues_by_type"].values()])
    if naming_total >= RISK_THRESHOLD:
        risks.append(tr(lang, "risk_naming_issues_high").format(naming_total))

    if not risks:
        return [tr(lang, "risk_none")]
    return [tr(lang, "risk_high")] + risks


def format_element_list(elements, max_items, lang):
    lines = []
    count = 0
    for element in elements:
        if count >= max_items:
            break
        name = safe_text(getattr(element, "Name", u""))
        lines.append(u"- `{0}` {1}".format(element_id_value(element.Id), name))
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
    theme_id = get_theme_id()

    room_result = check_rooms()
    door_result = check_marks(BuiltInCategory.OST_Doors)
    window_result = check_marks(BuiltInCategory.OST_Windows)
    view_result = check_unplaced_views()
    naming_result = check_view_naming()
    naming_issue_total = sum([len(items) for items in naming_result["issues_by_type"].values()])

    issue_count = (
        len(room_result["missing_number"])
        + len(room_result["missing_name"])
        + len(room_result["duplicate_numbers"])
        + len(door_result["missing_mark"])
        + len(window_result["missing_mark"])
        + len(view_result["unplaced"])
        + naming_issue_total
    )

    lines = []
    lines.append(build_intro_block(theme_id, tr(lang, "report_title"), tr(lang, "read_only_note")))
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
    lines.append(tr(lang, "view_naming_check"))
    lines.append(u"")
    lines.append(tr(lang, "view_naming_total").format(naming_result["reportable_total"]))
    lines.append(tr(lang, "view_naming_blank").format(len(naming_result["issues_by_type"]["BlankName"])))
    lines.append(tr(lang, "view_naming_temp").format(len(naming_result["issues_by_type"]["TemporaryKeyword"])))
    lines.append(tr(lang, "view_naming_prefix").format(len(naming_result["issues_by_type"]["MissingRecommendedPrefix"])))
    lines.append(u"")
    lines.append(tr(lang, "view_naming_detail"))
    for issue_type in ["BlankName", "TemporaryKeyword", "MissingRecommendedPrefix"]:
        for item in naming_result["issues_by_type"][issue_type]:
            lines.append(
                u"- `{0}` {1} | {2} | `{3}`".format(
                    item["element_id"],
                    item["view_name"] or tr(lang, "none").lstrip("- ").strip(),
                    get_naming_label(lang, issue_type),
                    item["expected_rule"] or tr(lang, "none").lstrip("- ").strip(),
                )
            )
    if naming_issue_total == 0:
        lines.append(tr(lang, "none"))
    lines.append(u"")
    lines.append(
        build_status_block(
            theme_id,
            tr(lang, "risk_notes").replace("## ", ""),
            build_risk_notes(lang, room_result, door_result, window_result, view_result, naming_result),
        )
    )
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
    output.print_md(u"")
    output.print_md(tr(lang, "output_done"))
    output.print_md(u"")
    output.print_md(tr(lang, "output_issues").format(issue_count))
    output.print_md(tr(lang, "output_report").format(report_path))

    forms.toast(
        tr(lang, "alert_done").format(issue_count, report_path),
        title=tr(lang, "alert_title"),
    )


try:
    main()
except Exception:
    err = traceback.format_exc()
    output.print_md(TEXT["zh"]["failed_title"] + u" / " + TEXT["en"]["failed_title"].replace("# ", u""))
    output.print_md("```text\n{0}\n```".format(err))
    forms.alert(TEXT["zh"]["failed_alert"] + u"\n\n" + TEXT["en"]["failed_alert"], title="Yang Agent")
