# -*- coding: utf-8 -*-
"""Preview rooms missing numbers.

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
        "title": u"# Yang Agent 房间缺失编号预览",
        "read_only": u"此报告为 dry-run 预览，未修改 Revit 模型。",
        "summary": u"## 汇总",
        "document": u"- 文档：{0}",
        "exported_at": u"- 导出时间：{0}",
        "rooms_total": u"- 房间总数：{0}",
        "missing_total": u"- 缺少编号房间数：{0}",
        "details": u"## 缺少编号的房间",
        "none": u"- 无",
        "suggested": u"建议编号",
        "next_steps": u"## 建议下一步",
        "step_1": u"1. 人工检查建议编号是否符合项目编号规则。",
        "step_2": u"2. 如确认无误，再生成 apply 工具写入房间编号。",
        "step_3": u"3. apply 前仍需二次确认影响房间数量。",
        "output_done": u"预览完成。此工具未修改模型。",
        "output_missing": u"- 缺少编号房间：{0}",
        "output_report": u"- 报告：`{0}`",
        "output_csv": u"- CSV：`{0}`",
        "alert_done": u"房间缺失编号预览已生成。\n\n此工具未修改模型。\n\n缺少编号房间：{0}\n\n{1}",
        "failed_title": u"# 房间缺失编号预览失败",
        "failed_alert": u"房间缺失编号预览失败。请查看 pyRevit 输出窗口。",
    },
    "en": {
        "alert_title": u"Yang Agent",
        "no_doc": u"No active Revit document.",
        "title": u"# Yang Agent Missing Room Numbers Preview",
        "read_only": u"This is a dry-run preview. No Revit model changes were made.",
        "summary": u"## Summary",
        "document": u"- Document: {0}",
        "exported_at": u"- Exported at: {0}",
        "rooms_total": u"- Total rooms: {0}",
        "missing_total": u"- Rooms missing numbers: {0}",
        "details": u"## Rooms Missing Numbers",
        "none": u"- None",
        "suggested": u"Suggested number",
        "next_steps": u"## Suggested Next Steps",
        "step_1": u"1. Review suggested numbers against project numbering rules.",
        "step_2": u"2. Generate an apply tool only after confirming the preview.",
        "step_3": u"3. Confirm affected room count again before applying changes.",
        "output_done": u"Preview completed. No model changes were made.",
        "output_missing": u"- Rooms missing numbers: {0}",
        "output_report": u"- Report: `{0}`",
        "output_csv": u"- CSV: `{0}`",
        "alert_done": u"Missing room numbers preview generated.\n\nNo model changes were made.\n\nRooms missing numbers: {0}\n\n{1}",
        "failed_title": u"# Missing Room Numbers Preview failed",
        "failed_alert": u"Missing Room Numbers Preview failed. See pyRevit output for details.",
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


def get_param_as_text(element, built_in_param):
    try:
        param = element.get_Parameter(built_in_param)
        if not param:
            return u""
        return safe_text(param.AsValueString() or param.AsString() or param.AsDouble() or param.AsInteger())
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
            "room_name": get_param_as_text(element, BuiltInParameter.ROOM_NAME),
            "current_number": get_param_as_text(element, BuiltInParameter.ROOM_NUMBER),
            "level_name": get_level_name(element),
        })
    return rows


def build_suggested_number(row, index):
    level = safe_text(row.get("level_name"))
    if level:
        clean_level = level.replace(" ", "").replace("-", "")
        return "{0}-{1:03d}".format(clean_level, index)
    return "R-{0:03d}".format(index)


def collect_preview_rows():
    rooms = collect_rooms()
    missing = []
    missing_index = 1

    for row in rooms:
        if is_blank(row.get("current_number")):
            row["suggested_number"] = build_suggested_number(row, missing_index)
            row["dry_run"] = "true"
            row["status"] = "Missing"
            missing.append(row)
            missing_index += 1

    return len(rooms), missing


def write_markdown(path, lang, room_count, missing):
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
    lines.append(tr(lang, "missing_total").format(len(missing)))
    lines.append(u"")
    lines.append(tr(lang, "details"))
    lines.append(u"")

    if not missing:
        lines.append(tr(lang, "none"))
    else:
        for row in missing:
            lines.append(
                u"- `{0}` {1} | {2} | {3}: `{4}`".format(
                    row["element_id"],
                    row["level_name"],
                    row["room_name"],
                    tr(lang, "suggested"),
                    row["suggested_number"],
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
    lang = get_or_choose_language(forms)

    if doc is None:
        forms.alert(tr(lang, "no_doc"), title=tr(lang, "alert_title"))
        return

    export_dir = get_export_dir()
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_path = os.path.join(export_dir, "missing_room_numbers_{0}.md".format(timestamp))
    csv_path = os.path.join(export_dir, "missing_room_numbers_{0}.csv".format(timestamp))

    room_count, missing = collect_preview_rows()
    write_markdown(report_path, lang, room_count, missing)
    write_csv(csv_path, missing)

    output.print_md(tr(lang, "title"))
    output.print_md(u"")
    output.print_md(tr(lang, "output_done"))
    output.print_md(u"")
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
