# -*- coding: utf-8 -*-
"""Export a read-only Revit model snapshot package."""

from __future__ import print_function

import codecs
import csv
import json
import os
import traceback
from datetime import datetime

import clr

clr.AddReference("RevitAPI")
clr.AddReference("RevitAPIUI")

from Autodesk.Revit.DB import (
    BuiltInCategory,
    BuiltInParameter,
    CategoryType,
    FilteredElementCollector,
    Level,
    StorageType,
    View,
    ViewSheet,
)
from Autodesk.Revit.DB.Architecture import Room
from pyrevit import forms, revit, script
from yang_agent_lang import get_or_choose_language
from yang_agent_report_style import build_intro_block, build_status_block
from yang_agent_settings import get_export_dir
from yang_agent_theme import get_theme_id


doc = revit.doc
output = script.get_output()


TEXT = {
    "zh": {
        "language_message": u"选择报告语言 / Select report language",
        "alert_title": u"Yang Agent",
        "no_doc": u"没有打开的 Revit 文档。",
        "report_title": u"# Yang Agent 模型快照导出",
        "read_only_note": u"此工具导出只读模型快照，未修改 Revit 模型。",
        "document_info": u"## 文档信息",
        "document": u"- 文档：{0}",
        "path": u"- 路径：{0}",
        "revit": u"- Revit：{0} ({1})",
        "exported_at": u"- 导出时间：{0}",
        "summary_title": u"导出摘要",
        "levels": u"- 标高：{0}",
        "rooms": u"- 房间：{0}",
        "doors_windows": u"- 门窗：{0}",
        "sheets_views": u"- 图纸和视图：{0}",
        "categories": u"- 模型类别：{0}",
        "files": u"## 输出文件",
        "output_title": u"# Yang Agent 模型快照导出",
        "output_done": u"模型快照导出完成。此工具未修改模型。",
        "output_report": u"- 摘要报告：`{0}`",
        "output_json": u"- JSON：`{0}`",
        "output_csv": u"- CSV：`{0}`",
        "alert_done": u"模型快照已导出。\n\n此工具未修改模型。\n\n{0}",
        "failed_title": u"# 模型快照导出失败",
        "failed_alert": u"模型快照导出失败。请查看 pyRevit 输出窗口。",
    },
    "en": {
        "language_message": u"Select report language / 选择报告语言",
        "alert_title": u"Yang Agent",
        "no_doc": u"No active Revit document.",
        "report_title": u"# Yang Agent Export Model Snapshot",
        "read_only_note": u"This tool exports a read-only model snapshot. No Revit model changes were made.",
        "document_info": u"## Document Info",
        "document": u"- Document: {0}",
        "path": u"- Path: {0}",
        "revit": u"- Revit: {0} ({1})",
        "exported_at": u"- Exported at: {0}",
        "summary_title": u"Export Summary",
        "levels": u"- Levels: {0}",
        "rooms": u"- Rooms: {0}",
        "doors_windows": u"- Doors and windows: {0}",
        "sheets_views": u"- Sheets and views: {0}",
        "categories": u"- Model categories: {0}",
        "files": u"## Output Files",
        "output_title": u"# Yang Agent Export Model Snapshot",
        "output_done": u"Model snapshot export completed. No model changes were made.",
        "output_report": u"- Summary report: `{0}`",
        "output_json": u"- JSON: `{0}`",
        "output_csv": u"- CSV: `{0}`",
        "alert_done": u"Model snapshot exported.\n\nNo model changes were made.\n\n{0}",
        "failed_title": u"# Export Model Snapshot failed",
        "failed_alert": u"Export Model Snapshot failed. See pyRevit output for details.",
    },
}


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


def choose_language():
    try:
        return get_or_choose_language(forms, message=TEXT["zh"]["language_message"])
    except Exception:
        return "zh"


def element_id_value(element_id):
    if element_id is None:
        return None
    try:
        return element_id.IntegerValue
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
        return get_param_text(element.get_Parameter(built_in_param))
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


def get_element_name(element):
    if element is None:
        return u""
    try:
        return safe_text(element.Name)
    except Exception:
        pass
    try:
        param = element.get_Parameter(BuiltInParameter.SYMBOL_NAME_PARAM)
        return get_param_text(param)
    except Exception:
        pass
    return u""


def get_family_name(symbol):
    if symbol is None:
        return u""
    try:
        return safe_text(symbol.FamilyName)
    except Exception:
        pass
    try:
        return safe_text(symbol.Family.Name)
    except Exception:
        pass
    try:
        param = symbol.get_Parameter(BuiltInParameter.SYMBOL_FAMILY_NAME_PARAM)
        return get_param_text(param)
    except Exception:
        pass
    return u""


def write_json(path, data):
    text = json.dumps(data, ensure_ascii=False, indent=2)
    with codecs.open(path, "w", "utf-8-sig") as stream:
        stream.write(text)


def write_markdown(path, lines):
    with codecs.open(path, "w", "utf-8-sig") as stream:
        stream.write(u"\n".join(lines))


