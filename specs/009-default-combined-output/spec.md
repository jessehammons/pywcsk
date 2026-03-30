# Spec: Default Combined Output

**Branch**: 009-default-combined-output
**Status**: Active
**Reference**: BSD `wc(1)` — default (no-flag) output behaviour

## Goal

When no counting flags are given, output all three counts — lines, words, bytes
— in the standard column order, matching `wc` default behaviour. This replaces
the previous no-flag default of line count only (a temporary placeholder
established in feature 002).

## Breaking Change

This is a deliberate breaking change to the no-flag default:

| | Before (002) | After (009) |
|--|--------------|-------------|
| `pywcsk hello.txt` | `      1 hello.txt` | `      1       1       6 hello.txt` |
| `pywcsk` with `"hello world\n"` on stdin | `      1` | `      1       2      12` |

Single-flag behaviour (`-l`, `-w`, `-c`) is **unchanged**.

## Implementation

The only source change is in `_format_counts()` in `pywcsk/cli.py`. The
`if not parts` branch currently appends only `counts.lines`. Change it to
append all three:

```python
# before
if not parts:
    parts.append(f"{counts.lines:>7}")

# after
if not parts:
    parts.extend([
        f"{counts.lines:>7}",
        f"{counts.words:>7}",
        f"{counts.bytes_count:>7}",
    ])
```

No other source changes required.

## Test Updates Required

Two existing tests assert the old single-column no-flag behaviour and must be
updated to expect three-column output:

| File | Test | Old assertion | New assertion |
|------|------|--------------|---------------|
| `tests/test_flag_validation.py` | `test_no_flag_unchanged` | `"      1\n"` | `"      1       1       6\n"` (stdin) |
| `tests/test_combined_flags.py` | `test_no_flag_unchanged` | `f"      1 {HELLO_FILE}\n"` | `f"      1       1       6 {HELLO_FILE}\n"` |

Both tests keep their existing name — the behaviour they guard (no-flag path
working correctly) is unchanged; only the expected output value updates.

## Acceptance Criteria

Fixtures:

- `hello.txt` → 1 line, 1 word, 6 bytes
- `multi.txt` → 3 lines, 5 words, 24 bytes
- `empty.txt` → 0 lines, 0 words, 0 bytes
- `no_newline.txt` → 0 lines, 1 word, 5 bytes
- stdin `"hello world\n"` → 1 line, 2 words, 12 bytes

| ID | Given | When | Then |
|----|-------|------|------|
| AC1 | `hello.txt` | `pywcsk hello.txt` (no flags) | stdout is `      1       1       6 hello.txt\n`, exit 0 |
| AC2 | `multi.txt` | `pywcsk multi.txt` (no flags) | stdout is `      3       5      24 multi.txt\n`, exit 0 |
| AC3 | `empty.txt` | `pywcsk empty.txt` (no flags) | stdout is `      0       0       0 empty.txt\n`, exit 0 |
| AC4 | `no_newline.txt` | `pywcsk no_newline.txt` (no flags) | stdout is `      0       1       5 no_newline.txt\n`, exit 0 |
| AC5 | `"hello world\n"` on stdin | `pywcsk` (no flags) | stdout is `      1       2      12\n`, no filename |
| AC6 | `-l` only | `pywcsk -l hello.txt` | stdout is `      1 hello.txt\n` — single-flag unchanged |
| AC7 | `-w` only | `pywcsk -w hello.txt` | stdout is `      1 hello.txt\n` — single-flag unchanged |
| AC8 | `-c` only | `pywcsk -c hello.txt` | stdout is `      6 hello.txt\n` — single-flag unchanged |

AC3 and AC4 exercise edge cases (empty file and no-trailing-newline) that
distinguish correct three-column default output from a lucky single-column
match.

AC6–AC8 are regression guards confirming the `if not parts` branch is only
reached when no flags are set. All three use `hello.txt` — this is intentional
since their purpose is to confirm flag routing, not fixture coverage. The
fixture values themselves are covered by AC1–AC4.

AC5 (stdin, no flags) has no oracle test. This is intentional — stdin oracle
tests require piping input through `subprocess`, which adds complexity for
minimal gain when the integration test already pins the exact output.

## Test Coverage Mapping

| AC | Integration test | Oracle test |
|----|-----------------|-------------|
| AC1 | `TestDefaultOutput::test_hello_file` | `test_oracle_default_hello` |
| AC2 | `TestDefaultOutput::test_multi_file` | `test_oracle_default_multi` |
| AC3 | `TestDefaultOutput::test_empty_file` | — |
| AC4 | `TestDefaultOutput::test_no_newline_file` | — |
| AC5 | `TestDefaultOutput::test_stdin` | — |
| AC6 | `TestDefaultOutput::test_flag_l_unchanged` | — |
| AC7 | `TestDefaultOutput::test_flag_w_unchanged` | — |
| AC8 | `TestDefaultOutput::test_flag_c_unchanged` | — |

### Updated Tests (not new — existing tests with corrected expected values)

| File | Test | Change |
|------|------|--------|
| `tests/test_flag_validation.py` | `test_no_flag_unchanged` | Update expected stdout |
| `tests/test_combined_flags.py` | `test_no_flag_unchanged` | Update expected stdout |

## Notes

- Oracle tests for AC1 and AC2 compare integer column values against system
  `wc` (no flags), using the same `_wc_cols` / `_pywcsk_cols` helper pattern
  established in feature 008.
- AC3 (empty file) and AC4 (no newline) are not oracle-tested — excluded as a
  conservative choice. These fixtures are simple ASCII and both BSD and GNU `wc`
  agree on their output, but the integration tests alone are sufficient given
  that the fixture values are already verified and pinned.
- The `if not parts` branch in `_format_counts()` is the only code path
  changed. All flag-combination paths from feature 008 are unaffected.
