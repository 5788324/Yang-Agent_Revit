# -*- coding: utf-8 -*-
"""Apply suggested door/window marks from a dry-run CSV.

This tool modifies the model only after the user selects a dry-run CSV and confirms.
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

from System import Int64  # noqa: E402
from Autodesk.Revit.DB import BuiltInParameter, ElementId  # noqa: E402
from pyrevit import forms, revit, script  # noqa: E402
from yang_agent_apply import (  # noqa: E402
    collect_apply_rows,
    confirm_apply,
    count_results,
    find_duplicate_element_ids,
    get_param_text,
    is_blank,
    is_expected_csv_name,
    parse_element_id,
    read_preview_csv,
    safe_text,
    validate_fields,
    write_utf8_csv,
)
from yang_agent_lang import get_export_dir, get_or_choose_language  # noqa: E402


doc = revit.doc
output = script.get_output()


TEXT = {
    "zh": {
        "alert_title": u"Yang Agent",
        "no_doc": u"没有打开的 Revit 文档。",
        "pick_csv": u"选择 missing_door_window_marks_*.csv",
        "no_csv": u"已取消。未选择 CSV。",
        "wrong_csv_name": u"YA-APPLY-MARK-001: 请选择 `预览缺失标记` 生成的 missing_door_window_marks_*.csv。\n\n当前文件：{0}",
        "bad_csv": u"CSV 缺少必要字段，不能执行。",
        "bad_csv_fields": u"YA-APPLY-MARK-002: CSV 缺少必要字段，不能执行。\n\n需要字段：{0}\n实际字段：{1}",
        "no_rows": u"没有可应用的门窗标记行。",
        "confirm": u"确认应用",
        "cancel": u"取消",
        "confirm_message": u"即将修改 {0} 个门窗元素的 Mark/标记。\n\n请确认：\n1. 当前模型是测试模型或已备份。\n2. CSV 来自 `预览缺失标记`。\n3. 已人工检查 suggested_mark。\n\n是否继续？",
        "title": u"# Yang Agent 应用门窗标记",
        "summary": u"## 汇总",
        "document": u"- 文档：{0}",
        "csv": u"- 来源 CSV：{0}",
        "applied": u"- 已应用：{0}",
        "skipped": u"- 已跳过：{0}",
        "failed": u"- 失败：{0}",
        "details": u"## 执行明细",
        "output_done": u"应用完成。模型已通过 Revit Transaction 修改。",
        "output_cancel": u"已取消。模型未修改。",
        "output_log": u"- 日志：`{0}`",
        "output_csv": u"- CSV 日志：`{0}`",
        "alert_done": u"门窗标记应用完成。\n\n已应用：{0}\n已跳过：{1}\n失败：{2}\n\n{3}",
        "failed_title": u"# 应用门窗标记失败",
        "failed_alert": u"应用门窗标记失败。请查看 pyRevit 输出窗口。",
    },
    "en": {
        "alert_title": u"Yang Agent",
        "no_doc": u"No active Revit document.",
        "pick_csv": u"Select missing_door_window_marks_*.csv",
        "no_csv": u"Cancelled. No CSV selected.",
        "wrong_csv_name": u"YA-APPLY-MARK-001: Please select missing_door_window_marks_*.csv exported by `Preview Missing Marks`.\n\nCurrent file: {0}",
        "bad_csv": u"CSV is missing required fields. Cannot apply.",
        "bad_csv_fields": u"YA-APPLY-MARK-002: CSV is missing required fields. Cannot apply.\n\nRequired fields: {0}\nActual fields: {1}",
        "no_rows": u"No applicable door/window mark rows were found.",
        "confirm": u"Apply",
        "cancel": u"Cancel",
        "confirm_message": u"This will modify Mark values on {0} door/window elements.\n\nPlease confirm:\n1. The current model is a test model or has been backed up.\n2. The CSV came from `Preview Missing Marks`.\n3. suggested_mark values were reviewed.\n\nContinue?",
        "title": u"# Yang Agent Apply Door/Window Marks",
        "summary": u"## Summary",
        "document": u"- Document: {0}",
        "csv": u"- Source CSV: {0}",
        "applied": u"- Applied: {0}",
        "skipped": u"- Skipped: {0}",
        "failed": u"- Failed: {0}",
        "details": u"## Details",
        "output_done": u"Apply completed. The model was modified inside a Revit Transaction.",
        "output_cancel": u"Cancelled. No model changes were made.",
        "output_log": u"- Log: `{0}`",
        "output_csv": u"- CSV log: `{0}`",
        "alert_done": u"Door/window marks applied.\n\nApplied: {0}\nSkipped: {1}\nFailed: {2}\n\n{3}",
        "failed_title": u"# Apply Door/Window Marks failed",
        "failed_alert": u"Apply Door/Window Marks failed. See pyRevit output for details.",
    },
}


REQUIRED_FIELDS = [
    "dry_run",
    "element_id",
    "category",
    "current_mark",
    "suggested_mark",
]


def tr(lang, key):
    return TEXT.get(lang, TEXT["zh"]).get(key, TEXT["zh"].get(key, key))

def is_applicable_row(row):
    category = safe_text(row.get("category")).strip()
    if category not in ["Door", "Window"]:
        return False
    if safe_text(row.get("dry_run")).lower().strip() != "true":
        return False
    if is_blank(row.get("suggested_mark")):
        return False
    if parse_element_id(row.get("element_id")) is None:
        return False
    return True


def get_mark_param(element):
    try:
        param = element.get_Parameter(BuiltInParameter.ALL_MODEL_MARK)
        if param is not None:
            return param
    except Exception:
        pass
    for name in ["Mark", u"标记"]:
        try:
            param = element.LookupParameter(name)
            if param is not None:
                return param
        except Exception:
            continue
    return None

def apply_marks(rows):
    results = []

    with revit.Transaction("[Agent] Apply Door Window Marks"):
        for row in rows:
            result = dict(row)
            result["applied_mark"] = u""
            result["result"] = u""
            result["message"] = u""

            element_id = parse_element_id(row.get("element_id"))
            if element_id is None:
                result["result"] = "failed"
                result["message"] = "YA-APPLY-MARK-003: Invalid ElementId"
                results.append(result)
                continue

            element = doc.GetElement(ElementId(Int64(element_id)))
            if element is None:
                result["result"] = "failed"
                result["message"] = "YA-APPLY-MARK-004: Element not found"
                results.append(result)
                continue

            param = get_mark_param(element)
            if param is None:
                result["result"] = "failed"
                result["message"] = "YA-APPLY-MARK-005: Mark parameter not found"
                results.append(result)
                continue

            try:
                if param.IsReadOnly:
                    result["result"] = "failed"
                    result["message"] = "YA-APPLY-MARK-006: Mark parameter is read-only"
                    results.append(result)
                    continue
            except Exception:
                pass

            existing_mark = get_param_text(param)
            result["actual_old_mark"] = existing_mark
            if not is_blank(existing_mark):
                result["result"] = "skipped"
                result["message"] = "Existing mark is not blank"
                results.append(result)
                continue

            suggested_mark = safe_text(row.get("suggested_mark")).strip()
            try:
                param.Set(suggested_mark)
                result["applied_mark"] = suggested_mark
                result["result"] = "applied"
                result["message"] = "OK"
            except Exception as set_error:
                result["result"] = "failed"
                result["message"] = safe_text(set_error)
            results.append(result)

    return results

def write_markdown(path, lang, source_csv, results):
    applied, skipped, failed = count_results(results)
    lines = []
    lines.append(tr(lang, "title"))
    lines.append(u"")
    lines.append(tr(lang, "summary"))
    lines.append(u"")
    lines.append(tr(lang, "document").format(safe_text(doc.Title)))
    lines.append(tr(lang, "csv").format(source_csv))
    lines.append(tr(lang, "applied").format(applied))
    lines.append(tr(lang, "skipped").format(skipped))
    lines.append(tr(lang, "failed").format(failed))
    lines.append(u"")
    lines.append(u"## Undo / Rollback")
    lines.append(u"")
    lines.append(u"- The changes were made inside one Revit Transaction: `[Agent] Apply Door Window Marks`.")
    lines.append(u"- In a test model, verify that one Revit Undo reverses the batch before using this workflow on real project work.")
    lines.append(u"- If the result is wrong, undo immediately and keep this log with the source CSV for diagnosis.")
    lines.append(u"")
    lines.append(tr(lang, "details"))
    lines.append(u"")
    for row in results:
        lines.append(
            u"- `{0}` {1} -> `{2}` | {3} | {4}".format(
                safe_text(row.get("element_id")),
                safe_text(row.get("category")),
                safe_text(row.get("applied_mark") or row.get("suggested_mark")),
                safe_text(row.get("result")),
                safe_text(row.get("message")),
            )
        )

    with codecs.open(path, "w", "utf-8-sig") as stream:
        stream.write(u"\n".join(lines))


def write_csv(path, rows):
    fieldnames = [
        "element_id",
        "category",
        "family_name",
        "type_name",
        "level_name",
        "current_mark",
        "suggested_mark",
        "actual_old_mark",
        "applied_mark",
        "result",
        "message",
    ]
    write_utf8_csv(path, rows, fieldnames)


def main():
    lang = get_or_choose_language(forms)

    if doc is None:
        forms.alert(tr(lang, "no_doc"), title=tr(lang, "alert_title"))
        return

    csv_path = forms.pick_file(
        files_filter="CSV Files (*.csv)|*.csv|All Files (*.*)|*.*",
        title=tr(lang, "pick_csv"),
    )
    if not csv_path:
        output.print_md(tr(lang, "output_cancel"))
        forms.toast(tr(lang, "no_csv"), title=tr(lang, "alert_title"))
        return

    if not is_expected_csv_name(csv_path, "missing_door_window_marks_"):
        forms.alert(
            tr(lang, "wrong_csv_name").format(os.path.basename(csv_path)),
            title=tr(lang, "alert_title"),
        )
        return

    rows, fieldnames = read_preview_csv(csv_path)
    if not validate_fields(fieldnames, REQUIRED_FIELDS):
        message = tr(lang, "bad_csv_fields").format(
            u", ".join(REQUIRED_FIELDS),
            u", ".join(fieldnames),
        )
        output.print_md(u"# CSV field validation failed")
        output.print_md(u"")
        output.print_md(u"- Required: `{0}`".format(u", ".join(REQUIRED_FIELDS)))
        output.print_md(u"- Actual: `{0}`".format(u", ".join(fieldnames)))
        forms.alert(message, title=tr(lang, "alert_title"))
        return

    apply_rows = collect_apply_rows(rows, is_applicable_row)
    if not apply_rows:
        forms.alert(tr(lang, "no_rows"), title=tr(lang, "alert_title"))
        return

    duplicate_ids = find_duplicate_element_ids(apply_rows)
    if duplicate_ids:
        message = "YA-APPLY-MARK-007: Duplicate element_id values in apply CSV: {0}".format(
            ", ".join(duplicate_ids)
        )
        output.print_md("# Apply CSV validation failed")
        output.print_md("")
        output.print_md(message)
        forms.alert(message, title=tr(lang, "alert_title"))
        return

    if not confirm_apply(
        forms,
        tr(lang, "confirm"),
        tr(lang, "cancel"),
        tr(lang, "confirm_message").format(len(apply_rows)),
    ):
        output.print_md(tr(lang, "output_cancel"))
        return

    results = apply_marks(apply_rows)
    applied, skipped, failed = count_results(results)

    export_dir = get_export_dir()
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_path = os.path.join(export_dir, "apply_door_window_marks_{0}.md".format(timestamp))
    log_csv_path = os.path.join(export_dir, "apply_door_window_marks_{0}.csv".format(timestamp))

    write_markdown(log_path, lang, csv_path, results)
    write_csv(log_csv_path, results)

    output.print_md(tr(lang, "title"))
    output.print_md(u"")
    output.print_md(tr(lang, "output_done"))
    output.print_md(u"")
    output.print_md(u"- Undo / rollback: verify one Revit Undo reverses `[Agent] Apply Door Window Marks` in a test model.")
    output.print_md(tr(lang, "applied").format(applied))
    output.print_md(tr(lang, "skipped").format(skipped))
    output.print_md(tr(lang, "failed").format(failed))
    output.print_md(tr(lang, "output_log").format(log_path))
    output.print_md(tr(lang, "output_csv").format(log_csv_path))

    forms.alert(
        tr(lang, "alert_done").format(applied, skipped, failed, log_path),
        title=tr(lang, "alert_title"),
    )


try:
    main()
except Exception:
    err = traceback.format_exc()
    output.print_md(TEXT["zh"]["failed_title"] + u" / " + TEXT["en"]["failed_title"].replace("# ", u""))
    output.print_md("```text\n{0}\n```".format(err))
    forms.alert(TEXT["zh"]["failed_alert"] + u"\n\n" + TEXT["en"]["failed_alert"], title="Yang Agent")
