# -*- coding: utf-8 -*-
"""Export a read-only YangAgent regression checklist."""

from __future__ import print_function

import codecs
import os
import traceback
from datetime import datetime

from pyrevit import forms, revit, script
from yang_agent_lang import get_or_choose_language
from yang_agent_report_style import build_intro_block, build_status_block
from yang_agent_settings import get_export_dir
from yang_agent_theme import get_theme_id


doc = revit.doc
output = script.get_output()


TEXT = {
    "zh": {
        "language_message": u"选择报告语言 / Select report language",
        "alert_title": u"Yang Agent",
        "no_doc": u"没有打开的 Revit 文档。",
        "report_title": u"# Yang Agent 回归测试清单",
        "read_only_note": u"此清单只用于测试记录，未修改 Revit 模型。",
        "summary": u"## 基本信息",
        "document": u"- 文档：{0}",
        "exported_at": u"- 导出时间：{0}",
        "tester": u"- 测试人：",
        "revit_version": u"- Revit 版本：{0}",
        "pyrevit_version": u"- pyRevit 版本：手动填写",
        "model_type": u"- 测试模型：`*_test.rvt` 或 `*_sandbox.rvt`",
        "rules_title": u"测试规则",
        "rules": u"## 测试规则",
        "rule_1": u"- 禁止在中心模型或正式项目模型上测试修改工具。",
        "rule_2": u"- Apply 工具必须先有 dry-run CSV，并人工检查 CSV。",
        "rule_3": u"- Apply 后必须确认可以通过 Revit Undo 撤销。",
        "checklist": u"## 工具测试清单",
        "expected": u"预期结果",
        "result": u"结果",
        "notes": u"备注",
        "output_title": u"# Yang Agent 回归测试清单",
        "output_done": u"回归测试清单生成完成。此工具未修改模型。",
        "output_report": u"- 清单文件：`{0}`",
        "alert_done": u"回归测试清单已生成。\n\n此工具未修改模型。\n\n{0}",
        "failed_title": u"# 回归测试清单生成失败",
        "failed_alert": u"回归测试清单生成失败。请查看 pyRevit 输出窗口。",
    },
    "en": {
        "language_message": u"Select report language / 选择报告语言",
        "alert_title": u"Yang Agent",
        "no_doc": u"No active Revit document.",
        "report_title": u"# Yang Agent Regression Test Checklist",
        "read_only_note": u"This checklist is for test recording only. No Revit model changes were made.",
        "summary": u"## Basic Information",
        "document": u"- Document: {0}",
        "exported_at": u"- Exported at: {0}",
        "tester": u"- Tester:",
        "revit_version": u"- Revit version: {0}",
        "pyrevit_version": u"- pyRevit version: fill manually",
        "model_type": u"- Test model: `*_test.rvt` or `*_sandbox.rvt`",
        "rules_title": u"Test Rules",
        "rules": u"## Test Rules",
        "rule_1": u"- Do not test modification tools on central or production project models.",
        "rule_2": u"- Apply tools require a dry-run CSV that has been manually reviewed.",
        "rule_3": u"- After Apply, confirm Revit can undo the change.",
        "checklist": u"## Tool Test Checklist",
        "expected": u"Expected result",
        "result": u"Result",
        "notes": u"Notes",
        "output_title": u"# Yang Agent Regression Test Checklist",
        "output_done": u"Regression checklist completed. No model changes were made.",
        "output_report": u"- Checklist file: `{0}`",
        "alert_done": u"Regression checklist generated.\n\nNo model changes were made.\n\n{0}",
        "failed_title": u"# Regression Test Checklist failed",
        "failed_alert": u"Regression Test Checklist failed. See pyRevit output for details.",
    },
}


