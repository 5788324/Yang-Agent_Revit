"""Offline preflight checks for the YangAgent pyRevit extension.

This script is safe to run without Revit. It validates the extension layout,
required button assets, ASCII bundle folder names, and Python syntax so the
next sandbox-model run can fail early outside Revit.
"""

from __future__ import annotations

import argparse
import os
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
EXTENSION_ROOT = REPO_ROOT / "pyrevit" / "YangAgent.extension"
REQUIRED_BUTTON_FILES = ("bundle.yaml", "README.md", "icon.png", "script.py")
REQUIRED_CONTAINER_FILES = {
    ".pulldown": ("bundle.yaml", "icon.png"),
}
ASCII_FOLDER_SUFFIXES = (".extension", ".tab", ".panel", ".pulldown", ".pushbutton")


class CheckResult(object):
    def __init__(self) -> None:
        self.errors = []
        self.warnings = []
        self.infos = []

    def error(self, message: str) -> None:
        self.errors.append(message)

    def warning(self, message: str) -> None:
        self.warnings.append(message)

    def info(self, message: str) -> None:
        self.infos.append(message)


def is_ascii_text(value: str) -> bool:
    try:
        value.encode("ascii")
        return True
    except UnicodeEncodeError:
        return False


def check_exists(path: Path, result: CheckResult, label: str) -> None:
    if not path.exists():
        result.error(f"{label} is missing: {path.relative_to(REPO_ROOT)}")


def read_text(path: Path, result: CheckResult) -> str:
    try:
        return path.read_text(encoding="utf-8-sig")
    except UnicodeDecodeError as exc:
        result.error(f"UTF-8 decode failed: {path.relative_to(REPO_ROOT)} ({exc})")
    except OSError as exc:
        result.error(f"Read failed: {path.relative_to(REPO_ROOT)} ({exc})")
    return ""


def check_ascii_folder_name(path: Path, result: CheckResult) -> None:
    if path.suffix.lower() not in ASCII_FOLDER_SUFFIXES:
        return
    if not is_ascii_text(path.name):
        result.error(
            "Folder name must stay ASCII for pyRevit cache stability: "
            f"{path.relative_to(REPO_ROOT)}"
        )


def check_bundle_title(path: Path, result: CheckResult) -> None:
    text = read_text(path, result)
    if not text:
        return
    if "title:" not in text:
        result.error(f"bundle.yaml missing title: {path.relative_to(REPO_ROOT)}")


def compile_python(path: Path, result: CheckResult) -> None:
    try:
        source = path.read_text(encoding="utf-8-sig")
        compile(source, str(path), "exec")
    except SyntaxError as exc:
        result.error(f"Python syntax failed: {path.relative_to(REPO_ROOT)} ({exc})")
    except UnicodeDecodeError as exc:
        result.error(f"UTF-8 decode failed: {path.relative_to(REPO_ROOT)} ({exc})")
    except Exception as exc:  # pragma: no cover - defensive
        result.error(f"Python compile failed: {path.relative_to(REPO_ROOT)} ({exc})")


def iter_dirs_with_suffix(root: Path, suffix: str):
    for path in root.rglob(f"*{suffix}"):
        if path.is_dir():
            yield path


def check_container_dirs(result: CheckResult) -> None:
    for suffix, required_files in REQUIRED_CONTAINER_FILES.items():
        for directory in iter_dirs_with_suffix(EXTENSION_ROOT, suffix):
            check_ascii_folder_name(directory, result)
            for filename in required_files:
                check_exists(directory / filename, result, f"{suffix} file")
            bundle_path = directory / "bundle.yaml"
            if bundle_path.exists():
                check_bundle_title(bundle_path, result)

    for suffix in (".tab", ".panel"):
        for directory in iter_dirs_with_suffix(EXTENSION_ROOT, suffix):
            check_ascii_folder_name(directory, result)


def check_pushbuttons(result: CheckResult) -> None:
    pushbuttons = sorted(iter_dirs_with_suffix(EXTENSION_ROOT, ".pushbutton"))
    if not pushbuttons:
        result.error("No .pushbutton directories were found under pyrevit/YangAgent.extension")
        return

    for directory in pushbuttons:
        check_ascii_folder_name(directory, result)
        for filename in REQUIRED_BUTTON_FILES:
            check_exists(directory / filename, result, "pushbutton file")
        bundle_path = directory / "bundle.yaml"
        if bundle_path.exists():
            check_bundle_title(bundle_path, result)
        script_path = directory / "script.py"
        if script_path.exists():
            compile_python(script_path, result)

    result.info(f"Found {len(pushbuttons)} pushbutton folders.")


def check_library_python(result: CheckResult) -> None:
    py_files = sorted(EXTENSION_ROOT.rglob("*.py"))
    for path in py_files:
        compile_python(path, result)
    result.info(f"Compiled {len(py_files)} Python files.")


def check_extension_root(result: CheckResult) -> None:
    if not EXTENSION_ROOT.is_dir():
        result.error(f"Extension root not found: {EXTENSION_ROOT.relative_to(REPO_ROOT)}")
        return
    check_ascii_folder_name(EXTENSION_ROOT, result)


def run_checks() -> CheckResult:
    result = CheckResult()
    check_extension_root(result)
    if result.errors:
        return result
    check_container_dirs(result)
    check_pushbuttons(result)
    check_library_python(result)
    return result


def print_messages(result: CheckResult) -> None:
    for message in result.errors:
        print(f"ERROR: {message}")
    for message in result.warnings:
        print(f"WARN: {message}")
    for message in result.infos:
        print(f"INFO: {message}")
    print(
        "Summary: {0} errors, {1} warnings".format(
            len(result.errors),
            len(result.warnings),
        )
    )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.parse_args()

    os.chdir(str(REPO_ROOT))
    result = run_checks()
    print_messages(result)
    return 1 if result.errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
