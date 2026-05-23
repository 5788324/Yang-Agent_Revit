# -*- coding: utf-8 -*-
"""Preview doors and windows missing marks.

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
from pyrevit import forms, revit, script  # noqa: E402
from yang_agent_lang import get_export_dir, get_or_choose_language  # noqa: E402


doc = revit.doc
output = script.get_output()


TEXT = {
    "zh": {
        "alert_title": u"Yang Agent",
        "no_doc": u"没有打开的 Revit 文档。",
        "title": u"# Yang Agent 门窗缺失标记预览",
        "read_only": u"此报告为 dry-run 预览，未修改 Revit 模型。",
        "summary": u"## 汇总",
        "document": u"- 文档：{0}",
        "exported_at": u"- 导出时间：{0}",
        "doors_total": u"- 门总数：{0}",
        "windows_total": u"- 窗总数：{0}",
        "missing_total": u"- 缺少标记总数：{0}",
        "details": u"## 缺少标记的门窗",
        "none": u"- 无",
        "suggested": u"建议标记",
        "next_steps": u"## 建议下一步",
        "step_1": u"1. 人工检查建议标记是否符合公司标准。",
        "step_2": u"2. 如确认无误，再生成 apply 工具写入标记。",
        "step_3": u"3. apply 前仍需二次确认影响元素数量。",
        "output_done": u"预览完成。此工具未修改模型。",
        "output_missing": u"- 缺少标记：{0}",
        "output_report": u"- 报告：`{0}`",
        "output_csv": u"- CSV：`{0}`",
        "alert_done": u"门窗缺失标记预览已生成。\n\n此工具未修改模型。\n\n缺少标记：{0}\n\n{1}",
        "failed_title": u"# 门窗缺失标记预览失败",
        "failed_alert": u"门窗缺失标记预览失败。请查看 pyRevit 输出窗口。",
    },
    "en": {
        "alert_title": u"Yang Agent",
        "no_doc": u"No active Revit document.",
        "title": u"# Yang Agent Missing Door and Window Marks Preview",
        "read_only": u"This is a dry-run preview. No Revit model changes were made.",
        "summary": u"## Summary",
        "document": u"- Document: {0}",
        "exported_at": u"- Exported at: {0}",
        "doors_total": u"- Total doors: {0}",
        "windows_total": u"- Total windows: {0}",
        "missing_total": u"- Missing marks: {0}",
        "details": u"## Doors and Windows Missing Marks",
        "none": u"- None",
        "suggested": u"Suggested mark",
        "next_steps": u"## Suggested Next Steps",
        "step_1": u"1. Review suggested marks against company standards.",
        "step_2": u"2. Generate an apply tool only after confirming the preview.",
        "step_3": u"3. Confirm affected element count again before applying changes.",
        "output_done": u"Preview completed. No model changes were made.",
        "output_missing": u"- Missing marks: {0}",
        "output_report": u"- Report: `{0}`",
        "output_csv": u"- CSV: `{0}`",
        "alert_done": u"Missing door/window marks preview generated.\n\nNo model changes were made.\n\nMissing marks: {0}\n\n{1}",
        "failed_title": u"# Missing Door and Window Marks Preview failed",
        "failed_alert": u"Missing Door and Window Marks Preview failed. See pyRevit output for details.",
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


def get_family_type(element):
    family_name = u""
    type_name = u""
    try:
        symbol = doc.GetElement(element.GetTypeId())
        if symbol:
            type_name = safe_text(symbol.Name)
            family_name = safe_text(symbol.Family.Name)
    except Exception:
        pass
    return family_name, type_name


def get_level_name(element):
    try:
        level = doc.GetElement(element.LevelId)
        if level:
            return safe_text(level.Name)
    except Exception:
        pass
    return u""


def collect_category(built_in_category, category_name):
    rows = []
    collector = FilteredElementCollector(doc).OfCategory(
        built_in_category
    ).WhereElementIsNotElementType()

    for element in collector.ToElements():
        mark = get_param_as_text(element, BuiltInParameter.ALL_MODEL_MARK)
        family_name, type_name = get_family_type(element)
        rows.append({
            "element_id": element_id_value(element.Id),
            "category": category_name,
            "family_name": family_name,
            "type_name": type_name,
            "level_name": get_level_name(element),
            "current_mark": mark,
        })
    return rows


def build_suggested_mark(row, index):
    prefix = "D" if row["category"] == "Door" else "W"
    level = safe_text(row.get("level_name"))
    if level:
        clean_level = level.replace(" ", "").replace("-", "")
        return "{0}-{1}-{2:03d}".format(prefix, clean_level, index)
    return "{0}-{1:03d}".format(prefix, index)


def collect_preview_rows():
    all_rows = []
    all_rows.extend(collect_category(BuiltInCategory.OST_Doors, "Door"))
    all_rows.extend(collect_category(BuiltInCategory.OST_Windows, "Window"))

    missing = []
    door_count = 0
    window_count = 0
    missing_index = 1

    for row in all_rows:
        if row["category"] == "Door":
            door_count += 1
        elif row["category"] == "Window":
            window_count += 1

        if is_blank(row.get("current_mark")):
            row["suggested_mark"] = build_suggested_mark(row, missing_index)
            row["dry_run"] = "true"
            missing.append(row)
            missing_index += 1

    return door_count, window_count, missing


def write_markdown(path, lang, door_count, window_count, missing):
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
    lines.append(tr(lang, "doors_total").format(door_count))
    lines.append(tr(lang, "windows_total").format(window_count))
    lines.append(tr(lang, "missing_total").format(len(missing)))
    lines.append(u"")
    lines.append(tr(lang, "details"))
    lines.append(u"")

    if not missing:
        lines.append(tr(lang, "none"))
    else:
        for row in missing:
            lines.append(
                u"- `{0}` {1} | {2} | {3} | {4}: `{5}`".format(
                    row["element_id"],
                    row["category"],
                    row["level_name"],
                    row["family_name"],
                    tr(lang, "suggested"),
                    row["suggested_mark"],
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
        "family_name",
        "type_name",
        "current_mark",
        "suggested_mark",
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
    report_path = os.path.join(export_dir, "missing_door_window_marks_{0}.md".format(timestamp))
    csv_path = os.path.join(export_dir, "missing_door_window_marks_{0}.csv".format(timestamp))

    door_count, window_count, missing = collect_preview_rows()
    write_markdown(report_path, lang, door_count, window_count, missing)
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