CHECKS = {
    "zh": [
        (u"System Settings", u"窗口可打开，语言、主题、用户资料和视图命名规则可保存"),
        (u"Report Export Path", u"可选择报告目录，后续报告写入该目录"),
        (u"Project Info Report", u"生成 `project_info_report_*.md`"),
        (u"Export Model Snapshot", u"生成快照 Markdown、JSON 以及 rooms / doors_windows / sheets_views CSV"),
        (u"Model Health Report", u"生成 `model_health_report_*.md`"),
        (u"AI Review Prompt", u"生成可复制给 AI 的只读提示包"),
        (u"Preview Missing Marks", u"生成缺失门窗标记报告与 CSV，不修改模型"),
        (u"Apply Door/Window Marks", u"读取人工确认后的 CSV，写入后可 Undo"),
        (u"Preview Missing Room Numbers", u"生成缺失房间编号报告与 CSV，不修改模型"),
        (u"Apply Room Numbers", u"读取人工确认后的 CSV，写入后可 Undo"),
        (u"Preview Duplicate Room Numbers", u"生成重复房间编号报告与 CSV，不修改模型"),
        (u"Preview Unplaced Views", u"生成未上图视图报告与 CSV，不修改模型"),
    ],
    "en": [
        (u"System Settings", u"Window opens and language, theme, profile, and view naming rules can be saved"),
        (u"Report Export Path", u"Can choose export folder and later reports are written there"),
        (u"Project Info Report", u"Generates `project_info_report_*.md`"),
        (u"Export Model Snapshot", u"Generates snapshot Markdown, JSON, and rooms / doors_windows / sheets_views CSV"),
        (u"Model Health Report", u"Generates `model_health_report_*.md`"),
        (u"AI Review Prompt", u"Generates a read-only prompt package for AI review"),
        (u"Preview Missing Marks", u"Generates missing door/window mark report and CSV without modifying the model"),
        (u"Apply Door/Window Marks", u"Reads reviewed CSV, writes values, and can be undone"),
        (u"Preview Missing Room Numbers", u"Generates missing room number report and CSV without modifying the model"),
        (u"Apply Room Numbers", u"Reads reviewed CSV, writes values, and can be undone"),
        (u"Preview Duplicate Room Numbers", u"Generates duplicate room number report and CSV without modifying the model"),
        (u"Preview Unplaced Views", u"Generates unplaced views report and CSV without modifying the model"),
    ],
}


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


def choose_language():
    try:
        return get_or_choose_language(forms, message=TEXT["zh"]["language_message"])
    except Exception:
        return "zh"


def get_revit_version():
    try:
        return safe_text(revit.app.VersionName)
    except Exception:
        return u""


def build_lines(lang):
    theme_id = get_theme_id()
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    lines = []
    lines.append(build_intro_block(theme_id, tr(lang, "report_title"), tr(lang, "read_only_note")))
    lines.append(u"")
    lines.append(tr(lang, "summary"))
    lines.append(u"")
    lines.append(tr(lang, "document").format(safe_text(doc.Title)))
    lines.append(tr(lang, "exported_at").format(timestamp))
    lines.append(tr(lang, "tester"))
    lines.append(tr(lang, "revit_version").format(get_revit_version()))
    lines.append(tr(lang, "pyrevit_version"))
    lines.append(tr(lang, "model_type"))
    lines.append(u"")
    lines.append(build_status_block(
        theme_id,
        tr(lang, "rules_title"),
        [tr(lang, "rule_1"), tr(lang, "rule_2"), tr(lang, "rule_3")],
    ))
    lines.append(u"")
    lines.append(tr(lang, "checklist"))
    lines.append(u"")
    lines.append(u"| # | Tool | {0} | {1} | {2} |".format(tr(lang, "expected"), tr(lang, "result"), tr(lang, "notes")))
    lines.append(u"|---:|---|---|---|---|")
    index = 1
    for tool_name, expected in CHECKS.get(lang, CHECKS["zh"]):
        lines.append(u"| {0} | {1} | {2} | Pass / Fail | |".format(index, tool_name, expected))
        index += 1
    return lines


def write_report(path, lines):
    with codecs.open(path, "w", "utf-8-sig") as stream:
        stream.write(u"\n".join(lines))


def main():
    lang = choose_language()
    if doc is None:
        forms.alert(tr(lang, "no_doc"), title=tr(lang, "alert_title"))
        return

    export_dir = get_export_dir()
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_path = os.path.join(export_dir, "yangagent_regression_checklist_{0}.md".format(timestamp))

    lines = build_lines(lang)
    write_report(report_path, lines)

    output.print_md(tr(lang, "output_title"))
    output.print_md(u"")
    output.print_md(tr(lang, "output_done"))
    output.print_md(tr(lang, "output_report").format(report_path))

    forms.toast(tr(lang, "alert_done").format(report_path), title=tr(lang, "alert_title"))


try:
    main()
except Exception:
    err = traceback.format_exc()
    output.print_md(TEXT["zh"]["failed_title"] + u" / " + TEXT["en"]["failed_title"].replace("# ", u""))
    output.print_md("```text\n{0}\n```".format(err))
    forms.alert(TEXT["zh"]["failed_alert"] + u"\n\n" + TEXT["en"]["failed_alert"], title="Yang Agent")
