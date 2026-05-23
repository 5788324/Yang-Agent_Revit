# -*- coding: utf-8 -*-
"""Export a standard YangAgent regression test checklist.

This tool is read-only. It does not modify the model and does not open a Transaction.
"""

from __future__ import print_function

import codecs
import os
import traceback
from datetime import datetime

import clr

clr.AddReference("RevitAPI")
clr.AddReference("RevitAPIUI")

from pyrevit import forms, revit, script  # noqa: E402
from yang_agent_lang import get_export_dir, get_or_choose_language  # noqa: E402


doc = revit.doc
output = script.get_output()


TEXT = {
    "zh": {
        "alert_title": u"Yang Agent",
        "no_doc": u"没有打开的 Revit 文档。",
        "title": u"# Yang Agent 回归测试清单",
        "read_only": u"此清单为测试记录模板，未修改 Revit 模型。",
        "summary": u"## 基本信息",
        "document": u"- 文档：{0}",
        "exported_at": u"- 导出时间：{0}",
        "tester": u"- 测试人：",
        "revit_version": u"- Revit 版本：",
        "pyrevit_version": u"- pyRevit 版本：",
        "model_type": u"- 测试模型：`*_test.rvt` 或 `*_sandbox.rvt`",
        "rules": u"## 测试规则",
        "rule_1": u"- 禁止在中心模型或正式项目模型上测试修改工具。",
        "rule_2": u"- Apply 工具必须先有 dry-run CSV，并且人工检查 CSV。",
        "rule_3": u"- Apply 后必须确认可以通过 Revit 撤销。",
        "checklist": u"## 工具测试清单",
        "expected": u"预期结果",
        "result": u"结果",
        "notes": u"备注",
        "output_done": u"回归测试清单已生成。此工具未修改模型。",
        "output_report": u"- 清单：`{0}`",
        "alert_done": u"回归测试清单已生成。\n\n此工具未修改模型。\n\n{0}",
        "failed_title": u"# 回归测试清单生成失败",
        "failed_alert": u"回归测试清单生成失败。请查看 pyRevit 输出窗口。",
    },
    "en": {
        "alert_title": u"Yang Agent",
        "no_doc": u"No active Revit document.",
        "title": u"# Yang Agent Regression Test Checklist",
        "read_only": u"This checklist is a test record template. No Revit model changes were made.",
        "summary": u"## Basic Information",
        "document": u"- Document: {0}",
        "exported_at": u"- Exported at: {0}",
        "tester": u"- Tester:",
        "revit_version": u"- Revit version:",
        "pyrevit_version": u"- pyRevit version:",
        "model_type": u"- Test model: `*_test.rvt` or `*_sandbox.rvt`",
        "rules": u"## Test Rules",
        "rule_1": u"- Do not test modification tools on central or production project models.",
        "rule_2": u"- Apply tools require a dry-run CSV that has been manually reviewed.",
        "rule_3": u"- After Apply, confirm Revit can undo the change.",
        "checklist": u"## Tool Test Checklist",
        "expected": u"Expected result",
        "result": u"Result",
        "notes": u"Notes",
        "output_done": u"Regression test checklist generated. No model changes were made.",
        "output_report": u"- Checklist: `{0}`",
        "alert_done": u"Regression test checklist generated.\n\nNo model changes were made.\n\n{0}",
        "failed_title": u"# Regression Test Checklist failed",
        "failed_alert": u"Regression Test Checklist failed. See pyRevit output for details.",
    },
}


