# Analysis: Default Combined Output

**Branch**: 009-default-combined-output
**Suite baseline**: 130 passed, 0 failed (pre-implementation)
**Oracle baseline**: 30 oracle tests pass

---

## Artifact Consistency

### spec.md → plan.md

| Spec requirement | Plan section | Consistent? |
|-----------------|-------------|-------------|
| One source change in `_format_counts()` | Section 1 | ✅ |
| Update `test_flag_validation.py::test_no_flag_unchanged` assertion + docstring | Section 2 | ✅ |
| Update `test_combined_flags.py::test_no_flag_unchanged` assertion + docstring | Section 3 | ✅ |
| New `TestDefaultOutput` with 8 integration tests | Section 4 | ✅ |
| 2 oracle tests appended, no new helpers | Section 5 | ✅ |
| AC6 satisfied by existing `TestCombinedFlags::test_l_w_c_file` — no new test | Section 4 note | ✅ |

### plan.md → tasks.md

| Plan section | Task | Consistent? |
|-------------|------|-------------|
| 1. `cli.py` one-line change | T001 | ✅ exact before/after strings match |
| 2. `test_flag_validation.py` update | T002 | ✅ exact assertion + docstring strings match |
| 3. `test_combined_flags.py` update | T003 | ✅ exact assertion + docstring strings match |
| 4. `test_default_output.py` new file | T004 | ✅ 8 tests, AC mapping matches |
| 5. `test_oracle.py` append | T005 | ✅ 2 tests, helpers named |
| pytest + pre-commit | T006 | ✅ |

---

## Current State (pre-implementation)

### Stale assertions confirmed in codebase

| File | Line | Current value | Required value |
|------|------|--------------|----------------|
| `tests/test_flag_validation.py` | 18 | `"AC1: no flags still outputs line count, exits 0."` | update docstring |
| `tests/test_flag_validation.py` | 21 | `assert result.stdout == "      1\n"` | `"      1       2      12\n"` |
| `tests/test_combined_flags.py` | 95 | `"AC11: no flags still outputs line count only."` | update docstring |
| `tests/test_combined_flags.py` | 98 | `assert result.stdout == f"      1 {HELLO_FILE}\n"` | `f"      1       1       6 {HELLO_FILE}\n"` |

### Files that do not yet exist

| File | Status |
|------|--------|
| `tests/test_default_output.py` | Does not exist — T004 |
| `test_oracle_default_hello` in `test_oracle.py` | Does not exist — T005 |
| `test_oracle_default_multi` in `test_oracle.py` | Does not exist — T005 |

---

## AC Coverage (pre-implementation)

| AC | Integration test | Oracle test | Status |
|----|-----------------|-------------|--------|
| AC1a `hello.txt` default | `TestDefaultOutput::test_hello_file` | `test_oracle_default_hello` | ❌ not implemented, no test |
| AC1b `multi.txt` default | `TestDefaultOutput::test_multi_file` | `test_oracle_default_multi` | ❌ not implemented, no test |
| AC1c `no_newline.txt` default | `TestDefaultOutput::test_no_newline_file` | — | ❌ not implemented, no test |
| AC2 stdin default | `TestDefaultOutput::test_stdin` | — | ❌ not implemented, no test |
| AC3 formatting | _(implicit in AC1/AC2)_ | — | ❌ not implemented |
| AC4a oracle hello | — | `test_oracle_default_hello` | ❌ no test |
| AC4b oracle multi | — | `test_oracle_default_multi` | ❌ no test |
| AC5a `-l` unchanged | `TestDefaultOutput::test_flag_l_unchanged` | — | ❌ no test (behaviour passes today) |
| AC5b `-w` unchanged | `TestDefaultOutput::test_flag_w_unchanged` | — | ❌ no test (behaviour passes today) |
| AC5c `-c` unchanged | `TestDefaultOutput::test_flag_c_unchanged` | — | ❌ no test (behaviour passes today) |
| AC6 combined unchanged | _(existing `TestCombinedFlags::test_l_w_c_file`)_ | — | ✅ already covered |
| AC7 `empty.txt` default | `TestDefaultOutput::test_empty_file` | — | ❌ not implemented, no test |
| AC8 no regression | _(implicit in AC1a + unit suite)_ | — | ✅ already covered |

**12 of 13 testable ACs have no dedicated test yet. 1 AC (AC6) already covered.**

---

## No Issues Found

- No conflicts between spec, plan, and tasks.
- No placeholder text in any artifact.
- T002 and T003 assertion values verified against actual `HELLO` and `HELLO_FILE`
  constants in the test files — values are correct.
- `_wc_cols([], path)` and `_pywcsk_cols([], path)` confirmed to work for the
  no-flag oracle case — the helpers accept `list[str]` and `[]` is valid.
- No new fixture files needed.
- No new oracle helpers needed.
- `AC12` docstring in `test_combined_flags.py` ("AC12: -l alone still outputs
  line count only.") is **not** stale — `-l` alone still does output line count
  only. The spec's deletion table correctly omits it.

---

## Ready to implement

All artifacts consistent. Run `/speckit.implement` to execute T001–T006.
