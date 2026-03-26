# Analysis: Combined Flags (`-l -w -c`)

**Branch**: 008-combined-flags-lwc
**Suite**: 130 passed, 0 failed — 30 oracle, 100 non-oracle

---

## Implementation Status

### `pywcsk/cli.py` — COMPLETE

Guard block removed. `_format_counts()` helper builds the column list in fixed
order (lines → words → bytes), called from both the stdin and files branches.
No dead code paths remain.

### `tests/test_flag_validation.py` — COMPLETE

6 obsolete exit-2 tests and their comment headers deleted. Module docstring,
class docstring, and regression-guard comment updated. 3 single-flag guards
retained.

### `tests/test_combined_flags.py` — COMPLETE

New file. 14 integration tests, one per AC.

### `tests/test_oracle.py` — COMPLETE

Combined-flag section appended. 4 oracle tests + `_wc_cols`/`_pywcsk_cols`
helpers.

---

## AC Coverage

| AC | Behaviour | Integration test | Oracle test | Status |
|----|-----------|-----------------|-------------|--------|
| AC1 | `-l -w hello.txt` → `      1       1 hello.txt` | `test_l_w_file` | `test_oracle_combined_l_w` | ✅ |
| AC2 | `-w -l hello.txt` → same as AC1 | `test_w_l_file` | — | ✅ |
| AC3 | `-l -c hello.txt` → `      1       6 hello.txt` | `test_l_c_file` | `test_oracle_combined_l_c` | ✅ |
| AC4 | `-w -c hello.txt` → `      1       6 hello.txt` | `test_w_c_file` | `test_oracle_combined_w_c` | ✅ |
| AC5 | `-l -w -c hello.txt` → three-column output | `test_l_w_c_file` | `test_oracle_combined_l_w_c` | ✅ |
| AC6 | `-c -w -l hello.txt` → same as AC5 | `test_c_w_l_file` | — | ✅ |
| AC7 | `-l -w -c multi.txt` → `      3       5      24 multi.txt` | `test_multi_file_all_flags` | — | ✅ |
| AC8 | `-l -w` stdin → `      1       2` | `test_l_w_stdin` | — | ✅ |
| AC9 | `-l -c` stdin → `      1      12` | `test_l_c_stdin` | — | ✅ |
| AC10 | `-l -w -c` stdin → `      1       2      12` | `test_l_w_c_stdin` | — | ✅ |
| AC11 | no flags → line count unchanged | `test_no_flag_unchanged` | — | ✅ |
| AC12 | `-l` only → line count unchanged | `test_flag_l_unchanged` | — | ✅ |
| AC13 | `-w` only → word count unchanged | `test_flag_w_unchanged` | — | ✅ |
| AC14 | `-c` only → byte count unchanged | `test_flag_c_unchanged` | `test_oracle_bytes_hello` | ✅ |

**14 of 14 ACs covered. All pass.**

---

## Dead Code Audit

Grep confirms zero remaining references to removed behaviour:

| Pattern | Matches |
|---------|---------|
| `exit_code == 2` | 0 |
| `UsageError` | 0 |
| `only one counting` | 0 |
| `sum([show` | 0 |
| `mutual exclusion` | 0 |
| `multiple flag validation` | 0 |

---

## Pre-commit

All 8 hooks pass clean: check-toml, check-yaml, trailing-whitespace,
end-of-file-fixer, black, flake8, bandit, mypy.

Note: flake8 C901 (McCabe complexity) was triggered by the duplicated `parts`
logic before `_format_counts()` was introduced. Extracting the helper reduced
`main` from complexity 11 to 3 and also eliminated the code duplication.

---

## No Outstanding Issues

Feature 008 is complete.