def write_csv(path, rows, fieldnames):
    with open(path, "wb") as raw_stream:
        raw_stream.write(codecs.BOM_UTF8)
        writer = csv.DictWriter(raw_stream, fieldnames=fieldnames)
        header = {}
        for field in fieldnames:
            header[field] = field.encode("utf-8")
        writer.writerow(header)
        for row in rows:
            encoded_row = {}
            for field in fieldnames:
                encoded_row[field] = safe_text(row.get(field, u"")).encode("utf-8")
            writer.writerow(encoded_row)


def collect_document_info():
    app = doc.Application
    active_view = doc.ActiveView
    return {
        "title": safe_text(doc.Title),
        "path_name": safe_text(doc.PathName),
        "is_workshared": bool(doc.IsWorkshared),
        "is_family_document": bool(doc.IsFamilyDocument),
        "revit_version_name": safe_text(app.VersionName),
        "revit_version_number": safe_text(app.VersionNumber),
        "active_view": {
            "id": element_id_value(active_view.Id) if active_view else None,
            "name": safe_text(active_view.Name) if active_view else u"",
            "view_type": safe_text(active_view.ViewType) if active_view else u"",
        },
        "exported_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    }


def collect_levels():
    levels = []
    for level in FilteredElementCollector(doc).OfClass(Level).ToElements():
        levels.append({
            "id": element_id_value(level.Id),
            "name": safe_text(level.Name),
            "elevation_internal_ft": safe_text(level.Elevation),
            "elevation_mm": safe_text(round(level.Elevation * 304.8, 3)),
        })
    levels.sort(key=lambda item: float(item.get("elevation_internal_ft") or 0))
    return levels


def collect_rooms():
    rows = []
    collector = FilteredElementCollector(doc).OfCategory(
        BuiltInCategory.OST_Rooms
    ).WhereElementIsNotElementType()
    for room in collector.ToElements():
        if not isinstance(room, Room):
            continue
        level = None
        try:
            level = doc.GetElement(room.LevelId)
        except Exception:
            level = None
        area_internal = 0.0
        try:
            area_param = room.get_Parameter(BuiltInParameter.ROOM_AREA)
            if area_param is not None:
                area_internal = area_param.AsDouble()
        except Exception:
            area_internal = 0.0
        rows.append({
            "element_id": safe_text(element_id_value(room.Id)),
            "number": get_param_as_text(room, BuiltInParameter.ROOM_NUMBER),
            "name": get_param_as_text(room, BuiltInParameter.ROOM_NAME),
            "level_id": safe_text(element_id_value(room.LevelId)),
            "level_name": safe_text(level.Name if level else u""),
            "area_sqm": safe_text(round(area_internal * 0.09290304, 3)),
            "department": get_param_text(get_lookup_param(room, [u"部门", "Department"])),
            "comments": get_param_as_text(room, BuiltInParameter.ALL_MODEL_INSTANCE_COMMENTS),
        })
    return rows


def collect_doors_windows():
    rows = []
    category_pairs = [
        (BuiltInCategory.OST_Doors, "Door"),
        (BuiltInCategory.OST_Windows, "Window"),
    ]
    for built_in_category, category_name in category_pairs:
        collector = FilteredElementCollector(doc).OfCategory(
            built_in_category
        ).WhereElementIsNotElementType()
        for element in collector.ToElements():
            level_name = u""
            family_name = u""
            type_name = u""
            try:
                level = doc.GetElement(element.LevelId)
                if level is not None:
                    level_name = safe_text(level.Name)
            except Exception:
                pass
            try:
                symbol = doc.GetElement(element.GetTypeId())
                if symbol is not None:
                    type_name = get_element_name(symbol)
                    family_name = get_family_name(symbol)
            except Exception:
                pass
            rows.append({
                "element_id": safe_text(element_id_value(element.Id)),
                "category": category_name,
                "family_name": family_name,
                "type_name": type_name,
                "level_name": level_name,
                "mark": get_mark_as_text(element),
                "comments": get_param_as_text(element, BuiltInParameter.ALL_MODEL_INSTANCE_COMMENTS),
            })
    return rows


def collect_sheets_views():
    rows = []
    for sheet in FilteredElementCollector(doc).OfClass(ViewSheet).ToElements():
        rows.append({
            "kind": "Sheet",
            "element_id": safe_text(element_id_value(sheet.Id)),
            "number": safe_text(sheet.SheetNumber),
            "name": safe_text(sheet.Name),
            "view_type": u"",
            "is_template": u"",
        })
    for view in FilteredElementCollector(doc).OfClass(View).ToElements():
        if isinstance(view, ViewSheet):
            continue
        rows.append({
            "kind": "View",
            "element_id": safe_text(element_id_value(view.Id)),
            "number": u"",
            "name": safe_text(view.Name),
            "view_type": safe_text(view.ViewType),
            "is_template": safe_text(view.IsTemplate),
        })
    return rows


def collect_category_summary():
    summary = {}
    collector = FilteredElementCollector(doc).WhereElementIsNotElementType()
    for element in collector.ToElements():
        try:
            category = element.Category
            if category is None:
                continue
            if category.CategoryType != CategoryType.Model:
                continue
            name = safe_text(category.Name)
            summary[name] = summary.get(name, 0) + 1
        except Exception:
            continue
    rows = []
    for name in sorted(summary.keys()):
        rows.append({"category": name, "count": summary[name]})
    return rows


def build_summary_lines(lang, document_info, counts, paths):
    theme_id = get_theme_id()

    def status_text(value):
        text = safe_text(value)
        if text.startswith(u"- "):
            return text[2:]
        return text

    lines = []
    lines.append(build_intro_block(theme_id, tr(lang, "report_title"), tr(lang, "read_only_note")))
    lines.append(u"")
    lines.append(tr(lang, "document_info"))
    lines.append(u"")
    lines.append(tr(lang, "document").format(document_info.get("title")))
    lines.append(tr(lang, "path").format(document_info.get("path_name")))
    lines.append(tr(lang, "revit").format(document_info.get("revit_version_name"), document_info.get("revit_version_number")))
    lines.append(tr(lang, "exported_at").format(document_info.get("exported_at")))
    lines.append(u"")
    lines.append(build_status_block(
        theme_id,
        tr(lang, "summary_title"),
        [
            status_text(tr(lang, "levels").format(counts.get("levels"))),
            status_text(tr(lang, "rooms").format(counts.get("rooms"))),
            status_text(tr(lang, "doors_windows").format(counts.get("doors_windows"))),
            status_text(tr(lang, "sheets_views").format(counts.get("sheets_views"))),
            status_text(tr(lang, "categories").format(counts.get("model_categories"))),
        ],
    ))
    lines.append(u"")
    lines.append(tr(lang, "files"))
    lines.append(u"")
    lines.append(tr(lang, "output_json").format(paths["json"]))
    for csv_path in paths["csvs"]:
        lines.append(tr(lang, "output_csv").format(csv_path))
    return lines


def main():
    lang = choose_language()
    if doc is None:
        forms.alert(tr(lang, "no_doc"), title=tr(lang, "alert_title"))
        return

    export_dir = get_export_dir()
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    document_info = collect_document_info()
    levels = collect_levels()
    rooms = collect_rooms()
    doors_windows = collect_doors_windows()
    sheets_views = collect_sheets_views()
    category_summary = collect_category_summary()

    counts = {
        "levels": len(levels),
        "rooms": len(rooms),
        "doors_windows": len(doors_windows),
        "sheets_views": len(sheets_views),
        "model_categories": len(category_summary),
    }
    snapshot = {
        "document": document_info,
        "counts": counts,
        "levels": levels,
        "rooms": rooms,
        "doors_windows": doors_windows,
        "sheets_views": sheets_views,
        "category_summary": category_summary,
    }

    summary_path = os.path.join(export_dir, "model_snapshot_report_{0}.md".format(timestamp))
    json_path = os.path.join(export_dir, "model_snapshot_{0}.json".format(timestamp))
    rooms_csv_path = os.path.join(export_dir, "rooms_{0}.csv".format(timestamp))
    doors_windows_csv_path = os.path.join(export_dir, "doors_windows_{0}.csv".format(timestamp))
    sheets_views_csv_path = os.path.join(export_dir, "sheets_views_{0}.csv".format(timestamp))

    write_json(json_path, snapshot)
    write_csv(
        rooms_csv_path,
        rooms,
        ["element_id", "number", "name", "level_id", "level_name", "area_sqm", "department", "comments"],
    )
    write_csv(
        doors_windows_csv_path,
        doors_windows,
        ["element_id", "category", "family_name", "type_name", "level_name", "mark", "comments"],
    )
    write_csv(
        sheets_views_csv_path,
        sheets_views,
        ["kind", "element_id", "number", "name", "view_type", "is_template"],
    )
    lines = build_summary_lines(
        lang,
        document_info,
        counts,
        {
            "json": json_path,
            "csvs": [rooms_csv_path, doors_windows_csv_path, sheets_views_csv_path],
        },
    )
    write_markdown(summary_path, lines)

    output.print_md(tr(lang, "output_title"))
    output.print_md(u"")
    output.print_md(tr(lang, "output_done"))
    output.print_md(tr(lang, "output_report").format(summary_path))
    output.print_md(tr(lang, "output_json").format(json_path))
    output.print_md(tr(lang, "output_csv").format(rooms_csv_path))
    output.print_md(tr(lang, "output_csv").format(doors_windows_csv_path))
    output.print_md(tr(lang, "output_csv").format(sheets_views_csv_path))

    forms.toast(tr(lang, "alert_done").format(export_dir), title=tr(lang, "alert_title"))


try:
    main()
except Exception:
    err = traceback.format_exc()
    output.print_md(TEXT["zh"]["failed_title"] + u" / " + TEXT["en"]["failed_title"].replace("# ", u""))
    output.print_md("```text\n{0}\n```".format(err))
    forms.alert(TEXT["zh"]["failed_alert"] + u"\n\n" + TEXT["en"]["failed_alert"], title="Yang Agent")
