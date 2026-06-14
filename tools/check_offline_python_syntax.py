#!/usr/bin/env python3
"""Check offline Python tool syntax without writing __pycache__ files."""

from __future__ import annotations

import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_TARGETS = [
    ROOT / "tools" / "static_checks.py",
    ROOT / "tools" / "validate_apply_csv.py",
    ROOT / "tools" / "check_pyrevit_extension.py",
    ROOT / "tools" / "run_sandbox_preflight.py",
]


def compile_path(path: Path) -> str | None:
    try:
        source = path.read_text(encoding="utf-8-sig")
    except OSError as exc:
        return f"Read failed: {path.relative_to(ROOT)} ({exc})"
    except UnicodeDecodeError as exc:
        return f"UTF-8 decode failed: {path.relative_to(ROOT)} ({exc})"

    try:
        compile(source, str(path), "exec")
    except SyntaxError as exc:
        return f"Python syntax failed: {path.relative_to(ROOT)} ({exc})"

    return None


def main(argv: list[str]) -> int:
    targets = [Path(arg) for arg in argv] if argv else DEFAULT_TARGETS
    errors = []
    checked = 0

    for target in targets:
        path = target if target.is_absolute() else (ROOT / target)
        error = compile_path(path)
        if error:
            errors.append(error)
            continue
        checked += 1

    for error in errors:
        print(f"ERROR: {error}")

    print(f"INFO: Checked {checked} offline Python files.")
    print(f"Summary: {len(errors)} errors, 0 warnings")
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
