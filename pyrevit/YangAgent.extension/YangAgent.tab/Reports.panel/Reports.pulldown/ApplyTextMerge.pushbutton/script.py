# -*- coding: utf-8 -*-
"""Merge multiple selected TextNote elements into one.

Selection-scoped direct-apply tool with explicit delete warning.
All-or-nothing Transaction following mainline pyRevit pattern.
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

from Autodesk.Revit.DB import TextNote, View  # noqa: E402
from pyrevit import forms, revit, script  # noqa: E402
from yang_agent_lang import get_or_choose_language  # noqa: E402
from yang_agent_settings import get_export_dir  # noqa: E402


doc = revit.doc
output = script.get_output()

MERGE_TEXT_TRUNCATE = 200


TEXT = {
    "zh": {
        "language_message": u"选择语言 / Select language",
        "alert_title": u"Yang Agent",
        "no_doc": u"没有打开的 Revit 文档。",
        "need_more": u"请在 Revit 中预选至少 2 个 TextNote 元素（可框选），然后重新运行本工具。\n\n当前已选 TextNote 数量：{0}",
        "sort_label": u"选择合并顺序",
        "sort_selection": u"按选择顺序",
        "sort_x_asc": u"按 X 坐标升序（从左到右）",
        "sort_x_desc": u"按 X 坐标降序（从右到左）",
        "sort_y_asc": u"按 Y 坐标升序（从下到上）",
        "sort_y_desc": u"按 Y 坐标降序（从上到下）",
        "separator_label": u"选择分隔符",
        "sep_newline": u"换行符",
        "sep_space": u"空格",
        "sep_comma": u"逗号",
        "sep_none": u"无分隔",
        "confirm_title": u"确认合并",
        "cancel_button": u"取消",
        "delete_warning": u"警告：将删除 {0} 个 TextNote 元素",
        "merged_text_preview": u"合并后文本预览：\n{0}",
        "text_truncated": u"\n（文本过长，已截断至 {0} 字符）",
        "confirm_message": u"文档：{0}\n\n合并数量：{1} 个 TextNote\n保留元素 ID：{2}\n将删除元素 ID：{3}\n分隔符：{4}\n排序方式：{5}\n\n{6}\n\n{7}\n\n请确认：\n1. 当前模型是测试模型或已备份。\n2. 已检查保留元素、删除元素列表和合并后文本。\n3. 如结果不对，可使用 Revit Undo 撤销（含删除）。\n\n是否继续？",
        "title": u"# Yang Agent 应用文本合并",
        "summary": u"## 汇总",
        "document": u"- 文档：{0}",
        "merged_count": u"- 合并数量：{0}",
        "keep_id": u"- 保留元素：{0}",
        "delete_ids": u"- 已删除元素：{0}",
        "separator_used": u"- 分隔符：{0}",
        "sort_used": u"- 排序方式：{0}",
        "merged_text": u"## 合并后文本",
        "details": u"## 执行明细",
        "undo_title": u"## Undo / 回滚",
        "undo_line_1": u"- 本次修改在一个 Revit Transaction 内完成：`[Agent] Apply Text Merge`。",
        "undo_line_2": u"- 一次 Revit Undo 可撤销整批操作（含合并和删除）。",
        "undo_line_3": u"- 如结果不对，请立刻 Undo，并保留本日志用于排查。",
        "view_label": u"所属视图",
        "output_done": u"文本合并完成。模型已在 Revit Transaction 内修改。",
        "output_cancel": u"已取消，模型未修改。",
        "output_failed": u"文本合并失败。Transaction 已回滚，模型未修改。",
        "output_log": u"- 日志：`{0}`",
        "output_csv": u"- CSV 日志：`{0}`",
        "alert_done": u"文本合并完成。\n\n已合并：{0} 个 TextNote\n保留：{1}\n已删除：{2}\n\n{3}",
        "failed_title": u"# 文本合并失败",
        "failed_alert": u"文本合并失败。请查看 pyRevit 输出窗口。",
        "sep_label_newline": u"换行符",
        "sep_label_space": u"空格",
        "sep_label_comma": u"逗号",
        "sep_label_none": u"无分隔",
    },
    "en": {
        "language_message": u"Select language / 选择语言",
        "alert_title": u"Yang Agent",
        "no_doc": u"No active Revit document.",
        "need_more": u"Please pre-select at least 2 TextNote elements in Revit (use box-select), then re-run this tool.\n\nTextNotes currently selected: {0}",
        "sort_label": u"Select sort order",
        "sort_selection": u"Selection order",
        "sort_x_asc": u"X coordinate ascending (left to right)",
        "sort_x_desc": u"X coordinate descending (right to left)",
        "sort_y_asc": u"Y coordinate ascending (bottom to top)",
        "sort_y_desc": u"Y coordinate descending (top to bottom)",
        "separator_label": u"Select separator",
        "sep_newline": u"Newline",
        "sep_space": u"Space",
        "sep_comma": u"Comma",
        "sep_none": u"None",
        "confirm_title": u"Confirm Merge",
        "cancel_button": u"Cancel",
        "delete_warning": u"WARNING: {0} TextNote element(s) will be DELETED",
        "merged_text_preview": u"Merged text preview:\n{0}",
        "text_truncated": u"\n(Text too long, truncated to {0} characters)",
        "confirm_message": u"Document: {0}\n\nMerge count: {1} TextNote(s)\nKeep element ID: {2}\nDelete element IDs: {3}\nSeparator: {4}\nSort: {5}\n\n{6}\n\n{7}\n\nConfirm:\n1. The current model is a test model or has been backed up.\n2. The keep element, delete list, and merged text were reviewed.\n3. Revit Undo can reverse this entire operation (including deletions).\n\nContinue?",
        "title": u"# Yang Agent Apply Text Merge",
        "summary": u"## Summary",
        "document": u"- Document: {0}",
        "merged_count": u"- Merged: {0}",
        "keep_id": u"- Kept: {0}",
        "delete_ids": u"- Deleted: {0}",
        "separator_used": u"- Separator: {0}",
        "sort_used": u"- Sort: {0}",
        "merged_text": u"## Merged Text",
        "details": u"## Execution Details",
        "undo_title": u"## Undo / Rollback",
        "undo_line_1": u"- Changes were made inside one Revit Transaction: `[Agent] Apply Text Merge`.",
        "undo_line_2": u"- One Revit Undo reverses the full batch (merge and deletions).",
        "undo_line_3": u"- If the result is wrong, undo immediately and keep this log for diagnosis.",
        "view_label": u"Owner view",
        "output_done": u"Text merge completed. Model modified inside a Revit Transaction.",
        "output_cancel": u"Cancelled. No model changes were made.",
        "output_failed": u"Text merge failed. Transaction rolled back, no model changes were made.",
        "output_log": u"- Log: `{0}`",
        "output_csv": u"- CSV log: `{0}`",
        "alert_done": u"Text merge completed.\n\nMerged: {0} TextNote(s)\nKept: {1}\nDeleted: {2}\n\n{3}",
        "failed_title": u"# Text Merge failed",
        "failed_alert": u"Text Merge failed. See pyRevit output for details.",
        "sep_label_newline": u"Newline",
        "sep_label_space": u"Space",
        "sep_label_comma": u"Comma",
        "sep_label_none": u"None",
    },
}


SEPARATOR_MAP = {
    "newline": u"\n",
    "space": u" ",
    "comma": u",",
    "none": u"",
}

SEPARATOR_LABEL_KEYS = {
    "newline": "sep_label_newline",
    "space": "sep_label_space",
    "comma": "sep_label_comma",
    "none": "sep_label_none",
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


def get_owner_view_name(note):
    try:
        owner_view_id = note.OwnerViewId
        if owner_view_id is not None:
            view = doc.GetElement(owner_view_id)
            if isinstance(view, View):
                return safe_text(view.Name)
    except Exception:
        pass
    return u""


def truncate_text(text, max_chars, lang):
    if len(text) <= max_chars:
        return text
    return text[:max_chars] + tr(lang, "text_truncated").format(max_chars)


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
    selected = forms.CommandSwitchWindow.show(
        options,
        message=tr(lang, "sort_label"),
    )
    if selected == tr(lang, "sort_x_asc"):
        return "x_asc"
    if selected == tr(lang, "sort_x_desc"):
        return "x_desc"
    if selected == tr(lang, "sort_y_asc"):
        return "y_asc"
    if selected == tr(lang, "sort_y_desc"):
        return "y_desc"
    return "selection"


def choose_separator(lang):
    options = [
        tr(lang, "sep_newline"),
        tr(lang, "sep_space"),
        tr(lang, "sep_comma"),
        tr(lang, "sep_none"),
    ]
    selected = forms.CommandSwitchWindow.show(
        options,
        message=tr(lang, "separator_label"),
    )
    if selected == tr(lang, "sep_space"):
        return "space"
    if selected == tr(lang, "sep_comma"):
        return "comma"
    if selected == tr(lang, "sep_none"):
        return "none"
    return "newline"


def collect_pre_data(keep_note, delete_notes):
    pre = {
        "keep_id": keep_note.Id,
        "keep_owner": get_owner_view_name(keep_note),
        "delete_items": [],
    }
    for note in delete_notes:
        pre["delete_items"].append({
            "element_id": element_id_value(note.Id),
            "old_text": safe_text(note.Text),
            "owner_view": get_owner_view_name(note),
        })
    return pre


def build_success_results(pre, merged_text):
    results = []
    for item in pre["delete_items"]:
        results.append({
            "element_id": item["element_id"],
            "category": "TextNote",
            "action": "deleted",
            "old_text": item["old_text"],
            "new_text": u"",
            "owner_view": item["owner_view"],
            "result": "deleted",
            "message": "Element deleted",
        })
    results.append({
        "element_id": element_id_value(pre["keep_id"]),
        "category": "TextNote",
        "action": "merged",
        "old_text": u"",
        "new_text": merged_text,
        "owner_view": pre["keep_owner"],
        "result": "applied",
        "message": "Merged text written",
    })
    return results


def build_failure_results(pre, merged_text, error):
    results = []
    for item in pre["delete_items"]:
        results.append({
            "element_id": item["element_id"],
            "category": "TextNote",
            "action": "deleted",
            "old_text": item["old_text"],
            "new_text": u"",
            "owner_view": item["owner_view"],
            "result": "failed",
            "message": "Transaction rolled back",
        })
    results.append({
        "element_id": element_id_value(pre["keep_id"]),
        "category": "TextNote",
        "action": "merged",
        "old_text": u"",
        "new_text": merged_text,
        "owner_view": pre["keep_owner"],
        "result": "failed",
        "message": safe_text(error),
    })
    return results


def write_markdown(path, lang, sort_mode, sep_key, sorted_notes, merged_text, results):
    delete_ids = [element_id_value(n.Id) for n in sorted_notes[1:]]
    lines = []
    lines.append(tr(lang, "title"))
    lines.append(u"")
    lines.append(tr(lang, "summary"))
    lines.append(u"")
    lines.append(tr(lang, "document").format(safe_text(doc.Title)))
    lines.append(tr(lang, "merged_count").format(len(sorted_notes)))
    lines.append(tr(lang, "keep_id").format(element_id_value(sorted_notes[0].Id)))
    lines.append(tr(lang, "delete_ids").format(u", ".join(delete_ids)))
    lines.append(tr(lang, "separator_used").format(tr(lang, SEPARATOR_LABEL_KEYS[sep_key])))
    lines.append(tr(lang, "sort_used").format(tr(lang, "sort_" + sort_mode)))
    lines.append(u"")
    lines.append(tr(lang, "merged_text"))
    lines.append(u"")
    lines.append(u"```")
    lines.append(merged_text)
    lines.append(u"```")
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
            u"- `{0}` | {1}: `{2}` | {3}: `{4}` | {5} | {6}".format(
                r["element_id"],
                tr(lang, "view_label"),
                r.get("owner_view", u"") or u"-",
                r["action"],
                r.get("old_text", u"") or r.get("new_text", u""),
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
        "action",
        "old_text",
        "new_text",
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

    # --- Step 1: get pre-selected TextNotes ---
    selection = revit.get_selection()
    textnotes = [e for e in selection if isinstance(e, TextNote)]

    if len(textnotes) < 2:
        forms.alert(
            tr(lang, "need_more").format(len(textnotes)),
            title=tr(lang, "alert_title"),
        )
        return

    # --- Step 2: choose sort mode and separator ---
    sort_mode = choose_sort_mode(lang)
    sep_key = choose_separator(lang)
    separator = SEPARATOR_MAP[sep_key]

    sorted_notes = sort_textnotes(textnotes, sort_mode)

    # --- Step 3: compute impact summary ---
    keep_note = sorted_notes[0]
    delete_notes = sorted_notes[1:]
    all_texts = [safe_text(n.Text) for n in sorted_notes]
    merged_text = separator.join(all_texts)

    # Truncate for confirmation dialog
    truncated = truncate_text(merged_text, MERGE_TEXT_TRUNCATE, lang)
    merged_preview = tr(lang, "merged_text_preview").format(truncated)

    delete_ids_str = u", ".join([element_id_value(n.Id) for n in delete_notes])

    # --- Step 4: confirmation with merged text preview + delete warning ---
    selected = forms.CommandSwitchWindow.show(
        [tr(lang, "confirm_title"), tr(lang, "cancel_button")],
        message=tr(lang, "confirm_message").format(
            safe_text(doc.Title),
            len(sorted_notes),
            element_id_value(keep_note.Id),
            delete_ids_str,
            tr(lang, SEPARATOR_LABEL_KEYS[sep_key]),
            tr(lang, "sort_" + sort_mode),
            merged_preview,
            tr(lang, "delete_warning").format(len(delete_notes)),
        ),
    )
    if selected != tr(lang, "confirm_title"):
        output.print_md(tr(lang, "output_cancel"))
        return

    # --- Step 5: pre-collect data, then apply in all-or-nothing Transaction ---
    pre = collect_pre_data(keep_note, delete_notes)

    # Pre-resolve ElementIds for Transaction use
    keep_id = keep_note.Id
    delete_ids = [n.Id for n in delete_notes]

    try:
        with revit.Transaction("[Agent] Apply Text Merge"):
            for note_id in delete_ids:
                doc.Delete(note_id)
            keep_element = doc.GetElement(keep_id)
            keep_element.Text = merged_text
        # Transaction committed — build success results
        results = build_success_results(pre, merged_text)
        success = True

    except Exception as apply_error:
        # Transaction rolled back by with-block on exception
        results = build_failure_results(pre, merged_text, apply_error)
        success = False

    # --- Step 6: export durable logs (success or failure) ---
    export_dir = get_export_dir()
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_path = os.path.join(export_dir, "apply_text_merge_{0}.md".format(timestamp))
    csv_path = os.path.join(export_dir, "apply_text_merge_{0}.csv".format(timestamp))

    write_markdown(log_path, lang, sort_mode, sep_key, sorted_notes, merged_text, results)
    write_csv(csv_path, results)

    if success:
        output.print_md(tr(lang, "title"))
        output.print_md(u"")
        output.print_md(tr(lang, "output_done"))
        output.print_md(u"")
        output.print_md(tr(lang, "undo_line_2"))
        output.print_md(tr(lang, "output_log").format(log_path))
        output.print_md(tr(lang, "output_csv").format(csv_path))

        forms.toast(
            tr(lang, "alert_done").format(
                len(sorted_notes),
                element_id_value(keep_note.Id),
                len(delete_notes),
                log_path,
            ),
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
