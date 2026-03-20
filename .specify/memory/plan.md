# Implementation Plan: pywcsk

**Date**: 2026-03-19 | **Spec**: `.specify/memory/spec.md`

## Summary

Implement the Unix `wc` utility in Python as a Click CLI tool, following the BSD `wc(1)` man page. The pipeline is `bytes → analyze() → Counts → formatter → str`. Each increment adds one coherent behavior and leaves all quality gates green.

## Technical Context

**Language/Version**: Python 3.13 (minimum 3.10)
**Primary Dependencies**: click (runtime); pytest, pytest-cov, pytest-mock, mypy, flake8, black, bandit, pre-commit (dev)
**Storage**: N/A (stateless CLI; reads files, writes to stdout/stderr)
**Testing**: pytest with unit, integration (CliRunner), golden output, and oracle layers
**Target Platform**: macOS (BSD wc) and Linux/ubuntu-latest (GNU wc) via GitHub Actions matrix
**Project Type**: CLI tool
**Performance Goals**: Matches system `wc` performance on typical files; no explicit throughput target
**Constraints**: mypy strict, flake8 clean, bandit clean, pre-commit all-green on every commit
**Scale/Scope**: Single-file CLI utility with ~4 source modules

## Constitution Check

- [x] `counter.py` is pure (no I/O, no Click) — enforced by architecture
- [x] Pipeline direction: bytes → Counts → str — no reverse dependencies
- [x] All three test layers required per task
- [x] Column ordering is invariant — formatter enforces this
- [x] `-c`/`-m` last-wins via `_resolve_bytes_chars(argv)` pre-processing
- [x] All files counted before any output — two-pass loop in CLI (Task 016)
- [x] Known deviations documented — tab width, `--libxo`, SIGINFO

## Project Structure

```text
pywcsk/                     # Package
├── __init__.py             # __version__ = "0.1.0"
├── cli.py                  # Click @command, flag wiring, file loop
├── counter.py              # Counts dataclass + analyze(bytes) -> Counts
└── formatter.py            # format_row, compute_col_width, make_total

tests/
├── test_basic.py           # version + import smoke tests (existing)
├── test_counter.py         # unit: analyze() and _count_* helpers
├── test_formatter.py       # unit: format_row, compute_col_width, make_total
├── test_flag_precedence.py # unit: _resolve_bytes_chars(argv)
├── test_cli.py             # integration: CliRunner tests
├── test_golden.py          # golden: CLI output vs .expected files
├── test_oracle.py          # oracle: CLI output vs system wc
├── fixtures/               # small deterministic input files
│   ├── empty.txt
│   ├── hello.txt           # "hello\n"
│   ├── multi.txt           # "one two\nthree four\nfive\n" — 3 lines, 5 words, 24 bytes
│   ├── no_newline.txt      # "hello" — 0 lines, 1 word, 5 bytes (no trailing newline)
│   ├── small.txt           # "hi\n"
│   ├── cafe.txt            # UTF-8 "café\n" (6 bytes, 5 chars)
│   ├── lines.txt           # varying line lengths; longest = 25 chars
│   ├── short_lines.txt     # max line = 5 chars
│   └── long_lines.txt      # max line = 20 chars
└── golden/                 # expected CLI output strings (~17 files)
```

## Module Design

### `counter.py`

```python
@dataclass
class Counts:
    lines: int = 0
    words: int = 0
    bytes_count: int = 0
    chars: int = 0
    max_line_length: int = 0

def analyze(data: bytes, encoding: str = "") -> Counts: ...

# Private helpers (not exported):
def _count_lines(data: bytes) -> int: ...       # data.count(b"\n")
def _count_words(data: bytes) -> int: ...       # len(data.split())
def _count_bytes(data: bytes) -> int: ...       # len(data)
def _count_chars(data: bytes, encoding: str = "") -> int: ...  # locale-aware decode
def _count_max_line_length(data: bytes, encoding: str = "") -> int: ...  # tab = 1 char
```

### `formatter.py`

```python
def format_row(
    counts: Counts,
    filename: str | None,         # None = stdin (no filename column)
    show_lines: bool,
    show_words: bool,
    show_bytes: bool,
    show_chars: bool,
    show_max_line: bool,
    col_width: int,
) -> str: ...

def compute_col_width(
    all_counts: list[Counts],
    show_lines: bool,
    show_words: bool,
    show_bytes: bool,
    show_chars: bool,
    show_max_line: bool,
) -> int: ...
# Returns max(7, len(str(max_value_across_all_shown_columns)))

def make_total(count_list: list[Counts], show_max_line: bool) -> Counts: ...
# Sums lines/words/bytes_count/chars; MAX for max_line_length
```

### `cli.py`

```python
def _resolve_bytes_chars(argv: list[str]) -> tuple[bool, bool]: ...
# Scans argv for -c/-m flags; rightmost wins; returns (show_bytes, show_chars)

@click.command()
@click.version_option(...)
@click.argument("files", nargs=-1)
@click.option("-l", ...)
@click.option("-w", ...)
@click.option("-c", ...)
@click.option("-m", ...)
@click.option("-L", ...)
def main(files, show_lines, show_words, ...) -> None:
    # 1. Resolve -c/-m precedence via _resolve_bytes_chars(sys.argv[1:])
    # 2. Determine default flag set if no flags specified
    # 3. Count all files (two-pass: accumulate Counts list first)
    # 4. Compute col_width from all Counts
    # 5. Format and print all rows
    # 6. Print total row if > 1 file succeeded
    # 7. Exit 1 if any errors occurred
```

## Oracle Testing Strategy

- `tests/test_oracle.py` created in Task 005 (first task where `analyze()` has all three default fields)
- `run_wc(flags, path) -> str`: returns raw stdout of system `wc`; string comparison is default
- `parse_wc_output(s) -> dict[str, int]`: semantic fallback; used only at `analyze()` level before CLI exists, with inline comment
- `wc_flavor` session fixture: detects `"bsd"` vs `"gnu"` via `wc --version`
- Module skipped if `wc` not on `$PATH`
- Oracle tests marked `@pytest.mark.oracle`; run selectively with `pytest -m oracle`
- Known deviations marked `@pytest.mark.xfail(strict=False, reason="...")`
- Semantic cases converted to string comparison in Task 009 (when CLI exists for default flags)

## Task Sequence

See `tasks.md` for the full ordered breakdown. Each task maps to one acceptance criterion cluster from `spec.md` and leaves all quality gates green.
