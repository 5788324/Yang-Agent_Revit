#!/usr/bin/env python3
"""Run read-only repository checks for YangAgent Revit.

The checks are intentionally static. They do not import Revit, run pyRevit,
launch installers, or modify model files.
"""

from __future__ import annotations

import argparse
import re
from dataclasses import dataclass
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PYREVIT_ROOT = ROOT / "pyrevit" / "YangAgent.extension"
DOCS_ROOT = ROOT / "docs"
DEFAULT_REPORT = DOCS_ROOT / "drafts" / "static-check-report.md"


@dataclass
class Finding:
    level: str
    area: str
    path: Path
    message: str


def rel(path: Path) -> str:
    try:
        return path.relative_to(ROOT).as_posix()
    except ValueError:
        return path.as_posix()


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def check_pyrevit_buttons() -> list[Finding]:
    findings: list[Finding] = []
    buttons = sorted(PYREVIT_ROOT.rglob("*.pushbutton"))
    if not buttons:
        findings.append(Finding("ERROR", "pyRevit buttons", PYREVIT_ROOT, "No .pushbutton folders found."))
        return findings

    for button in buttons:
        bundle = button / "bundle.yaml"
        script = button / "script.py"
        readme = button / "README.md"
        icon = button / "icon.png"

        if not bundle.exists():
            findings.append(Finding("ERROR", "pyRevit buttons", button, "Missing bundle.yaml."))
        if not script.exists():
            findings.append(Finding("ERROR", "pyRevit buttons", button, "Missing script.py."))
        if not readme.exists():
            findings.append(Finding("WARN", "pyRevit buttons", button, "Missing README.md."))
        if not icon.exists():
            findings.append(Finding("WARN", "pyRevit buttons", button, "Missing icon.png."))

        if bundle.exists():
            text = read_text(bundle)
            if "title:" not in text:
                findings.append(Finding("WARN", "pyRevit buttons", bundle, "bundle.yaml has no title."))
            if "context:" in text:
                findings.append(Finding("WARN", "pyRevit buttons", bundle, "bundle.yaml uses context; this previously caused pyRevit availability issues."))

    return findings


def iter_markdown_files() -> list[Path]:
    return sorted(DOCS_ROOT.rglob("*.md")) + sorted(ROOT.glob("*.md"))


def check_doc_commands() -> list[Finding]:
    findings: list[Finding] = []
    ps1_pattern = re.compile(r"([A-Za-z0-9_.-]+\.ps1)")
    explicit_script_path = re.compile(r"scripts[\\/][A-Za-z0-9_.-]+\.ps1", re.IGNORECASE)
    placeholder_pattern = re.compile(r"<[^>]+>|SCRIPT_PATH|your-path|script path", re.IGNORECASE)

    for path in iter_markdown_files():
        for number, line in enumerate(read_text(path).splitlines(), start=1):
            if ps1_pattern.search(line) and not explicit_script_path.search(line):
                findings.append(Finding("WARN", "docs commands", path, f"Line {number}: PowerShell script command may need an explicit scripts path."))
            if placeholder_pattern.search(line):
                findings.append(Finding("WARN", "docs commands", path, f"Line {number}: Placeholder wording may not be copy/paste friendly."))

    return findings


def check_version_wording() -> list[Finding]:
    findings: list[Finding] = []
    risky_patterns = [
        re.compile(r"2011\s*[-~]\s*2027.*(support|supported|available|works)", re.IGNORECASE),
        re.compile(r"(support|supported|available|works).{0,32}2011\s*[-~]\s*2027", re.IGNORECASE),
    ]
    saw_planned_2024_2027 = False
    saw_deferred_2011_2023 = False

    for path in iter_markdown_files():
        text = read_text(path)
        lowered_text = text.lower()
        if "2024-2027" in lowered_text and any(token in lowered_text for token in ["first phase", "targets", "priority"]):
            saw_planned_2024_2027 = True
        if "2011-2023" in lowered_text and any(token in lowered_text for token in ["backlog", "deferred", "planned"]):
            saw_deferred_2011_2023 = True

        for number, line in enumerate(text.splitlines(), start=1):
            lowered_line = line.lower()
            if any(token in lowered_line for token in ["do not", "forbidden", "avoid", "not write", "question"]):
                continue
            for pattern in risky_patterns:
                if pattern.search(line):
                    findings.append(Finding("WARN", "version wording", path, f"Line {number}: Avoid claiming full Revit 2011-2027 support before validation."))

    if not saw_planned_2024_2027:
        findings.append(Finding("WARN", "version wording", DOCS_ROOT, "No clear first-phase Revit 2024-2027 wording found."))
    if not saw_deferred_2011_2023:
        findings.append(Finding("WARN", "version wording", DOCS_ROOT, "No clear deferred Revit 2011-2023 wording found."))

    return findings


def write_report(path: Path, findings: list[Finding]) -> None:
    errors = [finding for finding in findings if finding.level == "ERROR"]
    warnings = [finding for finding in findings if finding.level == "WARN"]
    lines = [
        "# YangAgent Static Check Report",
        "",
        "This report is generated by `python tools/static_checks.py --write-report`.",
        "The check is read-only and does not require Revit.",
        "",
        "## Summary",
        "",
        f"- Errors: {len(errors)}",
        f"- Warnings: {len(warnings)}",
        "",
    ]

    if findings:
        lines.extend(["## Findings", ""])
        for finding in findings:
            lines.append(f"- `{finding.level}` `{finding.area}` `{rel(finding.path)}` - {finding.message}")
    else:
        lines.extend(["## Findings", "", "- No findings."])

    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description="Run YangAgent read-only static checks.")
    parser.add_argument("--write-report", action="store_true", help="Write a Markdown report.")
    parser.add_argument("--report", default=str(DEFAULT_REPORT), help="Report path when --write-report is used.")
    args = parser.parse_args()

    findings = []
    findings.extend(check_pyrevit_buttons())
    findings.extend(check_doc_commands())
    findings.extend(check_version_wording())

    for finding in findings:
        print(f"{finding.level}: {finding.area}: {rel(finding.path)}: {finding.message}")

    errors = [finding for finding in findings if finding.level == "ERROR"]
    print(f"Summary: {len(errors)} errors, {len(findings) - len(errors)} warnings")

    if args.write_report:
        write_report(Path(args.report), findings)
        print(f"Report: {rel(Path(args.report))}")

    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
