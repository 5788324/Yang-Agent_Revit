# -*- coding: utf-8 -*-
"""Preview rooms missing numbers in read-only dry-run mode."""

from __future__ import print_function

import codecs
import csv
import os
import traceback
from datetime import datetime

import clr

clr.AddReference("RevitAPI")
clr.AddReference("RevitAPIUI")

from Autodesk.Revit.DB import BuiltInCategory, BuiltInParameter, FilteredElementCollector  # noqa: E402
from Autodesk.Revit.DB.Architecture import Room  # noqa: E402
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
        "report_title": u"# Yang Agent 预览房间缺失编号",
        "read_only_note": u"这是 dry-run 只读预览，不会修改 Revit 模型。",
        "summary_heading": u"统计摘要",
        "document": u"文档：{0}",
        "exported_at": u"导出时间：{0}",
        "rooms_total": u"房间总数：{0}",
        "missing_total": u"缺失编号房间数量：{0}",
        "detail_heading": u"缺失编号房间明细",
        "suggested": u"建议编号",
        "next_steps_heading": u"建议下一步",
        "next_step_1": u"先核对这些房间是否允许自动补号，避免覆盖项目既有编号逻辑。",
        "next_step_2": u"确认楼层和房间名称后，再决定是否生成 apply 工具。",
        "next_step_3": u"正式写入前必须复核每个 ElementId 和建议编号。",
        "none": u"无",
        "output_title": u"# Yang Agent 预览房间缺失编号",
        "output_done": u"预览完成。该工具未修改模型。",
        "output_missing": u"- 缺失编号房间数量：{0}",
        "output_report": u"- 报告：`{0}`",
        "output_csv": u"- CSV：`{0}`",
        "alert_done": u"房间缺失编号预览已生成。\n\n该工具未修改模型。\n\n缺失编号房间数量：{0}\n\n{1}",
        "failed_title": u"# 房间缺失编号预览失败",
        "failed_alert": u"房间缺失编号预览失败。请查看 pyRevit 输出窗口。",
    },
    "en": {
        "language_message": u"Select report language / 选择报告语言",
        "alert_title": u"Yang Agent",
        "no_doc": u"No active Revit document.",
        "report_title": u"# Yang Agent Missing Room Numbers Preview",
        "read_only_note": u"This is a dry-run read-only preview. No Revit model changes were made.",
        "summary_heading": u"Summary",
        "document": u"Document: {0}",
        "exported_at": u"Exported at: {0}",
        "rooms_total": u"Total rooms: {0}",
        "missing_total": u"Rooms missing numbers: {0}",
        "detail_heading": u"Missing Room Number Details",
        "suggested": u"Suggested number",
        "next_steps_heading": u"Suggested Next Steps",
        "next_step_1": u"Verify whether these rooms are allowed to be auto-numbered before any write-back.",
        "next_step_2": u"Confirm level and room name context before generating an apply tool.",
        "next_step_3": u"Review every ElementId and suggested number before formal write-back.",
        "none": u"None",
        "output_title": u"# Yang Agent Missing Room Numbers Preview",
        "output_done": u"Preview completed. No model changes were made.",
        "output_missing": u"- Rooms missing numbers: {0}",
        "output_report": u"- Report: `{0}`",
        "output_csv": u"- CSV: `{0}`",
        "alert_done": u"Missing room numbers preview generated.\n\nNo model changes were made.\n\nRooms missing numbers: {0}\n\n{1}",
        "failed_title": u"# Missing Room Numbers Preview failed",
        "failed_alert": u"Missing Room Numbers Preview failed. See pyRevit output for details.",
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


def is_blank(value):
    return safe_text(value).strip() == u""


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


def get_level_name(room):
    try:
        level = doc.GetElement(room.LevelId)
        if level is not None:
            return safe_text(level.Name)
    except Exception:
        pass
    return u""


def collect_rooms():
    rows = []
    collector = (
        FilteredElementCollector(doc)
        .OfCategory(BuiltInCategory.OST_Rooms)
        .WhereElementIsNotElementType()
    )
    for element in collector.ToElements():
        if not isinstance(element, Room):
            continue
        rows.append(
            {
                "element_id": element_id_value(element.Id),
                "category": "Room",
                "level_name": get_level_name(element),
                "room_name": get_param_as_text(element, BuiltInParameter.ROOM_NAME),
                "current_number": get_param_as_text(element, BuiltInParameter.ROOM_NUMBER),
            }
        )
    return rows


def build_suggested_number(row, index):
    level_name = safe_text(row.get("level_name")).replace(" ", "").replace("-", "")
    if level_name:
        return "{0}-{1:03d}".format(level_name, index)
    return "R-{0:03d}".format(index)


def collect_preview_rows():
    rooms = collect_rooms()
    missing = []
    missing_index = 1
    for row in rooms:
        if is_blank(row.get("current_number")):
            row["suggested_number"] = build_suggested_number(row, missing_index)
            row["dry_run"] = "true"
            row["status"] = "MissingNumber"
            missing.append(row)
            missing_index += 1
    return len(rooms), missing


def build_report_lines(lang, room_count, missing):
    theme_id = get_theme_id()
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    summary_lines = [
        tr(lang, "document").format(safe_text(doc.Title)),
        tr(lang, "exported_at").format(timestamp),
        tr(lang, "rooms_total").format(room_count),
        tr(lang, "missing_total").format(len(missing)),
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

    if not missing:
        lines.append(u"- {0}".format(tr(lang, "none")))
    else:
        for row in missing:
            lines.append(
                u"- ElementId `{0}` | {1} | {2} | {3}: `{4}`".format(
                    row["element_id"],
                    row["level_name"] or tr(lang, "none"),
                    row["room_name"] or tr(lang, "none"),
                    tr(lang, "suggested"),
                    row["suggested_number"],
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
        "level_name",
        "room_name",
        "current_number",
        "suggested_number",
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
    report_path = os.path.join(export_dir, "missing_room_numbers_{0}.md".format(timestamp))
    csv_path = os.path.join(export_dir, "missing_room_numbers_{0}.csv".format(timestamp))

    room_count, missing = collect_preview_rows()
    write_markdown(report_path, build_report_lines(lang, room_count, missing))
    write_csv(csv_path, missing)

    output.print_md(tr(lang, "output_title"))
    output.print_md(u"")
    output.print_md(tr(lang, "output_done"))
    output.print_md(tr(lang, "output_missing").format(len(missing)))
    output.print_md(tr(lang, "output_report").format(report_path))
    output.print_md(tr(lang, "output_csv").format(csv_path))

    forms.toast(
        tr(lang, "alert_done").format(len(missing), report_path),
        title=tr(lang, "alert_title"),
    )


try:
    main()
except Exception:
    err = traceback.format_exc()
    output.print_md(TEXT["zh"]["failed_title"] + u" / " + TEXT["en"]["failed_title"].replace("# ", u""))
    output.print_md("```text\n{0}\n```".format(err))
    forms.alert(TEXT["zh"]["failed_alert"] + u"\n\n" + TEXT["en"]["failed_alert"], title="Yang Agent")