CHECKS = {
    "zh": [
        (u"系统设置", u"可以打开窗口，语言、主题、用户信息和视图命名规则可保存"),
        (u"导出路径", u"可以选择报告目录，后续报告写入该目录"),
        (u"导出模型快照", u"生成 JSON 和 rooms/doors_windows/sheets_views CSV"),
        (u"模型健康报告", u"生成 model_health_report_*.md"),
        (u"预览缺失标记", u"生成 missing_door_window_marks_*.md 和 .csv，不修改模型"),
        (u"应用门窗标记", u"读取人工确认的 missing_door_window_marks_*.csv，可写入并可撤销"),
        (u"预览缺失房间编号", u"生成 missing_room_numbers_*.md 和 .csv，不修改模型"),
        (u"应用房间编号", u"读取人工确认的 missing_room_numbers_*.csv，可写入并可撤销"),
        (u"预览重复房间编号", u"生成 duplicate_room_numbers_*.md 和 .csv，不修改模型"),
        (u"预览未上图视图", u"生成 unplaced_views_*.md 和 .csv，不修改模型"),
        (u"预览视图命名", u"生成 view_naming_rules_*.md 和 .csv，并使用系统设置中的规则"),
        (u"English 语言检查", u"切换 English 后，报告和提示显示英文"),
    ],
    "en": [
        (u"System Settings", u"Window opens; language, theme, profile, and view naming rules can be saved"),
        (u"Report Export Path", u"Can choose report directory; later reports are written there"),
        (u"Export Model Snapshot", u"Generates JSON and rooms/doors_windows/sheets_views CSV files"),
        (u"Model Health Report", u"Generates model_health_report_*.md"),
        (u"Preview Missing Marks", u"Generates missing_door_window_marks_*.md and .csv without modifying the model"),
        (u"Apply Door/Window Marks", u"Reads reviewed missing_door_window_marks_*.csv, writes values, and can be undone"),
        (u"Preview Missing Room Numbers", u"Generates missing_room_numbers_*.md and .csv without modifying the model"),
        (u"Apply Room Numbers", u"Reads reviewed missing_room_numbers_*.csv, writes values, and can be undone"),
        (u"Preview Duplicate Room Numbers", u"Generates duplicate_room_numbers_*.md and .csv without modifying the model"),
        (u"Preview Unplaced Views", u"Generates unplaced_views_*.md and .csv without modifying the model"),
        (u"Preview View Naming Rules", u"Generates view_naming_rules_*.md and .csv using System Settings rules"),
        (u"Chinese language check", u"After switching to Chinese, reports and prompts display Chinese"),
    ],
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


def get_app_version():
    try:
        return safe_text(revit.app.VersionName)
    except Exception:
        return u""


def write_markdown(path, lang):
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
    lines.append(tr(lang, "tester"))
    lines.append(tr(lang, "revit_version") + u" " + get_app_version())
    lines.append(tr(lang, "pyrevit_version"))
    lines.append(tr(lang, "model_type"))
    lines.append(u"")
    lines.append(tr(lang, "rules"))
    lines.append(u"")
    lines.append(tr(lang, "rule_1"))
    lines.append(tr(lang, "rule_2"))
    lines.append(tr(lang, "rule_3"))
    lines.append(u"")
    lines.append(tr(lang, "checklist"))
    lines.append(u"")
    lines.append(u"| # | Tool | {0} | {1} | {2} |".format(tr(lang, "expected"), tr(lang, "result"), tr(lang, "notes")))
    lines.append(u"|---:|---|---|---|---|")

    index = 1
    for tool_name, expected in CHECKS.get(lang, CHECKS["zh"]):
        lines.append(u"| {0} | {1} | {2} | Pass / Fail | |".format(index, tool_name, expected))
        index += 1

    with codecs.open(path, "w", "utf-8-sig") as stream:
        stream.write(u"\n".join(lines))


def main():
    lang = get_or_choose_language(forms)

    if doc is None:
        forms.alert(tr(lang, "no_doc"), title=tr(lang, "alert_title"))
        return

    export_dir = get_export_dir()
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_path = os.path.join(export_dir, "yangagent_regression_checklist_{0}.md".format(timestamp))

    write_markdown(report_path, lang)

    output.print_md(tr(lang, "title"))
    output.print_md(u"")
    output.print_md(tr(lang, "output_done"))
    output.print_md(u"")
    output.print_md(tr(lang, "output_report").format(report_path))

    forms.toast(
        tr(lang, "alert_done").format(report_path),
        title=tr(lang, "alert_title"),
    )


try:
    main()
except Exception:
    err = traceback.format_exc()
    output.print_md(TEXT["zh"]["failed_title"] + u" / " + TEXT["en"]["failed_title"].replace("# ", u""))
    output.print_md("```text\n{0}\n```".format(err))
    forms.alert(TEXT["zh"]["failed_alert"] + u"\n\n" + TEXT["en"]["failed_alert"], title="Yang Agent")
