# -*- coding: utf-8 -*-
"""Find and replace text on TextNote elements in the active document.

Low-risk personal-use model modification tool.
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

from Autodesk.Revit.DB import FilteredElementCollector, TextNote, View  # noqa: E402
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
        "find_label": u"查找文本",
        "replace_label": u"替换为（留空表示替换为空文本）",
        "case_sensitive_label": u"是否区分大小写？",
        "case_insensitive": u"不区分大小写",
        "case_sensitive_option": u"区分大小写",
        "no_find_text": u"查找文本不能为空。",
        "no_match": u"未找到匹配的 TextNote。未修改模型。",
        "confirm_title": u"确认应用",
        "cancel_button": u"取消",
        "confirm_message": u"文档：{0}\n\n查找文本：{1}\n替换文本：{2}\n区分大小写：{3}\n\n即将修改 {4} 个 TextNote 元素。\n\n请确认：\n1. 当前模型是测试模型或已备份。\n2. 已检查查找和替换文本。\n3. 如结果不对，可使用 Revit Undo 撤销。\n\n是否继续？",
        "yes": u"是",
        "no": u"否",
        "empty": u"(空)",
        "title": u"# Yang Agent 应用文本查找替换",
        "summary": u"## 摘要",
        "document": u"- 文档：{0}",
        "find_text": u"- 查找文本：{0}",
        "replace_text": u"- 替换文本：{0}",
        "case_sensitive": u"- 区分大小写：{0}",
        "applied": u"- 已替换：{0}",
        "details": u"## 执行明细",
        "undo_title": u"## Undo / 回滚",
        "undo_line_1": u"- 本次修改在一个 Revit Transaction 内完成：`[Agent] Apply Text Find Replace`。",
        "undo_line_2": u"- 如结果不对，请立即使用 Revit Undo 撤销，并保留本日志用于排查。",
        "view_label": u"所属视图",
        "old_label": u"原文本",
        "new_label": u"新文本",
        "output_done": u"文本替换完成。模型已在 Revit Transaction 内修改。",
        "output_cancel": u"已取消，模型未修改。",
        "output_applied": u"- 已替换：{0}",
        "output_log": u"- 日志：`{0}`",
        "output_csv": u"- CSV 日志：`{0}`",
        "alert_done": u"文本替换完成。\n\n已替换：{0}\n\n{1}",
        "failed_title": u"# 文本查找替换失败",
        "failed_alert": u"文本查找替换失败。请查看 pyRevit 输出窗口。",
    },
    "en": {
        "language_message": u"Select language / 选择语言",
        "alert_title": u"Yang Agent",
        "no_doc": u"No active Revit document.",
        "find_label": u"Find text",
        "replace_label": u"Replace with (leave empty to replace with empty text)",
        "case_sensitive_label": u"Case sensitivity?",
        "case_insensitive": u"Case insensitive",
        "case_sensitive_option": u"Case sensitive",
        "no_find_text": u"Find text cannot be empty.",
        "no_match": u"No matching TextNotes found. No model changes were made.",
        "confirm_title": u"Confirm Apply",
        "cancel_button": u"Cancel",
        "confirm_message": u"Document: {0}\n\nFind text: {1}\nReplace text: {2}\nCase sensitive: {3}\n\nThis will modify {4} TextNote element(s).\n\nPlease confirm:\n1. The current model is a test model or has been backed up.\n2. Find and replacement text were reviewed.\n3. Revit Undo can reverse this change if needed.\n\nContinue?",
        "yes": u"Yes",
        "no": u"No",
        "empty": u"(empty)",
        "title": u"# Yang Agent Apply Text Find & Replace",
        "summary": u"## Summary",
        "document": u"- Document: {0}",
        "find_text": u"- Find text: {0}",
        "replace_text": u"- Replace text: {0}",
        "case_sensitive": u"- Case sensitive: {0}",
        "applied": u"- Replaced: {0}",
        "details": u"## Execution Details",
        "undo_title": u"## Undo / Rollback",
        "undo_line_1": u"- Changes were made inside one Revit Transaction: `[Agent] Apply Text Find Replace`.",
        "undo_line_2": u"- If the result is wrong, use Revit Undo immediately and keep this log for diagnosis.",
        "view_label": u"Owner view",
        "old_label": u"Old text",
        "new_label": u"New text",
        "output_done": u"Text replace completed. The model was modified inside a Revit Transaction.",
        "output_cancel": u"Cancelled. No model changes were made.",
        "output_applied": u"- Replaced: {0}",
        "output_log": u"- Log: `{0}`",
        "output_csv": u"- CSV log: `{0}`",
        "alert_done": u"Text replace completed.\n\nReplaced: {0}\n\n{1}",
        "failed_title": u"# Text Find & Replace failed",
        "failed_alert": u"Text Find & Replace failed. See pyRevit output for details.",
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


def get_owner_view_name(element):
    try:
        owner_view_id = element.OwnerViewId
        if owner_view_id is not None:
            view = doc.GetElement(owner_view_id)
            if isinstance(view, View):
                return safe_text(view.Name)
    except Exception:
        pass
    return u""


def bool_label(lang, value):
    return tr(lang, "yes") if value else tr(lang, "no")


def collect_textnotes():
    return list(
        FilteredElementCollector(doc)
        .OfClass(TextNote)
        .WhereElementIsNotElementType()
        .ToElements()
    )


def match_text(text, find_text, case_sensitive):
    if case_sensitive:
        return find_text in text
    return find_text.lower() in text.lower()


def apply_replacement(text, find_text, replace_text, case_sensitive):
    if case_sensitive:
        return text.replace(find_text, replace_text)
    lower_text = text.lower()
    lower_find = find_text.lower()
    result_parts = []
    pos = 0
    while True:
        idx = lower_text.find(lower_find, pos)
        if idx == -1:
            result_parts.append(text[pos:])
            break
        result_parts.append(text[pos:idx])
        result_parts.append(replace_text)
        pos = idx + len(find_text)
    return u"".join(result_parts)


def choose_case_sensitive(lang):
    insensitive = tr(lang, "case_insensitive")
    sensitive = tr(lang, "case_sensitive_option")
    selected = forms.CommandSwitchWindow.show(
        [insensitive, sensitive],
        message=tr(lang, "case_sensitive_label"),
    )
    return selected == sensitive


def find_candidates(textnotes, find_text, replace_text, case_sensitive):
    candidates = []
    for note in textnotes:
        note_text = safe_text(note.Text)
        if is_blank(note_text):
            continue
        if not match_text(note_text, find_text, case_sensitive):
            continue
        candidates.append({
            "element": note,
            "element_id": element_id_value(note.Id),
            "old_text": note_text,
            "new_text": apply_replacement(note_text, find_text, replace_text, case_sensitive),
            "owner_view": get_owner_view_name(note),
        })
    return candidates


def apply_text_changes(candidates):
    results = []
    with revit.Transaction("[Agent] Apply Text Find Replace"):
        for c in candidates:
            result = {
                "element_id": c["element_id"],
                "category": "TextNote",
                "old_text": c["old_text"],
                "new_text": c["new_text"],
                "owner_view": c["owner_view"],
                "result": u"",
                "message": u"",
            }
            element = c["element"]
            try:
                element.Text = c["new_text"]
                result["result"] = "applied"
                result["message"] = "OK"
            except Exception as set_error:
                result["result"] = "failed"
                result["message"] = safe_text(set_error)
            results.append(result)
    return results


def count_applied(results):
    count = 0
    for r in results:
        if r.get("result") == "applied":
            count += 1
    return count


def write_markdown(path, lang, find_text, replace_text, case_sensitive, results):
    applied = count_applied(results)
    lines = []
    lines.append(tr(lang, "title"))
    lines.append(u"")
    lines.append(tr(lang, "summary"))
    lines.append(u"")
    lines.append(tr(lang, "document").format(safe_text(doc.Title)))
    lines.append(tr(lang, "find_text").format(find_text))
    lines.append(tr(lang, "replace_text").format(replace_text if replace_text else tr(lang, "empty")))
    lines.append(tr(lang, "case_sensitive").format(bool_label(lang, case_sensitive)))
    lines.append(tr(lang, "applied").format(applied))
    lines.append(u"")
    lines.append(tr(lang, "undo_title"))
    lines.append(u"")
    lines.append(tr(lang, "undo_line_1"))
    lines.append(tr(lang, "undo_line_2"))
    lines.append(u"")
    lines.append(tr(lang, "details"))
    lines.append(u"")
    for r in results:
        view_name = r.get("owner_view", u"") or u"-"
        lines.append(
            u"- `{0}` | {1}: `{2}` | {3}: `{4}` | {5}: `{6}` | {7} | {8}".format(
                r["element_id"],
                tr(lang, "view_label"),
                view_name,
                tr(lang, "old_label"),
                r["old_text"],
                tr(lang, "new_label"),
                r["new_text"],
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

    find_text = forms.ask_for_string(
        title=tr(lang, "alert_title"),
        prompt=tr(lang, "find_label"),
    )
    if find_text is None or is_blank(find_text):
        forms.alert(tr(lang, "no_find_text"), title=tr(lang, "alert_title"))
        return
    find_text = safe_text(find_text).strip()

    replace_text = forms.ask_for_string(
        title=tr(lang, "alert_title"),
        prompt=tr(lang, "replace_label"),
    )
    if replace_text is None:
        replace_text = u""
    replace_text = safe_text(replace_text)

    case_sensitive = choose_case_sensitive(lang)

    textnotes = collect_textnotes()
    candidates = find_candidates(textnotes, find_text, replace_text, case_sensitive)

    if not candidates:
        forms.alert(tr(lang, "no_match"), title=tr(lang, "alert_title"))
        return

    selected = forms.CommandSwitchWindow.show(
        [tr(lang, "confirm_title"), tr(lang, "cancel_button")],
        message=tr(lang, "confirm_message").format(
            safe_text(doc.Title),
            find_text,
            replace_text if replace_text else tr(lang, "empty"),
            bool_label(lang, case_sensitive),
            len(candidates),
        ),
    )
    if selected != tr(lang, "confirm_title"):
        output.print_md(tr(lang, "output_cancel"))
        return

    results = apply_text_changes(candidates)
    applied = count_applied(results)

    export_dir = get_export_dir()
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_path = os.path.join(export_dir, "apply_text_find_replace_{0}.md".format(timestamp))
    csv_path = os.path.join(export_dir, "apply_text_find_replace_{0}.csv".format(timestamp))

    write_markdown(log_path, lang, find_text, replace_text, case_sensitive, results)
    write_csv(csv_path, results)

    output.print_md(tr(lang, "title"))
    output.print_md(u"")
    output.print_md(tr(lang, "output_done"))
    output.print_md(u"")
    output.print_md(tr(lang, "undo_line_2"))
    output.print_md(tr(lang, "output_applied").format(applied))
    output.print_md(tr(lang, "output_log").format(log_path))
    output.print_md(tr(lang, "output_csv").format(csv_path))

    forms.toast(
        tr(lang, "alert_done").format(applied, log_path),
        title=tr(lang, "alert_title"),
    )


try:
    main()
except Exception:
    err = traceback.format_exc()
    output.print_md(TEXT["zh"]["failed_title"] + u" / " + TEXT["en"]["failed_title"].replace("# ", u""))
    output.print_md("```text\n{0}\n```".format(err))
    forms.alert(TEXT["zh"]["failed_alert"] + u"\n\n" + TEXT["en"]["failed_alert"], title="Yang Agent")
