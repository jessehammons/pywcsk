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
    001-speckit-setup.md
    002-cli-skeleton-refactor.md
    003-counter-counts-dataclass-lines.md
    004-counter-analyze-words.md
    005-counter-analyze-bytes.md
    006-counter-analyze-chars-maxlen.md
    007-formatter.md
    008-cli-default-no-flags.md
    009-flags-l-w-c.md
    010-flag-precedence-resolve-bytes-chars.md
    011-flag-m-char-counting.md
    012-flag-L-maxline.md
    013-multi-file-total.md
    014-multi-file-L-total-max.md
    015-error-handling.md
    016-column-width-scaling.md
    017-stdin-dash-argument.md
    018-documentation.md
```

---

## Python Architecture

Three new modules, plus updates to `cli.py`:

| File | Role |
|---|---|
| `pywcsk/counter.py` | `Counts` dataclass + `analyze(data: bytes) -> Counts`; private `_count_*` helpers; no I/O, no Click |
| `pywcsk/formatter.py` | Column formatting and total computation; imports `Counts` from `counter` |
| `pywcsk/cli.py` | Click command wiring counter + formatter; changed from `@click.group()` to `@click.command()` |

**Pipeline:** `bytes → analyze() → Counts → formatter → str`. Every layer receives and passes `Counts` — the CLI never touches raw integers, and the formatter never calls counting functions directly.

**Key constraint:** All files are counted before any output is produced (required for consistent column-width computation across a multi-file invocation).

**`-c`/`-m` last-wins:** Implemented via a `_resolve_bytes_chars(argv)` helper that inspects `sys.argv` for the relative order of `-c` and `-m` flags. Click doesn't natively support "last flag wins" for two mutually exclusive options.

---

## Test Layers

Layers 1–3 are required per task. Layer 4 is woven in incrementally starting from Task 005.

1. **Unit tests** — `tests/test_counter.py`, `tests/test_formatter.py`, `tests/test_flag_precedence.py`: pure functions, no CLI
2. **Integration tests** — `tests/test_cli.py`: Click `CliRunner`, covers flags, errors, multi-file
3. **Golden output tests** — `tests/test_golden.py`: parametrized, invokes CLI, compares against `tests/golden/*.expected` files; `{path}` tokens substituted at runtime; fixtures live in `tests/fixtures/`
4. **Oracle tests** — `tests/test_oracle.py`: runs system `wc` and `pywcsk` against the same fixtures and compares results; created in Task 005, extended in Tasks 006, 009, 011, 013.

### BSD vs GNU `wc` differences

macOS ships BSD `wc`; GitHub Actions (ubuntu-latest) ships GNU `wc`. Known divergences that affect oracle testing:

| Behavior | BSD (macOS) | GNU (Linux/CI) |
|---|---|---|
| Column width minimum | 7 | varies (based on actual value width) |
| `-L` flag | supported | supported |
| `-m` locale handling | uses `LC_CTYPE` | uses `LC_ALL`/`LC_CTYPE` |
| Multiple spaces in output | may differ | may differ |

**Strategy:** string comparison is the default — run system `wc` and `pywcsk` on the same fixture and assert `pywcsk_output == wc_output`. Semantic comparison (parse integers, compare counts only) is the narrow fallback used only for cases where BSD and GNU produce different column widths for identical input. Every fallback to semantic comparison must have an inline comment explaining exactly why string comparison cannot be used. Tests covering known behavioral divergences (tab expansion for `-L`, multibyte locale for `-m`) are marked `@pytest.mark.xfail(strict=False)` with a reason string.

---

## Incremental Task Breakdown

Each task = one coherent behavior; all checks green when done.

### Task 001 — Spec Kit setup and spec authoring

**Installation (one-time, system-level — not added to `pyproject.toml`):**

`specify-cli` requires Python 3.11+. To use Homebrew Python explicitly:

```bash
uv tool install --python /opt/homebrew/bin/python3 \
    "specify-cli @ git+https://github.com/github/spec-kit.git"
```

If `uv` is not yet installed:
```bash
/opt/homebrew/bin/pip3 install pipx
/opt/homebrew/bin/pipx install git+https://github.com/github/spec-kit.git \
    --python /opt/homebrew/bin/python3
```

**Bootstrap the project:**
```bash
cd /Users/jesse/code/pywcsk
specify init . --ai claude
```

This scaffolds `.specify/` with template markdown files and `.claude/commands/` with Claude Code slash commands (`/specify`, `/plan`, `/tasks`, `/implement`, `/analyze`).

**Write the spec files** (filling in the scaffolded templates):

- **`constitution.md`** — non-negotiable constraints: strict typing, all code linted, every behavior requires all three test layers before a task is complete, `counter.py` is pure (no I/O), output column order is invariant, `-c`/`-m` last-wins, `-L` total is max not sum, tab width = 1 (documented deviation from BSD tabstop-8), `--libxo` and SIGINFO out of scope
- **`spec.md`** — Given/When/Then acceptance criteria for every man-page behavior: default output, stdin, each flag (`-l`, `-w`, `-c`, `-m`, `-L`), flag combinations and output column ordering, multi-file with total row, `-L` total = max, `-c`/`-m` mutual exclusion (last wins), missing file errors, exit codes, `-` as stdin marker
- **`plan.md`** — prose version of the Python Architecture section above
- **`tasks/001-018-*.md`** — one file per task in this breakdown, each containing the acceptance criteria and test requirements for that task

**Verification (beyond pre-commit):**

1. **`pre-commit run --all-files`** — catches trailing whitespace, EOF, YAML validity
2. **`specify analyze`** — validates internal consistency: every acceptance criterion in `spec.md` maps to a task, no task references behavior absent from `spec.md`, constitution constraints are reflected in the plan
3. **Manual man-page cross-check** — read through the `wc` man page line by line and confirm every described behavior has a corresponding acceptance criterion in `spec.md`; check off each man-page paragraph
4. **Manual oracle spot-check on `spec.md`** — before writing any code, run actual system `wc` against two or three hand-crafted inputs and verify the expected outputs written in the spec's Given/When/Then match; this validates the spec itself, not the code

### Task 002 — CLI skeleton refactor (group → command)
**Why first:** `@click.group()` makes `-l file` be parsed as a subcommand invocation, not a flag. Must fix before any wc behavior.
- Change `cli.py`: `@click.group()` → `@click.command()`, keep `version_option`, add stub `files` argument (`nargs=-1`)
- Create `tests/test_cli.py` with `test_version_flag`, `test_help_flag`, `test_no_args_exits_zero`

### Task 003 — `counter.py`: `Counts` dataclass + `analyze()` for lines
- Create `pywcsk/counter.py` with the `Counts` dataclass (all five fields: `lines, words, bytes_count, chars, max_line_length`, all `int`, default `0`) and `analyze(data: bytes) -> Counts`
- `analyze()` populates only `lines` for now via private `_count_lines(data: bytes) -> int`: `data.count(b"\n")`; other fields remain `0`
- Create `tests/test_counter.py`: test `analyze(b"").lines == 0`, `analyze(b"hello\n").lines == 1`, `analyze(b"a\nb\nc\n").lines == 3`, `analyze(b"hello").lines == 0`; also assert other fields are `0`

### Task 004 — `counter.py`: `analyze()` adds words
- Add `_count_words(data: bytes) -> int`: `len(data.split())`; `analyze()` now populates `words`
- Extend `test_counter.py`: `analyze(b"hello world\n").words == 2`, `analyze(b"  spaces  \n").words == 1`, `analyze(b"hello\n\nworld\n").words == 2`

### Task 005 — `counter.py`: `analyze()` adds bytes + first oracle tests
- Add `_count_bytes(data: bytes) -> int`: `len(data)`; `analyze()` now populates `bytes_count`
- Extend `test_counter.py`: `analyze(b"hello\n").bytes_count == 6`, multibyte UTF-8 input → `bytes_count` exceeds `chars` (still `0` at this stage)
- **Create `tests/test_oracle.py`** — earliest point where oracle testing is meaningful: `analyze()` now produces lines, words, and bytes, which is exactly what `wc` reports by default
  - Session-scoped `wc_flavor` fixture: detects `"bsd"` vs `"gnu"` via `wc --version` (succeeds on GNU, fails on BSD); skips module if `wc` not on `$PATH`
  - `run_wc(flags, path) -> str` helper: runs system `wc` and returns its raw stdout string; string comparison is the default
  - `parse_wc_output(s) -> dict[str, int]` helper: available as semantic fallback only where documented
  - First oracle cases (at the `analyze()` level — no CLI string output yet, so semantic comparison is unavoidable at this stage):
    - `hello.txt` default: `analyze(data).lines/words/bytes_count` matches parsed `wc hello.txt`
    - `multi.txt` default: same
    - `empty.txt` default: all zeros on both sides
    - Inline comment on each: `# semantic comparison only — CLI not yet wired; switch to string comparison in Task 009`
  - Mark all tests `@pytest.mark.oracle`; add marker to `pyproject.toml` `[tool.pytest.ini_options]`

### Task 006 — `counter.py`: `analyze()` adds chars and max line length
- Add `_count_chars` (locale-aware decode, `errors="replace"`) and `_count_max_line_length` (tab = 1 char — documented deviation from BSD's tabstop-8)
- `analyze()` now populates all five fields; `Counts` is fully populated
- Extend `test_counter.py` with UTF-8 multibyte tests: `analyze(b"caf\xc3\xa9\n").chars == 5`, `.bytes_count == 6`
- Extend `test_oracle.py`: semantic oracle cases for `-m` and `-L` at the `analyze()` level (CLI not yet wired for these flags); `-L` on tab-containing files marked `xfail(strict=False, reason="tab expansion: BSD=tabstop-8, pywcsk=1")`; each case has inline comment `# semantic only — switch to string comparison in Task 012`

### Task 007 — `formatter.py`
- Imports `Counts` from `counter` (does not redefine it)
- `format_row(counts, filename, show_*, col_width) -> str`: columns in canonical order (lines, words, bytes/chars, max_line_length), right-justified
- `compute_col_width(all_counts, ...) -> int`: `max(7, len(str(max_val_across_all)))`
- `make_total(count_list, show_max_line) -> Counts`: sums lines/words/bytes_count/chars; MAX for max_line_length
- Create `tests/test_formatter.py`

### Task 008 — Default mode CLI (stdin + single file, no flags)
- Wire counter + formatter into CLI for default behavior (lines + words + bytes)
- Error handling: `OSError` per file → stderr, continue, exit 1 if any errors
- Create `tests/fixtures/`: `empty.txt`, `hello.txt`, `multi.txt`
- Create `tests/golden/`: `*.default.expected` files
- Create `tests/test_golden.py` with parametrized golden runner

### Task 009 — `-l`, `-w`, `-c` flags
- Add three `@click.option` is_flag options
- When any flag specified, show only flagged columns; no flags = default (lines+words+bytes)
- Output order always canonical regardless of flag input order
- Golden files: `hello.{l,w,c,lw,lwc}.expected`
- Extend `test_oracle.py`: CLI-level string-comparison oracle cases for `-l`, `-w`, `-c`; convert the Task 005 default-mode cases from semantic to string comparison now that the CLI exists

### Task 010 — Flag precedence: `_resolve_bytes_chars`
- Implement `_resolve_bytes_chars(argv: list[str]) -> tuple[bool, bool]` in `cli.py` (returns `(show_bytes, show_chars)`)
- No CLI wiring yet — pure logic, tested in isolation
- Create `tests/test_flag_precedence.py` with exhaustive unit tests:
  - `[]` → `(True, False)` (default: bytes)
  - `["-c"]` → `(True, False)`
  - `["-m"]` → `(False, True)`
  - `["-c", "-m"]` → `(False, True)` (last wins: `-m`)
  - `["-m", "-c"]` → `(True, False)` (last wins: `-c`)
  - `["-cm"]` → `(True, False)` (combined short flag: `-c` after `-m` in argv string)
  - `["-mc"]` → `(True, False)` (combined: `-c` wins)
  - `["-l", "-m", "-c", "-w"]` → `(True, False)` (irrelevant flags ignored)
  - `["-l", "-c", "-m", "-w"]` → `(False, True)`
  - repeated flags: `["-c", "-c"]` → `(True, False)`

### Task 011 — `-m` flag wired into CLI
- Add `-m` click option; call `_resolve_bytes_chars(sys.argv[1:])` to resolve byte/char mode
- Create `tests/fixtures/cafe.txt` (UTF-8 "café\n", 6 bytes, 5 chars)
- Golden files: `cafe.{m,c,cm,mc}.expected`
- Integration tests in `test_cli.py`: `test_flag_m_ascii`, `test_flag_m_utf8`
- Extend `test_oracle.py`: CLI-level string-comparison oracle cases for `-m` on ASCII fixtures; multibyte fixture oracle case marked `xfail(strict=False, reason="locale encoding resolution may differ BSD/GNU")`

### Task 012 — `-L` flag (longest line)
- Add `-L` option, pass through to formatter (`make_total` already implements max-not-sum)
- Create `tests/fixtures/lines.txt` (known longest line = 25 chars)
- Golden files: `lines.{L,lL}.expected`
- Extend `test_oracle.py`: CLI-level string-comparison oracle cases for `-L`; convert Task 006 semantic `-L` cases to string comparison; tab-expansion cases remain `xfail`

### Task 013 — Multiple files with total row
- Add total row when `len(processed_files) > 1`; total uses string `"total"` as filename
- Create `tests/fixtures/small.txt`
- Golden file: `hello_and_small.default.expected` (2 file rows + total row)
- Extend `test_oracle.py`: multi-file string-comparison oracle case verifying full output (per-file rows + total row) matches system `wc` exactly

### Task 014 — Multi-file `-L` total is max, not sum
- Covered by `formatter.make_total` (already correct); this task adds explicit test coverage proving it
- Create `tests/fixtures/short_lines.txt`, `long_lines.txt`
- Golden file: `short_and_long_lines.L.expected` (total = max not sum)

### Task 015 — Error handling hardening
- Handle permission denied, `IsADirectoryError`, all-files-fail case
- Total row printed only for successfully processed files (if >1 succeeded)
- Tests: `test_all_missing_files_exit_1`, `test_two_valid_one_missing_shows_total`, `test_directory_as_argument`

### Task 016 — Column width scaling (two-pass refactor)
- Refactor CLI output loop: count all files first, then format all rows
- All rows use the widest column width required by any single file
- Tests: wide-column consistency across files in same invocation

### Task 017 — Stdin via `-` argument
- `-` as filename reads from stdin, displays no filename (matching BSD behavior)
- Golden file: `dash_stdin.default.expected`
- Tests: `test_dash_reads_stdin`, `test_dash_and_file`, `test_dash_in_middle`

### Task 018 — README + documentation
- Fill in `README.md`: synopsis, installation, usage examples, flags table, known deviations from BSD wc
- No code changes; pre-commit hooks must pass on new content

---

## Final File Layout

```
pywcsk/
  __init__.py, cli.py, counter.py, formatter.py

tests/
  test_basic.py, test_counter.py, test_formatter.py, test_flag_precedence.py, test_cli.py, test_golden.py, test_oracle.py
  fixtures/: empty.txt, hello.txt, multi.txt, cafe.txt, lines.txt, small.txt,
             short_lines.txt, long_lines.txt
  golden/: ~17 *.expected files

.specify/
  constitution.md, spec.md, plan.md, tasks/001-018-*.md

.claude/commands/
  (generated by specify init — slash commands for Claude Code)
```

---

## Verification

After each task: `pre-commit run --all-files && pytest --verbose --cov=pywcsk`

Run oracle tests separately (requires system `wc`):
```bash
pytest -m oracle --verbose          # compare against system wc
pytest -m "not oracle" --verbose    # standard suite without oracle tests
```

End-to-end smoke tests (after Task 008+):
```bash
echo "hello world" | pywcsk                    # → "      1       2      11"
pywcsk -l tests/fixtures/hello.txt             # → "      1 tests/fixtures/hello.txt"
pywcsk tests/fixtures/hello.txt tests/fixtures/small.txt  # 3 rows including total
```
