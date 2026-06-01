from __future__ import annotations

import subprocess
import sys
from pathlib import Path


FORBIDDEN_TERMS = (
    "sched" + "uler",
    "schedul" + "ing",
    "time" + "table",
    "k" + "12",
    "scho" + "ol",
    "teach" + "er",
    "stud" + "ent",
    "class" + "room",
    "排" + "课",
    "课" + "表",
    "学" + "校",
    "教" + "师",
    "学" + "生",
)

FORBIDDEN_SUFFIXES = (
    ".xlsx",
    ".xls",
    ".zip",
    ".png",
    ".jpg",
    ".jpeg",
    ".log",
    ".out",
    ".err",
)


def tracked_files() -> list[Path]:
    result = subprocess.run(
        ["git", "ls-files"],
        check=True,
        capture_output=True,
        text=True,
    )
    return [Path(line.strip()) for line in result.stdout.splitlines() if line.strip()]


def main() -> int:
    root = Path.cwd()
    failures: list[str] = []
    for path in tracked_files():
        path_text = path.as_posix().lower()
        if path.suffix.lower() in FORBIDDEN_SUFFIXES:
            failures.append(f"forbidden generated artifact: {path}")
            continue
        if ".git/" in path_text:
            continue
        try:
            content = (root / path).read_text(encoding="utf-8")
        except UnicodeDecodeError:
            failures.append(f"non-text tracked file: {path}")
            continue
        lowered = content.lower()
        for term in FORBIDDEN_TERMS:
            if term.lower() in lowered or term.lower() in path_text:
                failures.append(f"forbidden term {term!r} in {path}")

    if failures:
        print("RELEASE BOUNDARY: FAIL")
        for failure in failures:
            print(f"- {failure}")
        return 1

    print("RELEASE BOUNDARY: PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
