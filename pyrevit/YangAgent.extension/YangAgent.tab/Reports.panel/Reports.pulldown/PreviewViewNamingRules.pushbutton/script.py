# -*- coding: utf-8 -*-
"""Preview view naming rule issues in read-only dry-run mode."""

from __future__ import print_function

import codecs
import csv
import os
import traceback
from datetime import datetime

import clr

clr.AddReference("RevitAPI")
clr.AddReference("RevitAPIUI")

from Autodesk.Revit.DB import FilteredElementCollector, View, ViewSheet  # noqa: E402
from pyrevit import forms, revit, script  # noqa: E402
from yang_agent_lang import get_or_choose_language, get_view_naming_rules  # noqa: E402
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
        "report_title": u"# Yang Agent 预览视图命名规则",
        "read_only_note": u"这是 dry-run 只读预览，不会修改 Revit 模型。",
        "summary_heading": u"统计摘要",
        "document": u"文档：{0}",
        "exported_at": u"导出时间：{0}",
        "views_total": u"纳入检查的视图数量：{0}",
        "issue_total": u"命名问题数量：{0}",
        "detail_heading": u"视图命名问题明细",
        "expected_rule": u"建议规则",
        "next_steps_heading": u"建议下一步",
        "next_step_1": u"先确认项目当前使用的视图命名前缀，再决定是否统一整改。",
        "next_step_2": u"临时视图、测试视图和工作视图建议先人工分类，不要直接自动改名。",
        "next_step_3": u"只有在命名规则稳定后，才适合继续生成 apply 工具。",
        "none": u"无",
        "output_title": u"# Yang Agent 预览视图命名规则",
        "output_done": u"预览完成。该工具未修改模型。",
        "output_issues": u"- 命名问题数量：{0}",
        "output_report": u"- 报告：`{0}`",
        "output_csv": u"- CSV：`{0}`",
        "alert_done": u"视图命名规则预览已生成。\n\n该工具未修改模型。\n\n命名问题数量：{0}\n\n{1}",
        "failed_title": u"# 视图命名规则预览失败",
        "failed_alert": u"视图命名规则预览失败。请查看 pyRevit 输出窗口。",
    },
    "en": {
        "language_message": u"Select report language / 选择报告语言",
        "alert_title": u"Yang Agent",
        "no_doc": u"No active Revit document.",
        "report_title": u"# Yang Agent View Naming Rules Preview",
        "read_only_note": u"This is a dry-run read-only preview. No Revit model changes were made.",
        "summary_heading": u"Summary",
        "document": u"Document: {0}",
        "exported_at": u"Exported at: {0}",
        "views_total": u"Views checked: {0}",
        "issue_total": u"Naming issues: {0}",
        "detail_heading": u"View Naming Issue Details",
        "expected_rule": u"Suggested rule",
        "next_steps_heading": u"Suggested Next Steps",
        "next_step_1": u"Confirm the current project naming prefixes before attempting any cleanup.",
        "next_step_2": u"Temporary, test, and working views should be reviewed manually before any rename automation.",
        "next_step_3": u"Only generate apply tools after naming rules are stable.",
        "none": u"None",
        "output_title": u"# Yang Agent View Naming Rules Preview",
        "output_done": u"Preview completed. No model changes were made.",
        "output_issues": u"- Naming issues: {0}",
        "output_report": u"- Report: `{0}`",
        "output_csv": u"- CSV: `{0}`",
        "alert_done": u"View naming rules preview generated.\n\nNo model changes were made.\n\nNaming issues: {0}\n\n{1}",
        "failed_title": u"# View Naming Rules Preview failed",
        "failed_alert": u"View Naming Rules Preview failed. See pyRevit output for details.",
    },
}


FALLBACK_TEMPORARY_KEYWORDS = [
    u"临时",
    u"测试",
    u"工作",
    u"复制",
    u"temp",
    u"test",
    u"working",
    u"copy",
]


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


