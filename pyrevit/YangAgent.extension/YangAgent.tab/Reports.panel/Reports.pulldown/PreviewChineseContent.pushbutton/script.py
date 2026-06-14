# -*- coding: utf-8 -*-
"""Scan the active Revit document for Chinese (CJK) characters.

Read-only preview — no model changes.
Scans families, symbols, parameters, materials, text notes,
family instances, project parameters, views, and project info.
"""

from __future__ import print_function

import codecs
import csv
import os
import re
import traceback
from datetime import datetime

import clr

clr.AddReference("RevitAPI")
clr.AddReference("RevitAPIUI")

from Autodesk.Revit.DB import (  # noqa: E402
    Family,
    FamilyInstance,
    FamilySymbol,
    FilteredElementCollector,
    Material,
    ParameterElement,
    ProjectInfo,
    SharedParameterElement,
    StorageType,
    TextNote,
    View,
)
from pyrevit import forms, revit, script  # noqa: E402
from yang_agent_lang import get_or_choose_language  # noqa: E402
from yang_agent_report_style import build_intro_block, build_status_block  # noqa: E402
from yang_agent_settings import get_export_dir  # noqa: E402
from yang_agent_theme import get_theme_id  # noqa: E402


doc = revit.doc
output = script.get_output()

# CJK Unified Ideographs (U+4E00 – U+9FFF)
CJK_RE = re.compile(u"[\u4e00-\u9fff]")
INSTANCE_LIMIT = 5000
TRUNCATE_LEN = 100


