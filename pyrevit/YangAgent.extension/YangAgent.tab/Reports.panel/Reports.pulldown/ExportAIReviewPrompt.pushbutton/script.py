# -*- coding: utf-8 -*-
"""Export a safe AI review prompt for YangAgent reports.

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


REPORT_EXTENSIONS = [".md", ".json", ".csv"]
MAX_RECENT_FILES = 20


TEXT = {
    "zh": {
        "alert_title": u"Yang Agent",
        "no_doc": u"没有打开的 Revit 文档。",
        "title": u"# Yang Agent AI 分析提示词",
        "read_only": u"此文件用于把 Revit 报告交给 AI 分析，未修改 Revit 模型。",
        "summary": u"## 基本信息",
        "document": u"- 文档：{0}",
        "exported_at": u"- 生成时间：{0}",
        "export_dir": u"- 报告目录：`{0}`",
        "recent_files": u"## 最近报告文件",
        "no_files": u"- 未找到 `.md`、`.json` 或 `.csv` 报告文件。",
        "prompt_title": u"## 可直接复制给 AI 的提示词",
        "prompt": u"""请分析这些 YangAgent Revit 报告文件，按严重程度列出问题和建议。

要求：
1. 只做分析和建议，不要生成会直接修改 Revit 模型的脚本。
2. 如果需要修复方案，先给 dry-run 方案，只预览会影响哪些元素。
3. 明确区分高风险、中风险、低风险问题。
4. 说明每个建议需要参考哪个报告文件或 CSV 字段。
5. 如果信息不足，请列出需要我在 Revit 中继续导出的报告。

我会把以下报告文件内容粘贴给你，请等待我提供文件内容后再分析。""",
        "output_done": u"AI 分析提示词已生成。此工具未修改模型。",
        "output_report": u"- 提示词：`{0}`",
        "alert_done": u"AI 分析提示词已生成。\n\n此工具未修改模型。\n\n{0}",
        "failed_title": u"# AI 分析提示词生成失败",
        "failed_alert": u"AI 分析提示词生成失败。请查看 pyRevit 输出窗口。",
    },
    "en": {
        "alert_title": u"Yang Agent",
        "no_doc": u"No active Revit document.",
        "title": u"# Yang Agent AI Review Prompt",
        "read_only": u"This file helps you send Revit reports to AI for review. No Revit model changes were made.",
        "summary": u"## Basic Information",
        "document": u"- Document: {0}",
        "exported_at": u"- Exported at: {0}",
        "export_dir": u"- Report directory: `{0}`",
        "recent_files": u"## Recent Report Files",
        "no_files": u"- No `.md`, `.json`, or `.csv` report files were found.",
        "prompt_title": u"## Prompt To Copy Into AI",
        "prompt": u"""Please analyze these YangAgent Revit report files and list issues and recommendations by severity.

Requirements:
1. Only provide analysis and recommendations. Do not generate scripts that directly modify the Revit model.
2. If a fix is needed, propose a dry-run approach first that previews affected elements.
3. Clearly separate high-risk, medium-risk, and low-risk issues.
4. Reference the report file or CSV field behind each recommendation.
5. If more information is needed, list which Revit reports I should export next.

I will paste the report contents below. Please wait for the file contents before analyzing.""",
        "output_done": u"AI review prompt generated. No model changes were made.",
        "output_report": u"- Prompt: `{0}`",
        "alert_done": u"AI review prompt generated.\n\nNo model changes were made.\n\n{0}",
        "failed_title": u"# AI Review Prompt failed",
        "failed_alert": u"AI Review Prompt failed. See pyRevit output for details.",
    },
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


def collect_recent_report_files(export_dir):
    files = []
    try:
        names = os.listdir(export_dir)
    except Exception:
        return files

    for name in names:
        path = os.path.join(export_dir, name)
        if not os.path.isfile(path):
            continue
        ext = os.path.splitext(name)[1].lower()
        if ext not in REPORT_EXTENSIONS:
            continue
        try:
            modified_at = os.path.getmtime(path)
            size = os.path.getsize(path)
        except Exception:
            modified_at = 0
            size = 0
        files.append({
            "name": safe_text(name),
            "path": safe_text(path),
            "modified_at": modified_at,
            "size": size,
        })

    files.sort(key=lambda item: item.get("modified_at", 0), reverse=True)
    return files[:MAX_RECENT_FILES]


def format_size(size):
    try:
        size = float(size)
    except Exception:
        return u""
    if size >= 1024 * 1024:
        return u"{0:.1f} MB".format(size / 1024.0 / 1024.0)
    if size >= 1024:
        return u"{0:.1f} KB".format(size / 1024.0)
    return u"{0:.0f} B".format(size)


def format_time(timestamp):
    try:
        return datetime.fromtimestamp(timestamp).strftime("%Y-%m-%d %H:%M:%S")
    except Exception:
        return u""


def write_markdown(path, lang, export_dir, recent_files):
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
    lines.append(tr(lang, "export_dir").format(export_dir))
    lines.append(u"")
    lines.append(tr(lang, "recent_files"))
    lines.append(u"")

    if not recent_files:
        lines.append(tr(lang, "no_files"))
    else:
        for file_info in recent_files:
            lines.append(
                u"- `{0}` | {1} | {2}".format(
                    file_info["path"],
                    format_time(file_info["modified_at"]),
                    format_size(file_info["size"]),
                )
            )

    lines.append(u"")
    lines.append(tr(lang, "prompt_title"))
    lines.append(u"")
    lines.append(u"```text")
    lines.append(tr(lang, "prompt"))
    lines.append(u"```")

    with codecs.open(path, "w", "utf-8-sig") as stream:
        stream.write(u"\n".join(lines))


def main():
    lang = get_or_choose_language(forms)

    if doc is None:
        forms.alert(tr(lang, "no_doc"), title=tr(lang, "alert_title"))
        return

    export_dir = get_export_dir()
    recent_files = collect_recent_report_files(export_dir)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_path = os.path.join(export_dir, "yangagent_ai_review_prompt_{0}.md".format(timestamp))

    write_markdown(report_path, lang, export_dir, recent_files)

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
