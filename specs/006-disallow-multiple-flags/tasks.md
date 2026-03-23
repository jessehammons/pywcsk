# Tasks: Disallow Multiple Counting Flags

## Tasks

- [x] T001 Add `sum([show_lines, show_words]) > 1` guard to `pywcsk/cli.py` — raises `click.UsageError` with message `"only one counting flag (-l, -w) may be used at a time"`
- [x] T002 Create `tests/test_flag_validation.py` — integration tests for AC1–AC7 via `CliRunner`
- [x] T003 Run full test suite; confirm all 89 existing tests still pass alongside new tests
- [x] T004 Run pre-commit; confirm all hooks green
