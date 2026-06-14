# -*- coding: utf-8 -*-
"""Replace or clear displayed text on selected dimension elements.

Selection-scoped direct-apply tool. Two modes:
- replace: set custom text on dimensions
- clear: restore original measured value display

Impact summary -> confirmation -> apply -> log -> Undo note.
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

from Autodesk.Revit.DB import Dimension  # noqa: E402
from pyrevit import forms, revit, script  # noqa: E402
from yang_agent_lang import get_or_choose_language  # noqa: E402
from yang_agent_settings import get_export_dir  # noqa: E402


doc = revit.doc
output = script.get_output()


TEXT = {
    "zh": {
        "language_message": u"选择语言 / Select language",
        "alert_title": u"Yang Agent",
        "no_doc": u"没有打开的 Revit 文档。",
        "need_more": u"请在 Revit 中预选至少 1 个 Dimension 标注元素，然后重新运行本工具。\n\n当前已选 Dimension 数量：{0}",
        "mode_label": u"选择操作模式",
        "mode_replace": u"替换覆盖文本",
        "mode_clear": u"清除覆盖文本（恢复原始数值）",
        "replace_prompt": u"输入替换文本",
        "no_replace_text": u"替换模式下替换文本不能为空。",
        "confirm_title": u"确认应用",
        "cancel_button": u"取消",
        "warning_replace": u"警告：标注替换会改变显示测量值，可能导致出图错误。",
        "confirm_message_replace": u"文档：{0}\n\n操作模式：替换覆盖文本\n数量：{1} 个 Dimension 标注\n替换文本：{2}\n\n{3}\n\n请确认：\n1. 当前模型是测试模型或已备份。\n2. 已检查替换文本是否正确。\n3. 如结果不对，可使用 Revit Undo 撤销。\n\n是否继续？",
        "confirm_message_clear": u"文档：{0}\n\n操作模式：清除覆盖文本\n数量：{1} 个 Dimension 标注\n\n将恢复原始测量值显示。\n\n请确认：\n1. 当前模型是测试模型或已备份。\n2. 如结果不对，可使用 Revit Undo 撤销。\n\n是否继续？",
        "title": u"# Yang Agent 应用标注文本覆盖",
        "summary": u"## 汇总",
        "document": u"- 文档：{0}",
        "mode_label_log": u"- 操作模式：{0}",
        "replace_text_log": u"- 替换文本：{0}",
        "count": u"- 处理数量：{0}",
        "applied": u"- 已应用：{0}",
        "failed": u"- 失败：{0}",
        "details": u"## 执行明细",
        "undo_title": u"## Undo / 回滚",
        "undo_line_1": u"- 本次修改在一个 Revit Transaction 内完成：`[Agent] Apply Dim Text Override`。",
        "undo_line_2": u"- 一次 Revit Undo 可撤销整批操作。",
        "undo_line_3": u"- 如结果不对，请立刻 Undo，并保留本日志用于排查。",
        "view_label": u"所属视图",
        "output_done": u"标注文本覆盖完成。模型已在 Revit Transaction 内修改。",
        "output_cancel": u"已取消，模型未修改。",
        "output_failed": u"标注文本覆盖失败。Transaction 已回滚，模型未修改。",
        "output_log": u"- 日志：`{0}`",
        "output_csv": u"- CSV 日志：`{0}`",
        "alert_done": u"标注文本覆盖完成。\n\n模式：{0}\n已应用：{1}\n失败：{2}\n\n{3}",
        "failed_title": u"# 标注文本覆盖失败",
        "failed_alert": u"标注文本覆盖失败。请查看 pyRevit 输出窗口。",
        "mode_replace_log": u"替换",
        "mode_clear_log": u"清除",
    },
    "en": {
        "language_message": u"Select language / 选择语言",
        "alert_title": u"Yang Agent",
        "no_doc": u"No active Revit document.",
        "need_more": u"Please pre-select at least 1 Dimension element in Revit, then re-run this tool.\n\nDimensions currently selected: {0}",
        "mode_label": u"Select operation mode",
        "mode_replace": u"Replace override text",
        "mode_clear": u"Clear override text (restore measured value)",
        "replace_prompt": u"Enter replacement text",
        "no_replace_text": u"Replacement text cannot be empty in replace mode.",
        "confirm_title": u"Confirm Apply",
        "cancel_button": u"Cancel",
        "warning_replace": u"WARNING: Dimension override changes the displayed measurement and may cause drawing errors.",
        "confirm_message_replace": u"Document: {0}\n\nMode: Replace override text\nCount: {1} dimension(s)\nReplacement text: {2}\n\n{3}\n\nConfirm:\n1. The current model is a test model or has been backed up.\n2. The replacement text was reviewed.\n3. Revit Undo can reverse this change if needed.\n\nContinue?",
        "confirm_message_clear": u"Document: {0}\n\nMode: Clear override text\nCount: {1} dimension(s)\n\nOriginal measured values will be restored.\n\nConfirm:\n1. The current model is a test model or has been backed up.\n2. Revit Undo can reverse this change if needed.\n\nContinue?",
        "title": u"# Yang Agent Apply Dim Text Override",
        "summary": u"## Summary",
        "document": u"- Document: {0}",
        "mode_label_log": u"- Mode: {0}",
        "replace_text_log": u"- Replacement text: {0}",
        "count": u"- Processed: {0}",
        "applied": u"- Applied: {0}",
        "failed": u"- Failed: {0}",
        "details": u"## Execution Details",
        "undo_title": u"## Undo / Rollback",
        "undo_line_1": u"- Changes were made inside one Revit Transaction: `[Agent] Apply Dim Text Override`.",
        "undo_line_2": u"- One Revit Undo reverses the full batch.",
        "undo_line_3": u"- If the result is wrong, undo immediately and keep this log for diagnosis.",
        "view_label": u"Owner view",
        "output_done": u"Dim text override completed. Model modified inside a Revit Transaction.",
        "output_cancel": u"Cancelled. No model changes were made.",
        "output_failed": u"Dim text override failed. Transaction rolled back, no model changes were made.",
        "output_log": u"- Log: `{0}`",
        "output_csv": u"- CSV log: `{0}`",
        "alert_done": u"Dim text override completed.\n\nMode: {0}\nApplied: {1}\nFailed: {2}\n\n{3}",
        "failed_title": u"# Dim Text Override failed",
        "failed_alert": u"Dim Text Override failed. See pyRevit output for details.",
        "mode_replace_log": u"Replace",
        "mode_clear_log": u"Clear",
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


def element_id_value(element_id):
    if element_id is None:
        return u""
    try:
        return safe_text(element_id.IntegerValue)
    except Exception:
        return safe_text(element_id)


def get_owner_view_name(element):
    try:
        from Autodesk.Revit.DB import View  # noqa: F811
        owner_view_id = element.OwnerViewId
        if owner_view_id is not None:
            view = doc.GetElement(owner_view_id)
            if isinstance(view, View):
                return safe_text(view.Name)
    except Exception:
        pass
    return u""


def get_current_override(dim):
    try:
        val = dim.ValueOverride
        if val is None:
            return u""
        return safe_text(val)
    except Exception:
        return u""


def get_segments_count(dim):
    try:
        return dim.Segments.Size
    except Exception:
        return 0


def choose_mode(lang):
    selected = forms.CommandSwitchWindow.show(
        [tr(lang, "mode_replace"), tr(lang, "mode_clear")],
        message=tr(lang, "mode_label"),
    )
    if selected == tr(lang, "mode_clear"):
        return "clear"
    return "replace"


def collect_pre_data(dimensions):
    pre = []
    for dim in dimensions:
        pre.append({
            "element_id": element_id_value(dim.Id),
            "category": "Dimension",
            "old_override": get_current_override(dim),
            "segments_count": get_segments_count(dim),
            "owner_view": get_owner_view_name(dim),
        })
    return pre


def build_failure_results(pre, mode, error):
    results = []
    for item in pre:
        results.append({
            "element_id": item["element_id"],
            "category": item["category"],
            "mode": mode,
            "old_override": item["old_override"],
            "new_override": u"",
            "segments_count": item["segments_count"],
            "owner_view": item["owner_view"],
            "result": "failed",
            "message": safe_text(error),
        })
    return results


def write_markdown(path, lang, mode, replace_text, pre, results):
    applied = sum(1 for r in results if r.get("result") == "applied")
    failed = sum(1 for r in results if r.get("result") == "failed")
    mode_label = tr(lang, "mode_" + mode + "_log")
    lines = []
    lines.append(tr(lang, "title"))
    lines.append(u"")
    lines.append(tr(lang, "summary"))
    lines.append(u"")
    lines.append(tr(lang, "document").format(safe_text(doc.Title)))
    lines.append(tr(lang, "mode_label_log").format(mode_label))
    if mode == "replace":
        lines.append(tr(lang, "replace_text_log").format(replace_text))
    lines.append(tr(lang, "count").format(len(pre)))
    lines.append(tr(lang, "applied").format(applied))
    lines.append(tr(lang, "failed").format(failed))
    lines.append(u"")
    lines.append(tr(lang, "undo_title"))
    lines.append(u"")
    lines.append(tr(lang, "undo_line_1"))
    lines.append(tr(lang, "undo_line_2"))
    lines.append(tr(lang, "undo_line_3"))
    lines.append(u"")
    lines.append(tr(lang, "details"))
    lines.append(u"")
    for i, r in enumerate(results):
        seg_info = u""
        if i < len(pre):
            sc = pre[i]["segments_count"]
            if sc > 0:
                seg_info = u" (segments: {0})".format(sc)
        lines.append(
            u"- `{0}` | {1}: `{2}` | {3} -> `{4}` | {5} | {6}{7}".format(
                r["element_id"],
                tr(lang, "view_label"),
                r.get("owner_view", u"") or u"-",
                r.get("old_override", u""),
                r.get("new_override", u""),
                r["result"],
                r["message"],
                seg_info,
            )
        )
    with codecs.open(path, "w", "utf-8-sig") as stream:
        stream.write(u"\n".join(lines))


def write_csv(path, results):
    fieldnames = [
        "element_id",
        "category",
        "mode",
        "old_override",
        "new_override",
        "segments_count",
        "owner_view",
        "result",
        "message",
    ]
    with open(path, "wb") as raw_stream:
        raw_stream.write(codecs.BOM_UTF8)
        writer = csv.DictWriter(raw_stream, fieldnames=fieldnames)
        header = {}
        for field in fieldnames:
            header[field] = field.encode("utf-8")
        writer.writerow(header)
        for row in results:
            encoded = {}
            for field in fieldnames:
                encoded[field] = safe_text(row.get(field, u"")).encode("utf-8")
            writer.writerow(encoded)


def main():
    lang = choose_language()

    if doc is None:
        forms.alert(tr(lang, "no_doc"), title=tr(lang, "alert_title"))
        return

    # --- Step 1: get pre-selected Dimensions ---
    selection = revit.get_selection()
    dimensions = [e for e in selection if isinstance(e, Dimension)]

    if len(dimensions) < 1:
        forms.alert(
            tr(lang, "need_more").format(len(dimensions)),
            title=tr(lang, "alert_title"),
        )
        return

    # --- Step 2: choose mode ---
    mode = choose_mode(lang)
    replace_text = u""

    if mode == "replace":
        replace_text = forms.ask_for_string(
            title=tr(lang, "alert_title"),
            prompt=tr(lang, "replace_prompt"),
        )
        if replace_text is None or safe_text(replace_text).strip() == u"":
            forms.alert(tr(lang, "no_replace_text"), title=tr(lang, "alert_title"))
            return
        replace_text = safe_text(replace_text).strip()
    else:
        replace_text = u""

    # --- Step 3: pre-collect data + confirmation ---
    pre = collect_pre_data(dimensions)

    if mode == "replace":
        confirm_msg = tr(lang, "confirm_message_replace").format(
            safe_text(doc.Title),
            len(dimensions),
            replace_text,
            tr(lang, "warning_replace"),
        )
    else:
        confirm_msg = tr(lang, "confirm_message_clear").format(
            safe_text(doc.Title),
            len(dimensions),
        )

    selected = forms.CommandSwitchWindow.show(
        [tr(lang, "confirm_title"), tr(lang, "cancel_button")],
        message=confirm_msg,
    )
    if selected != tr(lang, "confirm_title"):
        output.print_md(tr(lang, "output_cancel"))
        return

    # --- Step 4: apply in all-or-nothing Transaction ---
    # Pre-resolve IDs for Transaction use
    dim_ids = [d.Id for d in dimensions]
    new_value = replace_text  # for replace mode; empty string for clear mode

    try:
        with revit.Transaction("[Agent] Apply Dim Text Override"):
            for dim_id in dim_ids:
                dim = doc.GetElement(dim_id)
                if dim is None:
                    raise Exception("Dimension element not found: {0}".format(element_id_value(dim_id)))
                if dim.Segments.Size > 0:
                    for segment in dim.Segments:
                        segment.ValueOverride = new_value
                else:
                    dim.ValueOverride = new_value

        # Build success results from pre data
        results = []
        for item in pre:
            results.append({
                "element_id": item["element_id"],
                "category": item["category"],
                "mode": mode,
                "old_override": item["old_override"],
                "new_override": new_value,
                "segments_count": item["segments_count"],
                "owner_view": item["owner_view"],
                "result": "applied",
                "message": "OK",
            })
        success = True

    except Exception as apply_error:
        results = build_failure_results(pre, mode, apply_error)
        success = False

    # --- Step 5: export logs (success or failure) ---
    export_dir = get_export_dir()
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_path = os.path.join(export_dir, "apply_dim_text_override_{0}.md".format(timestamp))
    csv_path = os.path.join(export_dir, "apply_dim_text_override_{0}.csv".format(timestamp))

    write_markdown(log_path, lang, mode, replace_text, pre, results)
    write_csv(csv_path, results)

    if success:
        applied = sum(1 for r in results if r.get("result") == "applied")
        failed = sum(1 for r in results if r.get("result") == "failed")
        mode_label = tr(lang, "mode_" + mode + "_log")

        output.print_md(tr(lang, "title"))
        output.print_md(u"")
        output.print_md(tr(lang, "output_done"))
        output.print_md(u"")
        output.print_md(tr(lang, "undo_line_2"))
        output.print_md(tr(lang, "output_log").format(log_path))
        output.print_md(tr(lang, "output_csv").format(csv_path))

        forms.toast(
            tr(lang, "alert_done").format(mode_label, applied, failed, log_path),
            title=tr(lang, "alert_title"),
        )
    else:
        output.print_md(tr(lang, "title"))
        output.print_md(u"")
        output.print_md(tr(lang, "output_failed"))
        output.print_md(u"")
        output.print_md(tr(lang, "output_log").format(log_path))
        output.print_md(tr(lang, "output_csv").format(csv_path))

        forms.alert(tr(lang, "output_failed"), title=tr(lang, "alert_title"))


try:
    main()
except Exception:
    err = traceback.format_exc()
    output.print_md(TEXT["zh"]["failed_title"] + u" / " + TEXT["en"]["failed_title"].replace("# ", u""))
    output.print_md("```text\n{0}\n```".format(err))
    forms.alert(TEXT["zh"]["failed_alert"] + u"\n\n" + TEXT["en"]["failed_alert"], title="Yang Agent")
