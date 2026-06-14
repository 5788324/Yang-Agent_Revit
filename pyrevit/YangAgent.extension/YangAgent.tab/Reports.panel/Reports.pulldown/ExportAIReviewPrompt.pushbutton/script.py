# -*- coding: utf-8 -*-
"""Export a read-only AI review prompt package for YangAgent reports."""

from __future__ import print_function

import codecs
import os
import traceback
from datetime import datetime

from pyrevit import forms, revit, script
from yang_agent_lang import (
    get_agent_preferences,
    get_or_choose_language,
    read_company_standards,
)
from yang_agent_report_style import build_intro_block, build_status_block
from yang_agent_settings import get_export_dir
from yang_agent_theme import get_theme_id


doc = revit.doc
output = script.get_output()


REPORT_EXTENSIONS = [".md", ".json", ".csv"]
MAX_RECENT_FILES = 20


TEXT = {
    "zh": {
        "language_message": u"选择报告语言 / Select report language",
        "alert_title": u"Yang Agent",
        "no_doc": u"没有打开的 Revit 文档。",
        "report_title": u"# Yang Agent AI 审查提示包",
        "read_only_note": u"此工具只整理只读报告上下文，未修改 Revit 模型。",
        "document_info": u"## 文档信息",
        "document": u"- 文档：{0}",
        "exported_at": u"- 导出时间：{0}",
        "export_dir": u"- 报告目录：`{0}`",
        "preferences_title": u"用户偏好",
        "revit_versions": u"- 常用 Revit 版本：{0}",
        "workflow": u"- 默认工作流：{0}",
        "review_focus": u"- 分析重点：{0}",
        "safety_notes": u"- 安全偏好：{0}",
        "company_title": u"公司标准",
        "company_standards": u"## 公司标准",
        "company_path": u"- 标准文件：`{0}`",
        "company_missing": u"- 未找到公司标准文件，可在 System Settings 中指定本地 Markdown 文件。",
        "recent_title": u"最近导出的报告",
        "recent_files": u"## 最近导出的报告",
        "recent_empty": u"- 当前目录下没有 `.md`、`.json` 或 `.csv` 报告文件。",
        "recent_item": u"- `{0}` | {1} | {2}",
        "prompt_title": u"## 可复制给 AI 的提示词",
        "prompt_heading": u"AI 提示词",
        "prompt_body": u"""请分析我随后粘贴的 YangAgent Revit 报告内容，并按严重程度给出问题与建议。

要求：
1. 只做分析和建议，不要直接生成会修改 Revit 模型的脚本。
2. 如需修复方案，先给 dry-run 方案，再说明影响范围。
3. 明确区分高风险、中风险、低风险问题。
4. 每条建议要引用对应的报告文件或机器字段。
5. 如果信息不足，请列出下一步需要导出的报告。""",
        "output_title": u"# Yang Agent AI 审查提示包",
        "output_done": u"AI 审查提示包生成完成。此工具未修改模型。",
        "output_report": u"- 输出文件：`{0}`",
        "alert_done": u"AI 审查提示包已生成。\n\n此工具未修改模型。\n\n{0}",
        "failed_title": u"# AI 审查提示包生成失败",
        "failed_alert": u"AI 审查提示包生成失败。请查看 pyRevit 输出窗口。",
    },
    "en": {
        "language_message": u"Select report language / 选择报告语言",
        "alert_title": u"Yang Agent",
        "no_doc": u"No active Revit document.",
        "report_title": u"# Yang Agent AI Review Prompt Package",
        "read_only_note": u"This tool only packages read-only report context. No Revit model changes were made.",
        "document_info": u"## Document Info",
        "document": u"- Document: {0}",
        "exported_at": u"- Exported at: {0}",
        "export_dir": u"- Report directory: `{0}`",
        "preferences_title": u"User Preferences",
        "revit_versions": u"- Common Revit versions: {0}",
        "workflow": u"- Preferred workflow: {0}",
        "review_focus": u"- Review focus: {0}",
        "safety_notes": u"- Safety notes: {0}",
        "company_title": u"Company Standards",
        "company_standards": u"## Company Standards",
        "company_path": u"- Standards file: `{0}`",
        "company_missing": u"- No company standards file was found. Set a local Markdown file in System Settings.",
        "recent_title": u"Recent Reports",
        "recent_files": u"## Recent Reports",
        "recent_empty": u"- No `.md`, `.json`, or `.csv` report files were found in the current export directory.",
        "recent_item": u"- `{0}` | {1} | {2}",
        "prompt_title": u"## Prompt To Copy Into AI",
        "prompt_heading": u"AI Prompt",
        "prompt_body": u"""Please analyze the YangAgent Revit report content that I will paste next and list findings and recommendations by severity.

Requirements:
1. Provide analysis and recommendations only. Do not generate scripts that directly modify the Revit model.
2. If a fix is needed, propose a dry-run approach first and describe the impact scope.
3. Clearly separate high-risk, medium-risk, and low-risk issues.
4. Reference the exact report file or machine-readable field behind each recommendation.
5. If more information is needed, list which report should be exported next.""",
        "output_title": u"# Yang Agent AI Review Prompt Package",
        "output_done": u"AI review prompt package completed. No model changes were made.",
        "output_report": u"- Output file: `{0}`",
        "alert_done": u"AI review prompt package generated.\n\nNo model changes were made.\n\n{0}",
        "failed_title": u"# AI Review Prompt Package failed",
        "failed_alert": u"AI Review Prompt Package failed. See pyRevit output for details.",
    },
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


def format_time(timestamp):
    try:
        return datetime.fromtimestamp(timestamp).strftime("%Y-%m-%d %H:%M:%S")
    except Exception:
        return u""


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


def collect_recent_files(export_dir):
    results = []
    try:
        names = os.listdir(export_dir)
    except Exception:
        return results
    for name in names:
        path = os.path.join(export_dir, name)
        if not os.path.isfile(path):
            continue
        extension = os.path.splitext(name)[1].lower()
        if extension not in REPORT_EXTENSIONS:
            continue
        try:
            modified_at = os.path.getmtime(path)
            size = os.path.getsize(path)
        except Exception:
            modified_at = 0
            size = 0
        results.append({
            "name": safe_text(name),
            "path": safe_text(path),
            "modified_at": modified_at,
            "size": size,
        })
    results.sort(key=lambda item: item.get("modified_at", 0), reverse=True)
    return results[:MAX_RECENT_FILES]


def build_lines(lang, export_dir, recent_files, preferences, standards_path, standards_text):
    theme_id = get_theme_id()
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    lines = []
    lines.append(build_intro_block(theme_id, tr(lang, "report_title"), tr(lang, "read_only_note")))
    lines.append(u"")
    lines.append(tr(lang, "document_info"))
    lines.append(u"")
    lines.append(tr(lang, "document").format(safe_text(doc.Title)))
    lines.append(tr(lang, "exported_at").format(timestamp))
    lines.append(tr(lang, "export_dir").format(export_dir))
    lines.append(u"")
    lines.append(build_status_block(
        theme_id,
        tr(lang, "preferences_title"),
        [
            tr(lang, "revit_versions").format(safe_text(preferences.get("revit_versions"))),
            tr(lang, "workflow").format(safe_text(preferences.get("preferred_workflow"))),
            tr(lang, "review_focus").format(safe_text(preferences.get("review_focus"))),
            tr(lang, "safety_notes").format(safe_text(preferences.get("safety_notes"))),
        ],
    ))
    lines.append(u"")
    lines.append(tr(lang, "company_standards"))
    lines.append(u"")
    lines.append(tr(lang, "company_path").format(safe_text(standards_path)))
    if safe_text(standards_text).strip():
        lines.append(u"")
        lines.append(u"```markdown")
        lines.append(standards_text)
        lines.append(u"```")
    else:
        lines.append(tr(lang, "company_missing"))
    lines.append(u"")
    lines.append(tr(lang, "recent_files"))
    lines.append(u"")
    if recent_files:
        for file_info in recent_files:
            lines.append(
                tr(lang, "recent_item").format(
                    file_info["path"],
                    format_time(file_info["modified_at"]),
                    format_size(file_info["size"]),
                )
            )
    else:
        lines.append(tr(lang, "recent_empty"))
    lines.append(u"")
    prompt_lines = tr(lang, "prompt_body").splitlines()
    summary_lines = []
    for line in prompt_lines:
        text = safe_text(line).strip()
        if text:
            summary_lines.append(text)
        if len(summary_lines) >= 2:
            break
    lines.append(build_status_block(
        theme_id,
        tr(lang, "prompt_heading"),
        summary_lines,
    ))
    lines.append(u"")
    lines.append(tr(lang, "prompt_title"))
    lines.append(u"")
    lines.append(u"```text")
    lines.append(tr(lang, "prompt_body"))
    lines.append(u"```")
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
    recent_files = collect_recent_files(export_dir)
    preferences = get_agent_preferences()
    standards_path, standards_text = read_company_standards()
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_path = os.path.join(export_dir, "yangagent_ai_review_prompt_{0}.md".format(timestamp))

    lines = build_lines(lang, export_dir, recent_files, preferences, standards_path, standards_text)
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
