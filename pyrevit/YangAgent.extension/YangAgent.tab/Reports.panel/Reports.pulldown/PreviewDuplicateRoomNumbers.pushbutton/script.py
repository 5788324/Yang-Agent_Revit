# -*- coding: utf-8 -*-
"""Preview duplicate room numbers.

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
    BuiltInCategory,
    BuiltInParameter,
    FilteredElementCollector,
)
from Autodesk.Revit.DB.Architecture import Room  # noqa: E402
from pyrevit import forms, revit, script  # noqa: E402
from yang_agent_lang import get_export_dir, get_or_choose_language  # noqa: E402


doc = revit.doc
output = script.get_output()


TEXT = {
    "zh": {
        "alert_title": u"Yang Agent",
        "no_doc": u"没有打开的 Revit 文档。",
        "title": u"# Yang Agent 重复房间编号预览",
        "read_only": u"此报告为 dry-run 预览，未修改 Revit 模型。",
        "summary": u"## 汇总",
        "document": u"- 文档：{0}",
        "exported_at": u"- 导出时间：{0}",
        "rooms_total": u"- 房间总数：{0}",
        "duplicate_groups": u"- 重复编号组：{0}",
        "duplicate_rooms": u"- 涉及房间数：{0}",
        "details": u"## 重复房间编号",
        "none": u"- 无",
        "next_steps": u"## 建议下一步",
        "step_1": u"1. 人工确认重复编号是否属于分区、套内或设计意图。",
        "step_2": u"2. 确认公司房间编号规则后，再生成修复预览。",
        "step_3": u"3. 不建议直接自动批量重编号。",
        "output_done": u"预览完成。此工具未修改模型。",
        "output_groups": u"- 重复编号组：{0}",
        "output_report": u"- 报告：`{0}`",
        "output_csv": u"- CSV：`{0}`",
        "alert_done": u"重复房间编号预览已生成。\n\n此工具未修改模型。\n\n重复编号组：{0}\n\n{1}",
        "failed_title": u"# 重复房间编号预览失败",
        "failed_alert": u"重复房间编号预览失败。请查看 pyRevit 输出窗口。",
    },
    "en": {
        "alert_title": u"Yang Agent",
        "no_doc": u"No active Revit document.",
        "title": u"# Yang Agent Duplicate Room Numbers Preview",
        "read_only": u"This is a dry-run preview. No Revit model changes were made.",
        "summary": u"## Summary",
        "document": u"- Document: {0}",
        "exported_at": u"- Exported at: {0}",
        "rooms_total": u"- Total rooms: {0}",
        "duplicate_groups": u"- Duplicate number groups: {0}",
        "duplicate_rooms": u"- Affected rooms: {0}",
        "details": u"## Duplicate Room Numbers",
        "none": u"- None",
        "next_steps": u"## Suggested Next Steps",
        "step_1": u"1. Confirm whether duplicates are intentional.",
        "step_2": u"2. Define company room numbering rules before generating repair previews.",
        "step_3": u"3. Avoid direct automatic bulk renumbering.",
        "output_done": u"Preview completed. No model changes were made.",
        "output_groups": u"- Duplicate number groups: {0}",
        "output_report": u"- Report: `{0}`",
        "output_csv": u"- CSV: `{0}`",
        "alert_done": u"Duplicate room numbers preview generated.\n\nNo model changes were made.\n\nDuplicate number groups: {0}\n\n{1}",
        "failed_title": u"# Duplicate Room Numbers Preview failed",
        "failed_alert": u"Duplicate Room Numbers Preview failed. See pyRevit output for details.",
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
    try:
        return safe_text(param.AsInteger())
    except Exception:
        pass
    try:
        return safe_text(param.AsDouble())
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


def get_level_name(room):
    try:
        level = doc.GetElement(room.LevelId)
        if level:
            return safe_text(level.Name)
    except Exception:
        pass
    return u""


def collect_rooms():
    rows = []
    collector = FilteredElementCollector(doc).OfCategory(
        BuiltInCategory.OST_Rooms
    ).WhereElementIsNotElementType()

    for element in collector.ToElements():
        if not isinstance(element, Room):
            continue
        rows.append({
            "element_id": element_id_value(element.Id),
            "category": "Room",
            "room_number": get_param_as_text(element, BuiltInParameter.ROOM_NUMBER),
            "room_name": get_param_as_text(element, BuiltInParameter.ROOM_NAME),
            "level_name": get_level_name(element),
        })
    return rows


def collect_duplicate_rows():
    rooms = collect_rooms()
    by_number = {}
    for row in rooms:
        number = safe_text(row.get("room_number")).strip()
        if is_blank(number):
            continue
        by_number.setdefault(number, []).append(row)

    duplicates = []
    group_count = 0
    for number in sorted(by_number.keys()):
        group_rows = by_number[number]
        if len(group_rows) < 2:
            continue
        group_count += 1
        for row in group_rows:
            row["dry_run"] = "true"
            row["duplicate_number"] = number
            row["duplicate_count"] = safe_text(len(group_rows))
            row["status"] = "Duplicate"
            duplicates.append(row)

    return len(rooms), group_count, duplicates


def write_markdown(path, lang, room_count, group_count, duplicates):
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
    lines.append(tr(lang, "rooms_total").format(room_count))
    lines.append(tr(lang, "duplicate_groups").format(group_count))
    lines.append(tr(lang, "duplicate_rooms").format(len(duplicates)))
    lines.append(u"")
    lines.append(tr(lang, "details"))
    lines.append(u"")

    if not duplicates:
        lines.append(tr(lang, "none"))
    else:
        current_number = None
        for row in duplicates:
            number = row["duplicate_number"]
            if number != current_number:
                lines.append(u"")
                lines.append(u"### `{0}`".format(number))
                current_number = number
            lines.append(
                u"- `{0}` {1} | {2}".format(
                    row["element_id"],
                    row["level_name"],
                    row["room_name"],
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
    lang = get_or_choose_language(forms)

    if doc is None:
        forms.alert(tr(lang, "no_doc"), title=tr(lang, "alert_title"))
        return

    export_dir = get_export_dir()
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_path = os.path.join(export_dir, "duplicate_room_numbers_{0}.md".format(timestamp))
    csv_path = os.path.join(export_dir, "duplicate_room_numbers_{0}.csv".format(timestamp))

    room_count, group_count, duplicates = collect_duplicate_rows()
    write_markdown(report_path, lang, room_count, group_count, duplicates)
    write_csv(csv_path, duplicates)

    output.print_md(tr(lang, "title"))
    output.print_md(u"")
    output.print_md(tr(lang, "output_done"))
    output.print_md(u"")
    output.print_md(tr(lang, "output_groups").format(group_count))
    output.print_md(tr(lang, "output_report").format(report_path))
    output.print_md(tr(lang, "output_csv").format(csv_path))

    forms.toast(
        tr(lang, "alert_done").format(group_count, report_path),
        title=tr(lang, "alert_title"),
    )


try:
    main()
except Exception:
    err = traceback.format_exc()
    output.print_md(TEXT["zh"]["failed_title"] + u" / " + TEXT["en"]["failed_title"].replace("# ", u""))
    output.print_md("```text\n{0}\n```".format(err))
    forms.alert(TEXT["zh"]["failed_alert"] + u"\n\n" + TEXT["en"]["failed_alert"], title="Yang Agent")
