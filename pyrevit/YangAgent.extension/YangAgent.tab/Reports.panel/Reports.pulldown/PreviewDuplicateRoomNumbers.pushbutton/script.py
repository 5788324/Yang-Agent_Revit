# -*- coding: utf-8 -*-
"""Preview duplicate room numbers in read-only dry-run mode."""

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
        "report_title": u"# Yang Agent 预览重复房间编号",
        "read_only_note": u"这是 dry-run 只读预览，不会修改 Revit 模型。",
        "summary_heading": u"统计摘要",
        "document": u"文档：{0}",
        "exported_at": u"导出时间：{0}",
        "rooms_total": u"房间总数：{0}",
        "duplicate_groups": u"重复编号组数：{0}",
        "duplicate_rooms": u"涉及房间数量：{0}",
        "detail_heading": u"重复房间编号明细",
        "number_label": u"房间编号",
        "next_steps_heading": u"建议下一步",
        "next_step_1": u"先核对这些重复编号是否属于设计意图，例如分区、镜像或阶段占位。",
        "next_step_2": u"确认公司房间编号规则后，再考虑生成修复预览或 apply 工具。",
        "next_step_3": u"不要在未核对 ElementId 和楼层的情况下直接批量重编号。",
        "none": u"无",
        "output_title": u"# Yang Agent 预览重复房间编号",
        "output_done": u"预览完成。该工具未修改模型。",
        "output_groups": u"- 重复编号组数：{0}",
        "output_rooms": u"- 涉及房间数量：{0}",
        "output_report": u"- 报告：`{0}`",
        "output_csv": u"- CSV：`{0}`",
        "alert_done": u"重复房间编号预览已生成。\n\n该工具未修改模型。\n\n重复编号组数：{0}\n涉及房间数量：{1}\n\n{2}",
        "failed_title": u"# 重复房间编号预览失败",
        "failed_alert": u"重复房间编号预览失败。请查看 pyRevit 输出窗口。",
    },
    "en": {
        "language_message": u"Select report language / 选择报告语言",
        "alert_title": u"Yang Agent",
        "no_doc": u"No active Revit document.",
        "report_title": u"# Yang Agent Duplicate Room Numbers Preview",
        "read_only_note": u"This is a dry-run read-only preview. No Revit model changes were made.",
        "summary_heading": u"Summary",
        "document": u"Document: {0}",
        "exported_at": u"Exported at: {0}",
        "rooms_total": u"Total rooms: {0}",
        "duplicate_groups": u"Duplicate number groups: {0}",
        "duplicate_rooms": u"Affected rooms: {0}",
        "detail_heading": u"Duplicate Room Number Details",
        "number_label": u"Room number",
        "next_steps_heading": u"Suggested Next Steps",
        "next_step_1": u"Verify whether these duplicates are intentional, such as zoning, mirroring, or phase placeholders.",
        "next_step_2": u"Confirm company room numbering rules before generating repair previews or apply tools.",
        "next_step_3": u"Do not bulk renumber before reviewing ElementId and level context.",
        "none": u"None",
        "output_title": u"# Yang Agent Duplicate Room Numbers Preview",
        "output_done": u"Preview completed. No model changes were made.",
        "output_groups": u"- Duplicate number groups: {0}",
        "output_rooms": u"- Affected rooms: {0}",
        "output_report": u"- Report: `{0}`",
        "output_csv": u"- CSV: `{0}`",
        "alert_done": u"Duplicate room numbers preview generated.\n\nNo model changes were made.\n\nDuplicate number groups: {0}\nAffected rooms: {1}\n\n{2}",
        "failed_title": u"# Duplicate Room Numbers Preview failed",
        "failed_alert": u"Duplicate Room Numbers Preview failed. See pyRevit output for details.",
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
                "room_number": get_param_as_text(element, BuiltInParameter.ROOM_NUMBER),
                "room_name": get_param_as_text(element, BuiltInParameter.ROOM_NAME),
                "level_name": get_level_name(element),
            }
        )
    return rows


def collect_duplicate_rows():
    rooms = collect_rooms()
    grouped = {}
    for row in rooms:
        number = safe_text(row.get("room_number")).strip()
        if is_blank(number):
            continue
        grouped.setdefault(number, []).append(row)

    duplicates = []
    group_count = 0
    for number in sorted(grouped.keys()):
        rows = grouped[number]
        if len(rows) < 2:
            continue
        group_count += 1
        for row in rows:
            row["dry_run"] = "true"
            row["duplicate_number"] = number
            row["duplicate_count"] = safe_text(len(rows))
            row["status"] = "Duplicate"
            duplicates.append(row)

    return len(rooms), group_count, duplicates


def build_report_lines(lang, room_count, group_count, duplicates):
    theme_id = get_theme_id()
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    summary_lines = [
        tr(lang, "document").format(safe_text(doc.Title)),
        tr(lang, "exported_at").format(timestamp),
        tr(lang, "rooms_total").format(room_count),
        tr(lang, "duplicate_groups").format(group_count),
        tr(lang, "duplicate_rooms").format(len(duplicates)),
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

    if not duplicates:
        lines.append(u"- {0}".format(tr(lang, "none")))
    else:
        current_number = None
        for row in duplicates:
            number = row["duplicate_number"]
            if number != current_number:
                if current_number is not None:
                    lines.append(u"")
                lines.append(u"### {0}: `{1}`".format(tr(lang, "number_label"), number))
                current_number = number
            lines.append(
                u"- ElementId `{0}` | {1} | {2}".format(
                    row["element_id"],
                    row["level_name"] or tr(lang, "none"),
                    row["room_name"] or tr(lang, "none"),
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
        "room_number",
        "room_name",
        "duplicate_number",
        "duplicate_count",
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
    report_path = os.path.join(export_dir, "duplicate_room_numbers_{0}.md".format(timestamp))
    csv_path = os.path.join(export_dir, "duplicate_room_numbers_{0}.csv".format(timestamp))

    room_count, group_count, duplicates = collect_duplicate_rows()
    write_markdown(report_path, build_report_lines(lang, room_count, group_count, duplicates))
    write_csv(csv_path, duplicates)

    output.print_md(tr(lang, "output_title"))
    output.print_md(u"")
    output.print_md(tr(lang, "output_done"))
    output.print_md(tr(lang, "output_groups").format(group_count))
    output.print_md(tr(lang, "output_rooms").format(len(duplicates)))
    output.print_md(tr(lang, "output_report").format(report_path))
    output.print_md(tr(lang, "output_csv").format(csv_path))

    forms.toast(
        tr(lang, "alert_done").format(group_count, len(duplicates), report_path),
        title=tr(lang, "alert_title"),
    )


try:
    main()
except Exception:
    err = traceback.format_exc()
    output.print_md(TEXT["zh"]["failed_title"] + u" / " + TEXT["en"]["failed_title"].replace("# ", u""))
    output.print_md("```text\n{0}\n```".format(err))
    forms.alert(TEXT["zh"]["failed_alert"] + u"\n\n" + TEXT["en"]["failed_alert"], title="Yang Agent")
