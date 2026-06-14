# -*- coding: utf-8 -*-
"""Preview text find-and-replace candidates on TextNote elements.

Dry-run only. This tool exports CSV + Markdown for human review before any
future apply command.
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
        "find_label": u"查找文本",
        "replace_label": u"替换为（留空表示替换为空文本）",
        "case_sensitive_label": u"是否区分大小写？",
        "case_insensitive": u"不区分大小写",
        "case_sensitive_option": u"区分大小写",
        "report_title": u"# Yang Agent 文本查找替换预览",
        "read_only_note": u"这是 dry-run 只读预览，不会修改 Revit 模型。",
        "summary_heading": u"统计摘要",
        "document": u"文档：{0}",
        "exported_at": u"导出时间：{0}",
        "find_text": u"查找文本：{0}",
        "replace_text": u"替换文本：{0}",
        "case_sensitive": u"区分大小写：{0}",
        "yes": u"是",
        "no": u"否",
        "textnotes_total": u"TextNote 总数：{0}",
        "candidate_count": u"匹配数量：{0}",
        "detail_heading": u"替换候选明细",
        "view_label": u"所属视图",
        "current_label": u"当前文本",
        "proposed_label": u"替换后文本",
        "next_steps_heading": u"建议下一步",
        "next_step_1": u"先检查 CSV 中的替换候选是否符合预期。",
        "next_step_2": u"确认替换文本无误后，再决定是否执行 apply。",
        "next_step_3": u"不要修改 CSV 的 dry_run、element_id、category 字段。",
        "none": u"无匹配结果。",
        "output_title": u"# Yang Agent 文本查找替换预览",
        "output_done": u"预览完成。未修改模型。",
        "output_candidates": u"- 匹配数量：{0}",
        "output_report": u"- 报告：`{0}`",
        "output_csv": u"- CSV：`{0}`",
        "alert_done": u"文本查找替换预览已生成。\n\n未修改模型。\n\n匹配数量：{0}\n\n{1}",
        "failed_title": u"# 文本查找替换预览失败",
        "failed_alert": u"文本查找替换预览失败。请查看 pyRevit 输出窗口。",
        "no_find_text": u"查找文本不能为空。",
    },
    "en": {
        "language_message": u"Select report language / 选择报告语言",
        "alert_title": u"Yang Agent",
        "no_doc": u"No active Revit document.",
        "find_label": u"Find text",
        "replace_label": u"Replace with (leave empty to replace with empty text)",
        "case_sensitive_label": u"Case sensitivity?",
        "case_insensitive": u"Case insensitive",
        "case_sensitive_option": u"Case sensitive",
        "report_title": u"# Yang Agent Text Find & Replace Preview",
        "read_only_note": u"This is a dry-run read-only preview. No Revit model changes were made.",
        "summary_heading": u"Summary",
        "document": u"Document: {0}",
        "exported_at": u"Exported at: {0}",
        "find_text": u"Find text: {0}",
        "replace_text": u"Replace text: {0}",
        "case_sensitive": u"Case sensitive: {0}",
        "yes": u"Yes",
        "no": u"No",
        "textnotes_total": u"Total TextNotes: {0}",
        "candidate_count": u"Candidates: {0}",
        "detail_heading": u"Candidate Details",
        "view_label": u"Owner view",
        "current_label": u"Current text",
        "proposed_label": u"Proposed text",
        "next_steps_heading": u"Suggested Next Steps",
        "next_step_1": u"Review the CSV candidates before applying any changes.",
        "next_step_2": u"Confirm the replacement text before running apply.",
        "next_step_3": u"Do not modify the dry_run, element_id, or category columns in the CSV.",
        "none": u"No matching TextNotes found.",
        "output_title": u"# Yang Agent Text Find & Replace Preview",
        "output_done": u"Preview completed. No model changes were made.",
        "output_candidates": u"- Candidates: {0}",
        "output_report": u"- Report: `{0}`",
        "output_csv": u"- CSV: `{0}`",
        "alert_done": u"Text find & replace preview generated.\n\nNo model changes were made.\n\nCandidates: {0}\n\n{1}",
        "failed_title": u"# Text Find & Replace Preview failed",
        "failed_alert": u"Text Find & Replace Preview failed. See pyRevit output for details.",
        "no_find_text": u"Find text cannot be empty.",
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


def collect_candidates(textnotes, find_text, replace_text, case_sensitive):
    candidates = []
    for note in textnotes:
        note_text = safe_text(note.Text)
        if is_blank(note_text):
            continue
        if not match_text(note_text, find_text, case_sensitive):
            continue
        candidates.append({
            "dry_run": "true",
            "element_id": element_id_value(note.Id),
            "category": "TextNote",
            "current_text": note_text,
            "proposed_text": apply_replacement(note_text, find_text, replace_text, case_sensitive),
            "owner_view": get_owner_view_name(note),
        })
    return candidates


def bool_label(lang, value):
    return tr(lang, "yes") if value else tr(lang, "no")


def none_label(lang):
    return tr(lang, "none").lstrip("- ").strip()


def build_report_lines(lang, find_text, replace_text, case_sensitive, total_count, candidates):
    theme_id = get_theme_id()
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    summary_lines = [
        tr(lang, "document").format(safe_text(doc.Title)),
        tr(lang, "exported_at").format(timestamp),
        tr(lang, "find_text").format(find_text),
        tr(lang, "replace_text").format(replace_text if replace_text else none_label(lang)),
        tr(lang, "case_sensitive").format(bool_label(lang, case_sensitive)),
        tr(lang, "textnotes_total").format(total_count),
        tr(lang, "candidate_count").format(len(candidates)),
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

    if not candidates:
        lines.append(u"- {0}".format(tr(lang, "none")))
    else:
        for row in candidates:
            view_name = row["owner_view"] or u"-"
            lines.append(
                u"- `{0}` | {1}: `{2}` | {3}: `{4}` | {5}: `{6}`".format(
                    row["element_id"],
                    tr(lang, "view_label"),
                    view_name,
                    tr(lang, "current_label"),
                    row["current_text"],
                    tr(lang, "proposed_label"),
                    row["proposed_text"],
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
        "current_text",
        "proposed_text",
        "owner_view",
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


def choose_case_sensitive(lang):
    insensitive = tr(lang, "case_insensitive")
    sensitive = tr(lang, "case_sensitive_option")
    selected = forms.CommandSwitchWindow.show(
        [insensitive, sensitive],
        message=tr(lang, "case_sensitive_label"),
    )
    return selected == sensitive


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

    textnotes = collect_textnotes()
    total_count = len(textnotes)
    case_sensitive = choose_case_sensitive(lang)
    candidates = collect_candidates(textnotes, find_text, replace_text, case_sensitive)

    export_dir = get_export_dir()
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_path = os.path.join(export_dir, "text_find_replace_candidates_{0}.md".format(timestamp))
    csv_path = os.path.join(export_dir, "text_find_replace_candidates_{0}.csv".format(timestamp))

    report_lines = build_report_lines(lang, find_text, replace_text, case_sensitive, total_count, candidates)
    write_markdown(report_path, report_lines)
    write_csv(csv_path, candidates)

    output.print_md(tr(lang, "output_title"))
    output.print_md(u"")
    output.print_md(tr(lang, "output_done"))
    output.print_md(u"")
    output.print_md(tr(lang, "output_candidates").format(len(candidates)))
    output.print_md(tr(lang, "output_report").format(report_path))
    output.print_md(tr(lang, "output_csv").format(csv_path))

    forms.toast(
        tr(lang, "alert_done").format(len(candidates), report_path),
        title=tr(lang, "alert_title"),
    )


try:
    main()
except Exception:
    err = traceback.format_exc()
    output.print_md(TEXT["zh"]["failed_title"] + u" / " + TEXT["en"]["failed_title"].replace("# ", u""))
    output.print_md("```text\n{0}\n```".format(err))
    forms.alert(TEXT["zh"]["failed_alert"] + u"\n\n" + TEXT["en"]["failed_alert"], title="Yang Agent")
