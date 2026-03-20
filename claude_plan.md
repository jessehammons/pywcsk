# Plan: Incrementally implement `wc` in pywcsk using GitHub Spec Kit

## Context

`pywcsk` is a Python CLI skeleton (Click, pyproject.toml, mypy strict, flake8, pytest, GitHub Actions). The goal is to implement the Unix `wc` command functionality from its man page, incrementally, using **GitHub Spec Kit (Spec-Driven Development)** methodology. Every stage must leave all checks green: unit tests, integration tests, golden output tests, mypy, flake8, bandit, pre-commit.

Skipped (out of scope): `--libxo` (FreeBSD-specific), SIGINFO signal handling (BSD-specific).

---

## Spec Kit Directory Structure to Create

```
.specify/
  constitution.md        # Non-negotiable constraints (typed, linted, tests-required)
  spec.md                # Behavioral spec with Given/When/Then for all man-page behaviors
  plan.md                # Technical implementation strategy
  tasks/
    001-cli-skeleton-refactor.md
    002-counter-count-lines.md
    003-counter-count-words.md
    004-counter-count-bytes.md
    005-counter-chars-maxlen.md
    006-formatter.md
    007-cli-default-no-flags.md
    008-flags-l-w-c.md
    009-flag-m-char-counting.md
    010-flag-L-maxline.md
    011-multi-file-total.md
    012-multi-file-L-total-max.md
    013-error-handling.md
    014-column-width-scaling.md
    015-stdin-dash-argument.md
    016-documentation.md
```

---

## Python Architecture

Three new modules, plus updates to `cli.py`:

| File | Role |
|---|---|
| `pywcsk/counter.py` | Pure functions on `bytes`; no I/O, no Click imports |
| `pywcsk/formatter.py` | `Counts` dataclass + column formatting + total computation |
| `pywcsk/cli.py` | Click command wiring counter + formatter; changed from `@click.group()` to `@click.command()` |

**Key constraint:** All files are counted before any output is produced (required for consistent column-width computation across a multi-file invocation).

**`-c`/`-m` last-wins:** Implemented via a `_resolve_bytes_chars(argv)` helper that inspects `sys.argv` for the relative order of `-c` and `-m` flags. Click doesn't natively support "last flag wins" for two mutually exclusive options.

---

## Test Layers (all three required per task)

1. **Unit tests** — `tests/test_counter.py`, `tests/test_formatter.py`: pure functions, no CLI
2. **Integration tests** — `tests/test_cli.py`: Click `CliRunner`, covers flags, errors, multi-file
3. **Golden output tests** — `tests/test_golden.py`: parametrized, invokes CLI, compares against `tests/golden/*.expected` files; `{path}` tokens substituted at runtime; fixtures live in `tests/fixtures/`

---

## Incremental Task Breakdown

Each task = one coherent behavior; all checks green when done.

### Task 001 — CLI skeleton refactor (group → command)
**Why first:** `@click.group()` makes `-l file` be parsed as a subcommand invocation, not a flag. Must fix before any wc behavior.
- Change `cli.py`: `@click.group()` → `@click.command()`, keep `version_option`, add stub `files` argument (`nargs=-1`)
- Create `tests/test_cli.py` with `test_version_flag`, `test_help_flag`, `test_no_args_exits_zero`

### Task 002 — `counter.py`: `count_lines`
- Create `pywcsk/counter.py` with `count_lines(data: bytes) -> int`: `data.count(b"\n")`
- Create `tests/test_counter.py` with parametrized tests: empty bytes → 0, `b"hello\n"` → 1, `b"a\nb\nc\n"` → 3, no trailing newline → 0 for `b"hello"`

### Task 003 — `counter.py`: `count_words`
- Add `count_words(data: bytes) -> int`: `len(data.split())`
- Extend `test_counter.py`: empty → 0, `b"hello"` → 1, `b"hello world\n"` → 2, `b"  spaces  \n"` → 1, `b"hello\n\nworld\n"` → 2

### Task 004 — `counter.py`: `count_bytes`
- Add `count_bytes(data: bytes) -> int`: `len(data)`
- Extend `test_counter.py`: empty → 0, `b"hello\n"` → 6, multibyte UTF-8 string → byte count exceeds char count