TEXT = {
    "zh": {
        "language_message": u"选择报告语言 / Select report language",
        "alert_title": u"Yang Agent",
        "no_doc": u"没有打开的 Revit 文档。",
        "report_title": u"# Yang Agent 中文内容预览",
        "read_only_note": u"这是只读扫描报告，不会修改 Revit 模型。",
        "summary_heading": u"统计摘要",
        "document": u"文档：{0}",
        "exported_at": u"导出时间：{0}",
        "total_hits": u"总命中数：{0}",
        "section_families": u"族名含中文",
        "section_symbols": u"族类型名/参数含中文",
        "section_materials": u"材质名含中文",
        "section_textnotes": u"文字注释含中文",
        "section_instances": u"族实例参数含中文",
        "section_project_params": u"项目参数含中文",
        "section_views": u"视图名含中文",
        "section_project_info": u"项目信息含中文",
        "detail_heading": u"明细",
        "next_steps_heading": u"建议下一步",
        "next_step_1": u"中文内容不等于错误——本报告仅帮助了解项目中中文的分布。",
        "next_step_2": u"如需批量修改文字注释，可使用\"文本查找替换\"工具。",
        "next_step_3": u"族名和参数的修改需谨慎，建议先在测试模型验证。",
        "none": u"无",
        "output_title": u"# Yang Agent 中文内容预览",
        "output_done": u"扫描完成。未修改模型。",
        "output_hits": u"- 总命中数：{0}",
        "output_report": u"- 报告：`{0}`",
        "output_csv": u"- CSV：`{0}`",
        "alert_done": u"中文内容扫描完成。\n\n未修改模型。\n\n总命中数：{0}\n\n{1}",
        "failed_title": u"# 中文内容扫描失败",
        "failed_alert": u"中文内容扫描失败。请查看 pyRevit 输出窗口。",
    },
    "en": {
        "language_message": u"Select language / 选择语言",
        "alert_title": u"Yang Agent",
        "no_doc": u"No active Revit document.",
        "report_title": u"# Yang Agent Chinese Content Preview",
        "read_only_note": u"This is a read-only scan report. No Revit model changes were made.",
        "summary_heading": u"Summary",
        "document": u"Document: {0}",
        "exported_at": u"Exported at: {0}",
        "total_hits": u"Total hits: {0}",
        "section_families": u"Family names with Chinese",
        "section_symbols": u"Symbol names/params with Chinese",
        "section_materials": u"Material names with Chinese",
        "section_textnotes": u"TextNotes with Chinese",
        "section_instances": u"Family instance params with Chinese",
        "section_project_params": u"Project params with Chinese",
        "section_views": u"View names with Chinese",
        "section_project_info": u"Project info with Chinese",
        "detail_heading": u"Details",
        "next_steps_heading": u"Suggested Next Steps",
        "next_step_1": u"Chinese content does not mean errors — this report only helps understand CJK distribution.",
        "next_step_2": u"To batch-modify TextNotes, use the Text Find & Replace tool.",
        "next_step_3": u"Family names and parameters should be modified carefully; verify in a test model first.",
        "none": u"None",
        "output_title": u"# Yang Agent Chinese Content Preview",
        "output_done": u"Scan completed. No model changes were made.",
        "output_hits": u"- Total hits: {0}",
        "output_report": u"- Report: `{0}`",
        "output_csv": u"- CSV: `{0}`",
        "alert_done": u"Chinese content scan completed.\n\nNo model changes were made.\n\nTotal hits: {0}\n\n{1}",
        "failed_title": u"# Chinese Content Scan failed",
        "failed_alert": u"Chinese Content Scan failed. See pyRevit output for details.",
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


def element_id_text(element_id):
    if element_id is None:
        return u""
    try:
        return safe_text(element_id.IntegerValue)
    except Exception:
        return safe_text(element_id)


def contains_chinese(s):
    return bool(CJK_RE.search(safe_text(s)))


def truncate(text, max_len):
    t = safe_text(text).replace(u"\r\n", u" ").replace(u"\n", u" ").replace(u"\r", u" ")
    if len(t) <= max_len:
        return t
    return t[:max_len] + u"\u2026"


def get_param_text(param):
    if param is None:
        return u""
    try:
        if not param.HasValue:
            return u""
    except Exception:
        pass
    try:
        st = param.StorageType
        if st == StorageType.String:
            return safe_text(param.AsString())
        if st in (StorageType.Integer, StorageType.Double, StorageType.ElementId):
            return safe_text(param.AsValueString())
    except Exception:
        pass
    return u""


def add_hit(results, section, element_id, content_type, chinese_text, element_name):
    results.append({
        "section": section,
        "element_id": element_id_text(element_id),
        "category": content_type,
        "content_type": content_type,
        "chinese_text": truncate(chinese_text, TRUNCATE_LEN),
        "element_name": safe_text(element_name),
    })


def scan_all():
    results = []

    # --- Families ---
    try:
        families = FilteredElementCollector(doc).OfClass(Family)
        for fam in families:
            try:
                if contains_chinese(fam.Name):
                    cat_name = safe_text(fam.FamilyCategory.Name) if fam.FamilyCategory else u""
                    add_hit(results, "families", fam.Id, "family_name", fam.Name, cat_name)
            except Exception:
                pass
    except Exception:
        pass

    # --- Symbols + params ---
    try:
        symbols = FilteredElementCollector(doc).OfClass(FamilySymbol)
        for sym in symbols:
            try:
                if contains_chinese(sym.Name):
                    cat_name = safe_text(sym.Category.Name) if sym.Category else u""
                    add_hit(results, "symbols", sym.Id, "symbol_name", sym.Name, cat_name)
                for param in sym.Parameters:
                    try:
                        pname = param.Definition.Name if param.Definition else u""
                        if contains_chinese(pname):
                            add_hit(results, "symbols", sym.Id, "symbol_param_name", pname, sym.Name)
                        pval = get_param_text(param)
                        if contains_chinese(pval):
                            add_hit(results, "symbols", sym.Id, "symbol_param_value", pval, sym.Name)
                    except Exception:
                        pass
            except Exception:
                pass
    except Exception:
        pass

    # --- Materials ---
    try:
        materials = FilteredElementCollector(doc).OfClass(Material)
        for mat in materials:
            try:
                if contains_chinese(mat.Name):
                    add_hit(results, "materials", mat.Id, "material_name", mat.Name, u"Material")
            except Exception:
                pass
    except Exception:
        pass

    # --- TextNotes ---
    try:
        textnotes = FilteredElementCollector(doc).OfClass(TextNote)
        for tn in textnotes:
            try:
                if contains_chinese(tn.Text):
                    add_hit(results, "textnotes", tn.Id, "text_note", tn.Text, u"TextNote")
            except Exception:
                pass
    except Exception:
        pass

    # --- FamilyInstances (limited) ---
    try:
        instances = FilteredElementCollector(doc).OfClass(FamilyInstance).ToElements()
        instances = instances[:INSTANCE_LIMIT]
        for inst in instances:
            try:
                for param in inst.Parameters:
                    try:
                        pname = param.Definition.Name if param.Definition else u""
                        if contains_chinese(pname):
                            add_hit(results, "instances", inst.Id, "instance_param_name", pname,
                                    inst.Name if inst.Name else u"(unnamed)")
                        pval = get_param_text(param)
                        if contains_chinese(pval):
                            add_hit(results, "instances", inst.Id, "instance_param_value", pval,
                                    inst.Name if inst.Name else u"(unnamed)")
                    except Exception:
                        pass
            except Exception:
                pass
    except Exception:
        pass

    # --- Project Parameters (exclude shared) ---
    try:
        param_elements = FilteredElementCollector(doc).OfClass(ParameterElement)
        for pe in param_elements:
            try:
                if isinstance(pe, SharedParameterElement):
                    continue
                defn = pe.GetDefinition()
                if defn and contains_chinese(defn.Name):
                    add_hit(results, "project_params", pe.Id, "project_param", defn.Name, u"ProjectParam")
            except Exception:
                pass
    except Exception:
        pass

    # --- Views ---
    try:
        views = FilteredElementCollector(doc).OfClass(View)
        for view in views:
            try:
                if view.IsTemplate:
                    continue
                if contains_chinese(view.Name):
                    add_hit(results, "views", view.Id, "view_name", view.Name, view.ViewType.ToString())
            except Exception:
                pass
    except Exception:
        pass

    # --- ProjectInfo ---
    try:
        info = doc.ProjectInformation
        if info:
            fields = [
                ("project_name", info.Name),
                ("project_number", info.Number),
                ("project_author", info.Author),
                ("project_org", info.OrganizationName),
                ("project_building", info.BuildingName),
            ]
            for content_type, val in fields:
                if contains_chinese(val):
                    add_hit(results, "project_info", info.Id, content_type, val, u"ProjectInfo")
    except Exception:
        pass

    return results


def build_report_lines(lang, results):
    theme_id = get_theme_id()
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    sections = [
        ("families", "section_families"),
        ("symbols", "section_symbols"),
        ("materials", "section_materials"),
        ("textnotes", "section_textnotes"),
        ("instances", "section_instances"),
        ("project_params", "section_project_params"),
        ("views", "section_views"),
        ("project_info", "section_project_info"),
    ]

    section_counts = {}
    for sec_key, _ in sections:
        section_counts[sec_key] = sum(1 for r in results if r["section"] == sec_key)

    summary_lines = [
        tr(lang, "document").format(safe_text(doc.Title)),
        tr(lang, "exported_at").format(timestamp),
    ]
    for sec_key, text_key in sections:
        summary_lines.append(u"{0}: {1}".format(tr(lang, text_key), section_counts[sec_key]))
    summary_lines.append(tr(lang, "total_hits").format(len(results)))

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

    for sec_key, text_key in sections:
        sec_results = [r for r in results if r["section"] == sec_key]
        lines.append(u"## {0}".format(tr(lang, text_key)))
        lines.append(u"")
        if not sec_results:
            lines.append(u"- {0}".format(tr(lang, "none")))
        else:
            for r in sec_results:
                lines.append(
                    u"- `{0}` | {1}: {2}".format(
                        r["element_id"],
                        r["element_name"] or r["content_type"],
                        r["chinese_text"],
                    )
                )
        lines.append(u"")

    lines.append(build_status_block(theme_id, tr(lang, "next_steps_heading"), next_step_lines))
    return lines


def write_markdown(path, lines):
    with codecs.open(path, "w", "utf-8-sig") as stream:
        stream.write(u"\n".join(lines))


def write_csv(path, results):
    fieldnames = [
        "element_id",
        "category",
        "content_type",
        "chinese_text",
        "element_name",
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

    results = scan_all()

    export_dir = get_export_dir()
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_path = os.path.join(export_dir, "chinese_content_preview_{0}.md".format(timestamp))
    csv_path = os.path.join(export_dir, "chinese_content_preview_{0}.csv".format(timestamp))

    report_lines = build_report_lines(lang, results)
    write_markdown(log_path, report_lines)
    write_csv(csv_path, results)

    output.print_md(tr(lang, "output_title"))
    output.print_md(u"")
    output.print_md(tr(lang, "output_done"))
    output.print_md(u"")
    output.print_md(tr(lang, "output_hits").format(len(results)))
    output.print_md(tr(lang, "output_report").format(log_path))
    output.print_md(tr(lang, "output_csv").format(csv_path))

    forms.toast(
        tr(lang, "alert_done").format(len(results), log_path),
        title=tr(lang, "alert_title"),
    )


try:
    main()
except Exception:
    err = traceback.format_exc()
    output.print_md(TEXT["zh"]["failed_title"] + u" / " + TEXT["en"]["failed_title"].replace("# ", u""))
    output.print_md("```text\n{0}\n```".format(err))
    forms.alert(TEXT["zh"]["failed_alert"] + u"\n\n" + TEXT["en"]["failed_alert"], title="Yang Agent")
