# Tasks: Default Combined Output

## Tasks

- [x] T001 In `pywcsk/cli.py` `_format_counts()`, replace `parts.append(f"{counts.lines:>7}")` in the `if not parts` branch with `parts.extend([f"{counts.lines:>7}", f"{counts.words:>7}", f"{counts.bytes_count:>7}"])`
- [x] T002 In `tests/test_flag_validation.py` `test_no_flag_unchanged`: update assertion from `"      1\n"` to `"      1       2      12\n"`; update docstring from `"AC1: no flags still outputs line count, exits 0."` to `"AC1: no flags outputs lines, words, and bytes, exits 0."`
- [x] T003 In `tests/test_combined_flags.py` `test_no_flag_unchanged`: update assertion from `f"      1 {HELLO_FILE}\n"` to `f"      1       1       6 {HELLO_FILE}\n"`; update docstring from `"AC11: no flags still outputs line count only."` to `"AC11: no flags outputs lines, words, and bytes."`
- [x] T004 Create `tests/test_default_output.py` with `TestDefaultOutput` — 8 integration tests covering AC1a–AC1c, AC2, AC5a–AC5c, AC7
- [x] T005 Append `# Default output oracle tests (feature 009)` section to `tests/test_oracle.py` with `test_oracle_default_hello` (AC4a) and `test_oracle_default_multi` (AC4b) using existing `_wc_cols` / `_pywcsk_cols` helpers with `[]` flags
- [x] T006 Run `venv/bin/pytest --tb=short -q` and `venv/bin/pre-commit run --all-files`; confirm both pass clean (re-confirmed post-T007: 146 passed, all hooks green)
- [x] T007 Create `tests/test_formatter.py` with `TestFormatCounts` — 6 unit tests covering `_format_counts()` for all flag combinations including the no-flag default (constitution Principle III: unit test layer)
