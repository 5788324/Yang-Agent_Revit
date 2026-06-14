# -*- coding: utf-8 -*-
"""Shared helpers for YangAgent apply tools.

Keep this module IronPython-friendly because it is imported by pyRevit button
scripts inside Revit.
"""

from __future__ import print_function

import codecs
import csv
import os


def safe_text(value):
    if value is None:
        return u""
    try:
        if isinstance(value, unicode):  # noqa: F821  # IronPython
            return value
    except NameError:
        pass
    try:
        if isinstance(value, bytes):
            return value.decode("utf-8-sig")
    except Exception:
        pass
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


def normalize_key(value):
    text = safe_text(value)
    text = text.replace(u"\ufeff", u"")
    text = text.replace(u"\u00a0", u" ")
    return text.strip().lower()


def normalize_value(value):
    return safe_text(value).replace(u"\ufeff", u"").strip()


def is_expected_csv_name(path, prefix):
    name = safe_text(os.path.basename(path)).lower().strip()
    return name.startswith(prefix) and name.endswith(".csv")


def read_preview_csv(path):
    rows = []
    with codecs.open(path, "r", "utf-8-sig") as text_stream:
        reader = csv.DictReader(text_stream)
        if not reader.fieldnames:
            return rows, []

        fieldnames = [normalize_key(field) for field in reader.fieldnames]
        for raw_row in reader:
            row = {}
            index = 0
            for raw_key in reader.fieldnames:
                key = fieldnames[index]
                row[key] = normalize_value(raw_row.get(raw_key, u""))
                index += 1
            rows.append(row)
    return rows, fieldnames


def validate_fields(fieldnames, required_fields):
    available = set(fieldnames)
    for field in required_fields:
        if normalize_key(field) not in available:
            return False
    return True


def parse_element_id(value):
    try:
        return int(safe_text(value).strip())
    except Exception:
        return None


def get_param_text(param):
    if param is None:
        return u""
    try:
        storage_name = safe_text(param.StorageType)
    except Exception:
        storage_name = u""
    if storage_name == "String":
        try:
            value = param.AsString()
            return safe_text(value) if value is not None else u""
        except Exception:
            return u""
    if storage_name == "Integer":
        try:
            return safe_text(param.AsInteger())
        except Exception:
            return u""
    if storage_name == "Double":
        try:
            return safe_text(param.AsDouble())
        except Exception:
            return u""
    try:
        value = param.AsString()
        if value is not None:
            return safe_text(value)
    except Exception:
        pass
    try:
        value = param.AsValueString()
        if value is not None:
            return safe_text(value)
    except Exception:
        pass
    return u""


def collect_apply_rows(rows, is_applicable_row):
    apply_rows = []
    for row in rows:
        if is_applicable_row(row):
            apply_rows.append(row)
    return apply_rows


def find_duplicate_element_ids(rows):
    seen = set()
    duplicates = []
    for row in rows:
        element_id = safe_text(row.get("element_id")).strip()
        if element_id in seen and element_id not in duplicates:
            duplicates.append(element_id)
        seen.add(element_id)
    return duplicates


def confirm_apply(forms, confirm_label, cancel_label, message):
    selected = forms.CommandSwitchWindow.show(
        [confirm_label, cancel_label],
        message=message,
    )
    return selected == confirm_label


def count_results(results):
    applied = 0
    skipped = 0
    failed = 0
    for row in results:
        status = safe_text(row.get("result"))
        if status == "applied":
            applied += 1
        elif status == "skipped":
            skipped += 1
        else:
            failed += 1
    return applied, skipped, failed


def write_utf8_csv(path, rows, fieldnames):
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