### Task 005 — `counter.py` chars and max line length
- `count_chars(data: bytes, encoding: str = "") -> int`: locale-aware decode, `errors="replace"`
- `count_max_line_length(data: bytes, encoding: str = "") -> int`: max of decoded line lengths (tab = 1 char — documented deviation from BSD's tabstop-8)
- Extend `test_counter.py` with UTF-8 multibyte tests

### Task 006 — `formatter.py`
- `Counts` dataclass: `lines, words, bytes_count, chars, max_line_length`
- `format_row(counts, filename, show_*, col_width) -> str`: columns in canonical order (lines, words, bytes/chars, max_line_length), right-justified
- `compute_col_width(all_counts, ...) -> int`: `max(7, len(str(max_val_across_all)))`
- `make_total(count_list, show_max_line) -> Counts`: sums for lines/words/bytes/chars; MAX for max_line_length
- Create `tests/test_formatter.py`

### Task 007 — Default mode CLI (stdin + single file, no flags)
- Wire counter + formatter into CLI for default behavior (lines + words + bytes)
- Error handling: `OSError` per file → stderr, continue, exit 1 if any errors
- Create `tests/fixtures/`: `empty.txt`, `hello.txt`, `multi.txt`
- Create `tests/golden/`: `*.default.expected` files
- Create `tests/test_golden.py` with parametrized golden runner

### Task 008 — `-l`, `-w`, `-c` flags
- Add three `@click.option` is_flag options
- When any flag specified, show only flagged columns; no flags = default (lines+words+bytes)
- Output order always canonical regardless of flag input order
- Golden files: `hello.{l,w,c,lw,lwc}.expected`

### Task 009 — `-m` flag + `-c`/`-m` mutual exclusion
- Add `-m` option; implement `_resolve_bytes_chars(argv: list[str]) -> tuple[bool, bool]`
- Create `tests/fixtures/cafe.txt` (UTF-8 "café\n", 6 bytes, 5 chars)
- Golden files: `cafe.{m,c,cm,mc}.expected`

### Task 010 — `-L` flag (longest line)
- Add `-L` option, pass through to formatter (`make_total` already implements max-not-sum)
- Create `tests/fixtures/lines.txt` (known longest line = 25 chars)
- Golden files: `lines.{L,lL}.expected`

### Task 011 — Multiple files with total row
- Add total row when `len(processed_files) > 1`; total uses string `"total"` as filename
- Create `tests/fixtures/small.txt`
- Golden file: `hello_and_small.default.expected` (2 file rows + total row)

### Task 012 — Multi-file `-L` total is max, not sum
- Covered by `formatter.make_total` (already correct); this task adds explicit test coverage proving it
- Create `tests/fixtures/short_lines.txt`, `long_lines.txt`
- Golden file: `short_and_long_lines.L.expected` (total = max not sum)

### Task 013 — Error handling hardening
- Handle permission denied, `IsADirectoryError`, all-files-fail case
- Total row printed only for successfully processed files (if >1 succeeded)
- Tests: `test_all_missing_files_exit_1`, `test_two_valid_one_missing_shows_total`, `test_directory_as_argument`

### Task 014 — Column width scaling (two-pass refactor)
- Refactor CLI output loop: count all files first, then format all rows
- All rows use the widest column width required by any single file
- Tests: wide-column consistency across files in same invocation

### Task 015 — Stdin via `-` argument
- `-` as filename reads from stdin, displays no filename (matching BSD behavior)
- Golden file: `dash_stdin.default.expected`
- Tests: `test_dash_reads_stdin`, `test_dash_and_file`, `test_dash_in_middle`

### Task 016 — README + documentation
- Fill in `README.md`: synopsis, installation, usage examples, flags table, known deviations from BSD wc
- No code changes; pre-commit hooks must pass on new content

---

## Final File Layout

```
pywcsk/
  __init__.py, cli.py, counter.py, formatter.py

tests/
  test_basic.py, test_counter.py, test_formatter.py, test_cli.py, test_golden.py
  fixtures/: empty.txt, hello.txt, multi.txt, cafe.txt, lines.txt, small.txt,
             short_lines.txt, long_lines.txt
  golden/: ~17 *.expected files

.specify/
  constitution.md, spec.md, plan.md, tasks/001-016-*.md
```

---

## Verification

After each task: `pre-commit run --all-files && pytest --verbose --cov=pywcsk`

End-to-end smoke tests (after Task 005+):
```bash
echo "hello world" | pywcsk                    # → "      1       2      11"
pywcsk -l tests/fixtures/hello.txt             # → "      1 tests/fixtures/hello.txt"
pywcsk tests/fixtures/hello.txt tests/fixtures/small.txt  # 3 rows including total
```
