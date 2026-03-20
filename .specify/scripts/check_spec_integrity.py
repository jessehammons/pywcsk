#!/usr/bin/env python3
"""Spec integrity checker for .specify/memory/ files.

Checks:
  - No unresolved placeholders (TODO, TKTK, TBD, FIXME, ???, <placeholder>)
  - spec.md: FR-NNN numbers are sequential with no gaps
  - spec.md: US numbers in story headers match those referenced in tasks.md
  - tasks.md: [USN] tags only reference story numbers defined in spec.md
  - tasks.md: Task IDs (TNNN) are sequential with no gaps
"""

from pathlib import Path
import re
import sys


PLACEHOLDER_PATTERN = re.compile(
    r"\b(TODO|TKTK|TBD|FIXME)\b|" r"\?\?\?|" r"<placeholder>",
    re.IGNORECASE,
)

FR_PATTERN = re.compile(r"\bFR-(\d{3})\b")
US_HEADER_PATTERN = re.compile(r"^### User Story (\d+)", re.MULTILINE)
US_REF_PATTERN = re.compile(r"\[US(\d+)\]")
TASK_ID_PATTERN = re.compile(r"\bT(\d{3})\b")


def check_placeholders(path: Path, text: str) -> list[str]:
    """Return error strings for each line containing an unresolved placeholder."""
    errors = []
    for i, line in enumerate(text.splitlines(), 1):
        if m := PLACEHOLDER_PATTERN.search(line):
            errors.append(f"{path}:{i}: unresolved placeholder '{m.group()}'")
    return errors


def check_fr_sequential(path: Path, text: str) -> list[str]:
    """Return error strings for any gaps in the FR-NNN sequence."""
    nums = sorted(int(m) for m in FR_PATTERN.findall(text))
    if not nums:
        return []
    errors = []
    expected = list(range(nums[0], nums[-1] + 1))
    missing = sorted(set(expected) - set(nums))
    for n in missing:
        errors.append(f"{path}: FR-{n:03d} missing (gap in FR sequence)")
    return errors


def check_task_ids_sequential(path: Path, text: str) -> list[str]:
    """Return error strings for any gaps in the TNNN task ID sequence."""
    nums = sorted(int(m) for m in TASK_ID_PATTERN.findall(text))
    if not nums:
        return []
    errors = []
    expected = list(range(nums[0], nums[-1] + 1))
    missing = sorted(set(expected) - set(nums))
    for n in missing:
        errors.append(f"{path}: T{n:03d} missing (gap in task ID sequence)")
    return errors


def collect_us_numbers(spec_text: str) -> set[int]:
    """Return the set of user story numbers defined in spec_text."""
    return {int(m) for m in US_HEADER_PATTERN.findall(spec_text)}


def check_us_refs(tasks_path: Path, tasks_text: str, valid_us: set[int]) -> list[str]:
    """Return error strings for [USN] tags referencing undefined user stories."""
    errors = []
    for i, line in enumerate(tasks_text.splitlines(), 1):
        for m in US_REF_PATTERN.finditer(line):
            n = int(m.group(1))
            if n not in valid_us:
                errors.append(
                    f"{tasks_path}:{i}: [US{n}] references undefined user story"
                    f" (valid: {sorted(valid_us)})"
                )
    return errors


def main(argv: list[str]) -> int:
    """Run all spec integrity checks against the given file paths; return exit code."""
    if not argv:
        print("usage: check_spec_integrity.py <file> [file ...]", file=sys.stderr)
        return 1

    memory_dir = Path(__file__).parent.parent / "memory"
    spec_path = memory_dir / "spec.md"

    # Load spec.md to extract valid US numbers (needed for cross-file check)
    valid_us: set[int] = set()
    if spec_path.exists():
        valid_us = collect_us_numbers(spec_path.read_text(encoding="utf-8"))

    all_errors: list[str] = []

    for arg in argv:
        path = Path(arg)
        if not path.exists():
            continue
        text = path.read_text(encoding="utf-8")

        all_errors.extend(check_placeholders(path, text))

        if path.name == "spec.md":
            all_errors.extend(check_fr_sequential(path, text))

        if path.name == "tasks.md":
            all_errors.extend(check_task_ids_sequential(path, text))
            if valid_us:
                all_errors.extend(check_us_refs(path, text, valid_us))

    if all_errors:
        for err in all_errors:
            print(err, file=sys.stderr)
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
