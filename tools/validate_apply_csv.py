#!/usr/bin/env python3
"""Validate YangAgent dry-run CSV files before running an apply tool.

This is a read-only helper. It does not need Revit and never modifies model
files. Use it to catch obvious CSV problems before selecting the file in
pyRevit.
"""

from __future__ import annotations

import argparse
import csv
from dataclasses import dataclass
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

KINDS = {
    "mark": {
        "name_prefix": "missing_door_window_marks_",
        "required": ["dry_run", "element_id", "category", "current_mark", "suggested_mark"],
        "categories": {"Door", "Window"},
        "suggested": "suggested_mark",
        "current": "current_mark",
        "code": "YA-APPLY-MARK",
    },
    "room": {
        "name_prefix": "missing_room_numbers_",
        "required": ["dry_run", "element_id", "category", "current_number", "suggested_number"],
        "categories": {"Room"},
        "suggested": "suggested_number",
        "current": "current_number",
        "code": "YA-APPLY-ROOM",
    },
}


@dataclass
class Finding:
    level: str
    code: str
    message: str


def normalize_key(value: str | None) -> str:
    if value is None:
        return ""
    return value.replace("\ufeff", "").replace("\u00a0", " ").strip().lower()


def normalize_value(value: str | None) -> str:
    if value is None:
        return ""
    return value.replace("\ufeff", "").strip()


def rel(path: Path) -> str:
    try:
        return path.relative_to(ROOT).as_posix()
    except ValueError:
        return path.as_posix()


def read_rows(path: Path) -> tuple[list[dict[str, str]], list[str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as stream:
        reader = csv.DictReader(stream)
        if not reader.fieldnames:
            return [], []
        raw_fields = list(reader.fieldnames)
        fields = [normalize_key(field) for field in raw_fields]
        rows = []
        for raw_row in reader:
            row = {}
            for index, raw_field in enumerate(raw_fields):
                row[fields[index]] = normalize_value(raw_row.get(raw_field))
            rows.append(row)
        return rows, fields


def validate(path: Path, kind: str) -> list[Finding]:
    spec = KINDS[kind]
    findings: list[Finding] = []
    code_prefix = spec["code"]

    if not path.exists():
        return [Finding("ERROR", f"{code_prefix}-CSV-001", f"File does not exist: {path}")]

    name = path.name.lower()
    if not (name.startswith(spec["name_prefix"]) and name.endswith(".csv")):
        findings.append(Finding("ERROR", f"{code_prefix}-CSV-002", f"Unexpected file name: {path.name}"))

    try:
        rows, fields = read_rows(path)
    except Exception as exc:
        return [Finding("ERROR", f"{code_prefix}-CSV-003", f"Could not read CSV: {exc}")]

    missing = [field for field in spec["required"] if field not in set(fields)]
    if missing:
        findings.append(Finding("ERROR", f"{code_prefix}-CSV-004", f"Missing required fields: {', '.join(missing)}"))
        return findings

    if not rows:
        findings.append(Finding("WARN", f"{code_prefix}-CSV-005", "CSV has headers but no rows."))
        return findings

    seen_ids: set[str] = set()
    applicable = 0

    for number, row in enumerate(rows, start=2):
        element_id = row.get("element_id", "").strip()
        dry_run = row.get("dry_run", "").strip().lower()
        category = row.get("category", "").strip()
        suggested = row.get(spec["suggested"], "").strip()
        current = row.get(spec["current"], "").strip()

        if not element_id.isdigit():
            findings.append(Finding("ERROR", f"{code_prefix}-CSV-006", f"Line {number}: element_id is not a positive integer."))
        elif element_id in seen_ids:
            findings.append(Finding("WARN", f"{code_prefix}-CSV-007", f"Line {number}: duplicate element_id {element_id}."))
        else:
            seen_ids.add(element_id)

        if dry_run != "true":
            findings.append(Finding("ERROR", f"{code_prefix}-CSV-008", f"Line {number}: dry_run must be true."))

        if category not in spec["categories"]:
            findings.append(Finding("ERROR", f"{code_prefix}-CSV-009", f"Line {number}: unsupported category {category!r}."))

        if not suggested:
            findings.append(Finding("ERROR", f"{code_prefix}-CSV-010", f"Line {number}: suggested value is blank."))

        if current:
            findings.append(Finding("WARN", f"{code_prefix}-CSV-011", f"Line {number}: current value is not blank; apply will skip it if the model still has a value."))

        if element_id.isdigit() and dry_run == "true" and category in spec["categories"] and suggested:
            applicable += 1

    if applicable == 0:
        findings.append(Finding("ERROR", f"{code_prefix}-CSV-012", "No applicable rows found."))
    else:
        findings.append(Finding("INFO", f"{code_prefix}-CSV-000", f"Applicable rows: {applicable}"))

    return findings


def write_report(path: Path, csv_path: Path, kind: str, findings: list[Finding]) -> None:
    errors = [finding for finding in findings if finding.level == "ERROR"]
    warnings = [finding for finding in findings if finding.level == "WARN"]
    lines = [
        "# YangAgent Apply CSV Validation",
        "",
        f"- CSV: `{rel(csv_path)}`",
        f"- Kind: `{kind}`",
        f"- Errors: {len(errors)}",
        f"- Warnings: {len(warnings)}",
        "",
        "## Findings",
        "",
    ]
    for finding in findings:
        lines.append(f"- `{finding.level}` `{finding.code}` - {finding.message}")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate YangAgent dry-run CSV before apply.")
    parser.add_argument("--kind", choices=sorted(KINDS), required=True, help="CSV type to validate.")
    parser.add_argument("--csv", required=True, help="Path to dry-run CSV.")
    parser.add_argument("--report", default="", help="Optional Markdown report path.")
    args = parser.parse_args()

    csv_path = Path(args.csv)
    findings = validate(csv_path, args.kind)
    for finding in findings:
        print(f"{finding.level}: {finding.code}: {finding.message}")

    if args.report:
        report_path = Path(args.report)
        write_report(report_path, csv_path, args.kind, findings)
        print(f"Report: {rel(report_path)}")

    return 1 if any(finding.level == "ERROR" for finding in findings) else 0


if __name__ == "__main__":
    raise SystemExit(main())