def get_effective_rules():
    rules = get_view_naming_rules()
    keywords = []
    seen = set()
    for keyword in list(rules.get("temporary_keywords", [])) + FALLBACK_TEMPORARY_KEYWORDS:
        text = safe_text(keyword).strip()
        lowered = text.lower()
        if text and lowered not in seen:
            keywords.append(text)
            seen.add(lowered)
    return {
        "prefix_by_view_type": rules.get("prefix_by_view_type", {}),
        "temporary_keywords": keywords,
    }


def is_reportable_view(view, rules):
    if view is None:
        return False
    try:
        if view.IsTemplate:
            return False
    except Exception:
        return False
    if isinstance(view, ViewSheet):
        return False
    return safe_text(view.ViewType) in rules["prefix_by_view_type"]


def get_naming_issue(view_name, view_type, rules):
    name = safe_text(view_name).strip()
    if is_blank(name):
        return "BlankName", ""

    lowered = name.lower()
    for keyword in rules["temporary_keywords"]:
        keyword_text = safe_text(keyword).strip()
        if keyword_text and keyword_text.lower() in lowered:
            return "TemporaryKeyword", keyword_text

    prefixes = rules["prefix_by_view_type"].get(view_type, [])
    upper_name = name.upper()
    for prefix in prefixes:
        if upper_name.startswith(safe_text(prefix).upper()):
            return "", ""
    return "MissingRecommendedPrefix", u"|".join([safe_text(prefix) for prefix in prefixes])


def collect_preview_rows():
    rules = get_effective_rules()
    issues = []
    reportable_count = 0
    views = FilteredElementCollector(doc).OfClass(View).ToElements()
    for view in views:
        if not is_reportable_view(view, rules):
            continue

        reportable_count += 1
        view_type = safe_text(view.ViewType)
        view_name = safe_text(view.Name)
        issue_type, expected = get_naming_issue(view_name, view_type, rules)
        if not issue_type:
            continue

        issues.append(
            {
                "dry_run": "true",
                "element_id": element_id_value(view.Id),
                "category": "View",
                "view_name": view_name,
                "view_type": view_type,
                "issue_type": issue_type,
                "expected_rule": expected,
                "status": "NamingIssue",
            }
        )
    return reportable_count, issues


def build_report_lines(lang, reportable_count, issues):
    theme_id = get_theme_id()
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    summary_lines = [
        tr(lang, "document").format(safe_text(doc.Title)),
        tr(lang, "exported_at").format(timestamp),
        tr(lang, "views_total").format(reportable_count),
        tr(lang, "issue_total").format(len(issues)),
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

    if not issues:
        lines.append(u"- {0}".format(tr(lang, "none")))
    else:
        for row in issues:
            lines.append(
                u"- ElementId `{0}` | {1} | {2} | {3}: `{4}`".format(
                    row["element_id"],
                    row["view_type"] or tr(lang, "none"),
                    row["view_name"] or tr(lang, "none"),
                    row["issue_type"],
                    row["expected_rule"] or tr(lang, "none"),
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
        "view_name",
        "view_type",
        "issue_type",
        "expected_rule",
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
    report_path = os.path.join(export_dir, "view_naming_rules_{0}.md".format(timestamp))
    csv_path = os.path.join(export_dir, "view_naming_rules_{0}.csv".format(timestamp))

    reportable_count, issues = collect_preview_rows()
    write_markdown(report_path, build_report_lines(lang, reportable_count, issues))
    write_csv(csv_path, issues)

    output.print_md(tr(lang, "output_title"))
    output.print_md(u"")
    output.print_md(tr(lang, "output_done"))
    output.print_md(tr(lang, "output_issues").format(len(issues)))
    output.print_md(tr(lang, "output_report").format(report_path))
    output.print_md(tr(lang, "output_csv").format(csv_path))

    forms.toast(
        tr(lang, "alert_done").format(len(issues), report_path),
        title=tr(lang, "alert_title"),
    )


try:
    main()
except Exception:
    err = traceback.format_exc()
    output.print_md(TEXT["zh"]["failed_title"] + u" / " + TEXT["en"]["failed_title"].replace("# ", u""))
    output.print_md("```text\n{0}\n```".format(err))
    forms.alert(TEXT["zh"]["failed_alert"] + u"\n\n" + TEXT["en"]["failed_alert"], title="Yang Agent")
