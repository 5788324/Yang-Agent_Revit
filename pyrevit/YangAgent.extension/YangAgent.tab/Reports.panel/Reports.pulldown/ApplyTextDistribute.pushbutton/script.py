# -*- coding: utf-8 -*-
"""Distribute selected TextNote elements evenly along X or Y axis.

Selection-scoped direct-apply tool. Position-only changes via MoveElement.
No text content modification, no element deletion.
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

from Autodesk.Revit.DB import ElementTransformUtils, TextNote, XYZ  # noqa: E402
from pyrevit import forms, revit, script  # noqa: E402
from yang_agent_lang import get_or_choose_language  # noqa: E402
from yang_agent_settings import get_export_dir  # noqa: E402


doc = revit.doc
output = script.get_output()

# 1 mm = 1 / 304.8 feet (Revit internal length unit)
MM_TO_FEET = 1.0 / 304.8


TEXT = {
    "zh": {
        "language_message": u"选择语言 / Select language",
        "alert_title": u"Yang Agent",
        "no_doc": u"没有打开的 Revit 文档。",
        "need_more": u"请在 Revit 中预选至少 2 个 TextNote 元素（可框选），然后重新运行本工具。\n\n当前已选 TextNote 数量：{0}",
        "sort_label": u"选择排序方式",
        "sort_selection": u"按选择顺序",
        "sort_x_asc": u"按 X 坐标升序（从左到右）",
        "sort_x_desc": u"按 X 坐标降序（从右到左）",
        "sort_y_asc": u"按 Y 坐标升序（从下到上）",
        "sort_y_desc": u"按 Y 坐标降序（从上到下）",
        "direction_label": u"选择分布方向",
        "dir_x": u"沿 X 轴（水平）",
        "dir_y": u"沿 Y 轴（垂直）",
        "spacing_prompt": u"输入间距（毫米）",
        "spacing_invalid": u"间距必须是正数。输入值：{0}",
        "alignment_label": u"选择对齐方式",
        "align_none": u"不额外对齐",
        "align_x": u"对齐 X 坐标（沿 X 分布，Y 统一）",
        "align_y": u"对齐 Y 坐标（沿 Y 分布，X 统一）",
        "confirm_title": u"确认应用",
        "cancel_button": u"取消",
        "confirm_message": u"文档：{0}\n\n数量：{1} 个 TextNote\n排序方式：{2}\n分布方向：{3}\n间距：{4} 毫米\n对齐方式：{5}\n\n即将移动 {1} 个 TextNote 元素。\n\n请确认：\n1. 当前模型是测试模型或已备份。\n2. 如结果不对，可使用 Revit Undo 撤销。\n\n是否继续？",
        "title": u"# Yang Agent 应用文本等距分布",
        "summary": u"## 汇总",
        "document": u"- 文档：{0}",
        "count_label": u"- 数量：{0}",
        "sort_label_log": u"- 排序方式：{0}",
        "direction_label_log": u"- 分布方向：{0}",
        "spacing_label_log": u"- 间距：{0} 毫米",
        "alignment_label_log": u"- 对齐方式：{0}",
        "applied": u"- 已移动：{0}",
        "failed": u"- 失败：{0}",
        "details": u"## 执行明细",
        "undo_title": u"## Undo / 回滚",
        "undo_line_1": u"- 本次修改在一个 Revit Transaction 内完成：`[Agent] Apply Text Distribute`。",
        "undo_line_2": u"- 一次 Revit Undo 可撤销整批移动操作。",
        "undo_line_3": u"- 如结果不对，请立刻 Undo，并保留本日志用于排查。",
        "output_done": u"文本等距分布完成。模型已在 Revit Transaction 内修改。",
        "output_cancel": u"已取消，模型未修改。",
        "output_failed": u"文本等距分布失败。Transaction 已回滚，模型未修改。",
        "output_log": u"- 日志：`{0}`",
        "output_csv": u"- CSV 日志：`{0}`",
        "alert_done": u"文本等距分布完成。\n\n已移动：{0}\n失败：{1}\n\n{2}",
        "failed_title": u"# 文本等距分布失败",
        "failed_alert": u"文本等距分布失败。请查看 pyRevit 输出窗口。",
        "sort_sel_log": u"选择顺序",
        "sort_xa_log": u"X 升序",
        "sort_xd_log": u"X 降序",
        "sort_ya_log": u"Y 升序",
        "sort_yd_log": u"Y 降序",
        "dir_x_log": u"X 轴",
        "dir_y_log": u"Y 轴",
        "align_none_log": u"无",
        "align_x_log": u"对齐 X",
        "align_y_log": u"对齐 Y",
    },
    "en": {
        "language_message": u"Select language / 选择语言",
        "alert_title": u"Yang Agent",
        "no_doc": u"No active Revit document.",
        "need_more": u"Please pre-select at least 2 TextNote elements in Revit (use box-select), then re-run this tool.\n\nTextNotes currently selected: {0}",
        "sort_label": u"Select sort order",
        "sort_selection": u"Selection order",
        "sort_x_asc": u"X ascending (left to right)",
        "sort_x_desc": u"X descending (right to left)",
        "sort_y_asc": u"Y ascending (bottom to top)",
        "sort_y_desc": u"Y descending (top to bottom)",
        "direction_label": u"Select distribution direction",
        "dir_x": u"Along X axis (horizontal)",
        "dir_y": u"Along Y axis (vertical)",
        "spacing_prompt": u"Enter spacing (mm)",
        "spacing_invalid": u"Spacing must be a positive number. Got: {0}",
        "alignment_label": u"Select alignment",
        "align_none": u"No extra alignment",
        "align_x": u"Align X (distribute on X, unify Y)",
        "align_y": u"Align Y (distribute on Y, unify X)",
        "confirm_title": u"Confirm Apply",
        "cancel_button": u"Cancel",
        "confirm_message": u"Document: {0}\n\nCount: {1} TextNote(s)\nSort: {2}\nDirection: {3}\nSpacing: {4} mm\nAlignment: {5}\n\nThis will move {1} TextNote(s).\n\nConfirm:\n1. The current model is a test model or has been backed up.\n2. Revit Undo can reverse this change if needed.\n\nContinue?",
        "title": u"# Yang Agent Apply Text Distribute",
        "summary": u"## Summary",
        "document": u"- Document: {0}",
        "count_label": u"- Count: {0}",
        "sort_label_log": u"- Sort: {0}",
        "direction_label_log": u"- Direction: {0}",
        "spacing_label_log": u"- Spacing: {0} mm",
        "alignment_label_log": u"- Alignment: {0}",
        "applied": u"- Moved: {0}",
        "failed": u"- Failed: {0}",
        "details": u"## Execution Details",
        "undo_title": u"## Undo / Rollback",
        "undo_line_1": u"- Changes were made inside one Revit Transaction: `[Agent] Apply Text Distribute`.",
        "undo_line_2": u"- One Revit Undo reverses the full batch move.",
        "undo_line_3": u"- If the result is wrong, undo immediately and keep this log for diagnosis.",
        "output_done": u"Text distribute completed. Model modified inside a Revit Transaction.",
        "output_cancel": u"Cancelled. No model changes were made.",
        "output_failed": u"Text distribute failed. Transaction rolled back, no model changes were made.",
        "output_log": u"- Log: `{0}`",
        "output_csv": u"- CSV log: `{0}`",
        "alert_done": u"Text distribute completed.\n\nMoved: {0}\nFailed: {1}\n\n{2}",
        "failed_title": u"# Text Distribute failed",
        "failed_alert": u"Text Distribute failed. See pyRevit output for details.",
        "sort_sel_log": u"Selection",
        "sort_xa_log": u"X Asc",
        "sort_xd_log": u"X Desc",
        "sort_ya_log": u"Y Asc",
        "sort_yd_log": u"Y Desc",
        "dir_x_log": u"X Axis",
        "dir_y_log": u"Y Axis",
        "align_none_log": u"None",
        "align_x_log": u"Align X",
        "align_y_log": u"Align Y",
    },
}


SORT_LOG_KEYS = {
    "selection": "sort_sel_log",
    "x_asc": "sort_xa_log",
    "x_desc": "sort_xd_log",
    "y_asc": "sort_ya_log",
    "y_desc": "sort_yd_log",
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


def get_note_coord(note):
    try:
        c = note.Coord
        return (c.X, c.Y)
    except Exception:
        return (0.0, 0.0)


def sort_textnotes(notes, sort_mode):
    if sort_mode == "selection":
        return list(notes)
    if sort_mode == "x_asc":
        return sorted(notes, key=get_note_coord)
    if sort_mode == "x_desc":
        return sorted(notes, key=lambda n: -get_note_coord(n)[0])
    if sort_mode == "y_asc":
        return sorted(notes, key=lambda n: get_note_coord(n)[1])
    if sort_mode == "y_desc":
        return sorted(notes, key=lambda n: -get_note_coord(n)[1])
    return list(notes)


def choose_sort_mode(lang):
    options = [
        tr(lang, "sort_selection"),
        tr(lang, "sort_x_asc"),
        tr(lang, "sort_x_desc"),
        tr(lang, "sort_y_asc"),
        tr(lang, "sort_y_desc"),
    ]
    selected = forms.CommandSwitchWindow.show(options, message=tr(lang, "sort_label"))
    if selected == tr(lang, "sort_x_asc"):
        return "x_asc"
    if selected == tr(lang, "sort_x_desc"):
        return "x_desc"
    if selected == tr(lang, "sort_y_asc"):
        return "y_asc"
    if selected == tr(lang, "sort_y_desc"):
        return "y_desc"
    return "selection"


def choose_direction(lang):
    selected = forms.CommandSwitchWindow.show(
        [tr(lang, "dir_x"), tr(lang, "dir_y")],
        message=tr(lang, "direction_label"),
    )
    return "y" if selected == tr(lang, "dir_y") else "x"


def choose_alignment(lang):
    selected = forms.CommandSwitchWindow.show(
        [tr(lang, "align_none"), tr(lang, "align_x"), tr(lang, "align_y")],
        message=tr(lang, "alignment_label"),
    )
    if selected == tr(lang, "align_x"):
        return "x"
    if selected == tr(lang, "align_y"):
        return "y"
    return "none"


def coord_str(x, y):
    return u"({0:.4f}, {1:.4f})".format(x, y)


def write_markdown(path, lang, sort_mode, direction, spacing_mm, alignment, pre, results):
    applied = sum(1 for r in results if r.get("result") == "applied")
    failed = sum(1 for r in results if r.get("result") == "failed")
    lines = []
    lines.append(tr(lang, "title"))
    lines.append(u"")
    lines.append(tr(lang, "summary"))
    lines.append(u"")
    lines.append(tr(lang, "document").format(safe_text(doc.Title)))
    lines.append(tr(lang, "count_label").format(len(pre)))
    lines.append(tr(lang, "sort_label_log").format(tr(lang, SORT_LOG_KEYS[sort_mode])))
    lines.append(tr(lang, "direction_label_log").format(tr(lang, "dir_" + direction + "_log")))
    lines.append(tr(lang, "spacing_label_log").format(spacing_mm))
    lines.append(tr(lang, "alignment_label_log").format(tr(lang, "align_" + alignment + "_log")))
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
    for r in results:
        lines.append(
            u"- `{0}` | {1} -> {2} | delta: ({3:+.4f}, {4:+.4f}) | {5} | {6}".format(
                r["element_id"],
                coord_str(r["old_x"], r["old_y"]),
                coord_str(r["new_x"], r["new_y"]),
                r["delta_x"],
                r["delta_y"],
                r["result"],
                r["message"],
            )
        )
    with codecs.open(path, "w", "utf-8-sig") as stream:
        stream.write(u"\n".join(lines))


def write_csv(path, results):
    fieldnames = [
        "element_id",
        "category",
        "old_x",
        "old_y",
        "new_x",
        "new_y",
        "delta_x",
        "delta_y",
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
                val = row.get(field, u"")
                if isinstance(val, float):
                    val = u"{0:.4f}".format(val)
                encoded[field] = safe_text(val).encode("utf-8")
            writer.writerow(encoded)


def main():
    lang = choose_language()

    if doc is None:
        forms.alert(tr(lang, "no_doc"), title=tr(lang, "alert_title"))
        return

    # --- Step 1: get pre-selected TextNotes ---
    selection = revit.get_selection()
    textnotes = [e for e in selection if isinstance(e, TextNote)]

    if len(textnotes) < 2:
        forms.alert(
            tr(lang, "need_more").format(len(textnotes)),
            title=tr(lang, "alert_title"),
        )
        return

    # --- Step 2: choose parameters ---
    sort_mode = choose_sort_mode(lang)
    direction = choose_direction(lang)
    spacing_str = forms.ask_for_string(
        title=tr(lang, "alert_title"),
        prompt=tr(lang, "spacing_prompt"),
    )
    if spacing_str is None:
        return
    try:
        spacing_mm = float(safe_text(spacing_str).strip())
        if spacing_mm <= 0:
            forms.alert(tr(lang, "spacing_invalid").format(spacing_str), title=tr(lang, "alert_title"))
            return
    except Exception:
        forms.alert(tr(lang, "spacing_invalid").format(spacing_str), title=tr(lang, "alert_title"))
        return

    alignment = choose_alignment(lang)

    sorted_notes = sort_textnotes(textnotes, sort_mode)
    spacing_feet = spacing_mm * MM_TO_FEET
    step_sign = -1 if sort_mode in ("x_desc", "y_desc") else 1

    # --- Step 3: compute target positions + pre-collect data ---
    first = sorted_notes[0]
    base_x, base_y = get_note_coord(first)

    pre = []
    for i, note in enumerate(sorted_notes):
        old_x, old_y = get_note_coord(note)
        offset = spacing_feet * i * step_sign
        if direction == "x":
            new_x = base_x + offset
            new_y = base_y if alignment == "x" else old_y
        else:
            new_y = base_y + offset
            new_x = base_x if alignment == "y" else old_x
        pre.append({
            "element_id": element_id_value(note.Id),
            "category": "TextNote",
            "old_x": old_x,
            "old_y": old_y,
            "new_x": new_x,
            "new_y": new_y,
        })

    # --- Step 4: confirmation ---
    selected = forms.CommandSwitchWindow.show(
        [tr(lang, "confirm_title"), tr(lang, "cancel_button")],
        message=tr(lang, "confirm_message").format(
            safe_text(doc.Title),
            len(sorted_notes),
            tr(lang, SORT_LOG_KEYS[sort_mode]),
            tr(lang, "dir_" + direction + "_log"),
            spacing_mm,
            tr(lang, "align_" + alignment + "_log"),
        ),
    )
    if selected != tr(lang, "confirm_title"):
        output.print_md(tr(lang, "output_cancel"))
        return

    # --- Step 5: apply in all-or-nothing Transaction ---
    try:
        with revit.Transaction("[Agent] Apply Text Distribute"):
            for i, item in enumerate(pre):
                note = sorted_notes[i]
                dx = item["new_x"] - item["old_x"]
                dy = item["new_y"] - item["old_y"]
                vec = XYZ(dx, dy, 0.0)
                ElementTransformUtils.MoveElement(doc, note.Id, vec)

        results = []
        for item in pre:
            dx = item["new_x"] - item["old_x"]
            dy = item["new_y"] - item["old_y"]
            results.append({
                "element_id": item["element_id"],
                "category": item["category"],
                "old_x": item["old_x"],
                "old_y": item["old_y"],
                "new_x": item["new_x"],
                "new_y": item["new_y"],
                "delta_x": dx,
                "delta_y": dy,
                "result": "applied",
                "message": "OK",
            })
        success = True

    except Exception as apply_error:
        results = []
        for item in pre:
            dx = item["new_x"] - item["old_x"]
            dy = item["new_y"] - item["old_y"]
            results.append({
                "element_id": item["element_id"],
                "category": item["category"],
                "old_x": item["old_x"],
                "old_y": item["old_y"],
                "new_x": item["new_x"],
                "new_y": item["new_y"],
                "delta_x": dx,
                "delta_y": dy,
                "result": "failed",
                "message": safe_text(apply_error),
            })
        success = False

    # --- Step 6: export logs ---
    export_dir = get_export_dir()
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_path = os.path.join(export_dir, "apply_text_distribute_{0}.md".format(timestamp))
    csv_path = os.path.join(export_dir, "apply_text_distribute_{0}.csv".format(timestamp))

    write_markdown(log_path, lang, sort_mode, direction, spacing_mm, alignment, pre, results)
    write_csv(csv_path, results)

    if success:
        applied = sum(1 for r in results if r.get("result") == "applied")
        failed = sum(1 for r in results if r.get("result") == "failed")
        output.print_md(tr(lang, "title"))
        output.print_md(u"")
        output.print_md(tr(lang, "output_done"))
        output.print_md(u"")
        output.print_md(tr(lang, "undo_line_2"))
        output.print_md(tr(lang, "output_log").format(log_path))
        output.print_md(tr(lang, "output_csv").format(csv_path))
        forms.toast(
            tr(lang, "alert_done").format(applied, failed, log_path),
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
