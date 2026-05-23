# -*- coding: utf-8 -*-
"""Preview view naming rule issues.

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

from Autodesk.Revit.DB import FilteredElementCollector, View, ViewSheet  # noqa: E402
from pyrevit import forms, revit, script  # noqa: E402
from yang_agent_lang import get_export_dir, get_or_choose_language  # noqa: E402


doc = revit.doc
output = script.get_output()


TEXT = {
    "zh": {
        "alert_title": u"Yang Agent",
        "no_doc": u"没有打开的 Revit 文档。",
        "title": u"# Yang Agent 视图命名规则预览",
        "read_only": u"此报告为 dry-run 预览，未修改 Revit 模型。",
        "summary": u"## 汇总",
        "document": u"- 文档：{0}",
        "exported_at": u"- 导出时间：{0}",
        "views_total": u"- 可检查视图总数：{0}",
        "issue_total": u"- 命名问题数：{0}",
        "details": u"## 视图命名问题",
        "none": u"- 无",
        "next_steps": u"## 建议下一步",
        "step_1": u"1. BIM 负责人先确认公司视图命名标准。",
        "step_2": u"2. 根据项目习惯调整前缀和临时关键词规则。",
        "step_3": u"3. 只在规则稳定后再考虑生成 apply 工具。",
        "output_done": u"预览完成。此工具未修改模型。",
        "output_issues": u"- 命名问题数：{0}",
        "output_report": u"- 报告：`{0}`",
        "output_csv": u"- CSV：`{0}`",
        "alert_done": u"视图命名规则预览已生成。\n\n此工具未修改模型。\n\n命名问题数：{0}\n\n{1}",
        "failed_title": u"# 视图命名规则预览失败",
        "failed_alert": u"视图命名规则预览失败。请查看 pyRevit 输出窗口。",
    },
    "en": {
        "alert_title": u"Yang Agent",
        "no_doc": u"No active Revit document.",
        "title": u"# Yang Agent View Naming Rules Preview",
        "read_only": u"This is a dry-run preview. No Revit model changes were made.",
        "summary": u"## Summary",
        "document": u"- Document: {0}",
        "exported_at": u"- Exported at: {0}",
        "views_total": u"- Reportable views: {0}",
        "issue_total": u"- Naming issues: {0}",
        "details": u"## View Naming Issues",
        "none": u"- None",
        "next_steps": u"## Suggested Next Steps",
        "step_1": u"1. Confirm company view naming standards with the BIM lead.",
        "step_2": u"2. Adjust prefixes and temporary keywords based on project habits.",
        "step_3": u"3. Generate apply tools only after the rules are stable.",
        "output_done": u"Preview completed. No model changes were made.",
        "output_issues": u"- Naming issues: {0}",
        "output_report": u"- Report: `{0}`",
        "output_csv": u"- CSV: `{0}`",
        "alert_done": u"View naming rules preview generated.\n\nNo model changes were made.\n\nNaming issues: {0}\n\n{1}",
        "failed_title": u"# View Naming Rules Preview failed",
        "failed_alert": u"View Naming Rules Preview failed. See pyRevit output for details.",
    },
}


PREFIX_BY_VIEW_TYPE = {
    "FloorPlan": ["FP-", "PL-", "A-", "S-", "M-", "E-"],
    "CeilingPlan": ["RCP-", "CP-"],
    "Section": ["SEC-", "SECTION-"],
    "Elevation": ["EL-", "ELEV-"],
    "ThreeD": ["3D-"],
    "DraftingView": ["DR-", "DET-", "DT-"],
    "Legend": ["LG-", "LEG-"],
    "AreaPlan": ["AR-", "AREA-"],
    "EngineeringPlan": ["EP-", "ENG-"],
}

TEMP_KEYWORDS = [
    u"临时",
    u"测试",
    u"工作",
    u"temp",
    u"test",
    u"working",
    u"copy",
    u"复制",
]


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


def is_reportable_view(view):
    if view is None:
        return False
    try:
        if view.IsTemplate:
            return False
    except Exception:
        return False
    if isinstance(view, ViewSheet):
        return False

    view_type = safe_text(view.ViewType)
    return view_type in PREFIX_BY_VIEW_TYPE


def get_naming_issue(view_name, view_type):
    name = safe_text(view_name).strip()
    if is_blank(name):
        return "BlankName", ""

    lowered = name.lower()
    for keyword in TEMP_KEYWORDS:
        if safe_text(keyword).lower() in lowered:
            return "TemporaryKeyword", safe_text(keyword)

    prefixes = PREFIX_BY_VIEW_TYPE.get(view_type, [])
    upper_name = name.upper()
    for prefix in prefixes:
        if upper_name.startswith(prefix):
            return "", ""
    return "MissingRecommendedPrefix", u"|".join(prefixes)


def collect_preview_rows():
    views = FilteredElementCollector(doc).OfClass(View).ToElements()
    reportable_count = 0
    issues = []

    for view in views:
        if not is_reportable_view(view):
            continue

        reportable_count += 1
        view_type = safe_text(view.ViewType)
        view_name = safe_text(view.Name)
        issue_type, expected = get_naming_issue(view_name, view_type)
        if not issue_type:
            continue

        issues.append({
            "dry_run": "true",
            "element_id": element_id_value(view.Id),
            "category": "View",
            "view_name": view_name,
            "view_type": view_type,
            "issue_type": issue_type,
            "expected_rule": expected,
            "status": "NamingIssue",
        })

    return reportable_count, issues


def write_markdown(path, lang, reportable_count, issues):
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
    lines.append(tr(lang, "views_total").format(reportable_count))
    lines.append(tr(lang, "issue_total").format(len(issues)))
    lines.append(u"")
    lines.append(tr(lang, "details"))
    lines.append(u"")

    if not issues:
        lines.append(tr(lang, "none"))
    else:
        for row in issues:
            lines.append(
                u"- `{0}` {1} | {2} | {3} | {4}".format(
                    row["element_id"],
                    row["view_type"],
                    row["view_name"],
                    row["issue_type"],
                    row["expected_rule"],
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
    lang = get_or_choose_language(forms)

    if doc is None:
        forms.alert(tr(lang, "no_doc"), title=tr(lang, "alert_title"))
        return

    export_dir = get_export_dir()
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_path = os.path.join(export_dir, "view_naming_rules_{0}.md".format(timestamp))
    csv_path = os.path.join(export_dir, "view_naming_rules_{0}.csv".format(timestamp))

    reportable_count, issues = collect_preview_rows()
    write_markdown(report_path, lang, reportable_count, issues)
    write_csv(csv_path, issues)

    output.print_md(tr(lang, "title"))
    output.print_md(u"")
    output.print_md(tr(lang, "output_done"))
    output.print_md(u"")
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
