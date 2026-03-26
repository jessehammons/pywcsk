# Spec: Combined Flags (`-l -w -c`)

**Branch**: 008-combined-flags-lwc
**Status**: Active
**Reference**: BSD `wc(1)` — multi-flag output behaviour

## Goal

Allow any combination of counting flags (`-l`, `-w`, `-c`) to be used together
in a single invocation. When multiple flags are given, the output includes one
right-justified column per selected count, in fixed order: lines, words, bytes —
regardless of the order flags appear on the command line. This removes the
temporary single-flag restriction introduced in feature 006.

## Output Format

Each selected count is formatted as a right-justified integer in a 7-character
field. Multiple columns are separated by a single space. The filename (if any)
follows after a single space.

**Single column** (existing, unchanged):
```
      6 hello.txt
```

**Two columns** (e.g. `-l -w`):
```
      1       1 hello.txt
```

**Three columns** (`-l -w -c`):
```
      1       1       6 hello.txt
```

Column order is always: lines → words → bytes. Flag order on the command line
does not affect output column order.

## Removing the Feature 006 Restriction

Feature 006 raised a `UsageError` when more than one counting flag was given.
This feature removes that guard entirely. The `sum([show_lines, show_words,
show_bytes]) > 1` check in `cli.py` is deleted, along with the `UsageError`
it raised.

The tests in `test_flag_validation.py` that assert exit code 2 for multi-flag
input must be deleted as part of this feature:

| Test to delete | Was testing |
|----------------|-------------|
| `test_l_and_w_exits_nonzero` | `-l -w` → exit 2 |
| `test_w_and_l_exits_nonzero` | `-w -l` → exit 2 |
| `test_l_and_w_stdin_exits_nonzero` | `-l -w` on stdin → exit 2 |
| `test_error_message_content` | error message text in stderr |
| `test_l_and_c_exits_nonzero` | `-l -c` → exit 2 |
| `test_w_and_c_exits_nonzero` | `-w -c` → exit 2 |

## Acceptance Criteria

Fixtures used:

- `hello.txt` contains `"hello\n"` — 1 line, 1 word, 6 bytes
- `multi.txt` contains `"one two\nthree four\nfive\n"` — 3 lines, 5 words, 24 bytes
- stdin `"hello world\n"` — 1 line, 2 words, 12 bytes

| ID | Given | When | Then |
|----|-------|------|------|
| AC1 | `hello.txt` | `pywcsk -l -w hello.txt` | stdout is `      1       1 hello.txt\n`, exit 0 |
| AC2 | `hello.txt` | `pywcsk -w -l hello.txt` | stdout is `      1       1 hello.txt\n` — same as AC1, flag order does not change column order |
| AC3 | `hello.txt` | `pywcsk -l -c hello.txt` | stdout is `      1       6 hello.txt\n`, exit 0 |
| AC4 | `hello.txt` | `pywcsk -w -c hello.txt` | stdout is `      1       6 hello.txt\n`, exit 0 |
| AC5 | `hello.txt` | `pywcsk -l -w -c hello.txt` | stdout is `      1       1       6 hello.txt\n`, exit 0 |
| AC6 | `hello.txt` | `pywcsk -c -w -l hello.txt` | stdout is `      1       1       6 hello.txt\n` — same as AC5 |
| AC7 | `multi.txt` | `pywcsk -l -w -c multi.txt` | stdout is `      3       5      24 multi.txt\n`, exit 0 |
| AC8 | `"hello world\n"` on stdin | `pywcsk -l -w` | stdout is `      1       2\n`, no filename |
| AC9 | `"hello world\n"` on stdin | `pywcsk -l -c` | stdout is `      1      12\n`, no filename |
| AC10 | `"hello world\n"` on stdin | `pywcsk -l -w -c` | stdout is `      1       2      12\n`, no filename |
| AC11 | no flags | `pywcsk hello.txt` | stdout is `      1 hello.txt\n` — default behavior unchanged |
| AC12 | `-l` only | `pywcsk -l hello.txt` | stdout is `      1 hello.txt\n` — single-flag unchanged |
| AC13 | `-w` only | `pywcsk -w hello.txt` | stdout is `      1 hello.txt\n` — single-flag unchanged |
| AC14 | `-c` only | `pywcsk -c hello.txt` | stdout is `      6 hello.txt\n` — single-flag unchanged |

## Notes

- AC2 and AC6 confirm that column order is determined by flag type, not flag
  position on the command line.
- AC11–AC14 are regression guards. Single-flag and no-flag paths must be
  unaffected by the removal of the 006 guard and the new multi-column logic.
- Oracle tests compare against `wc` by parsing individual integer values, making
  them platform-safe (BSD vs GNU column width differences do not matter).
- AC4 (`-w -c hello.txt`): `hello.txt` has 1 word and 6 bytes, so both the
  words and bytes column values happen to be distinct (`1` and `6`).

## Test Coverage Mapping

| AC | Unit test | Integration test | Oracle test |
|----|-----------|-----------------|-------------|
| AC1 | — | `TestCombinedFlags::test_l_w_file` | `test_oracle_combined_l_w` |
| AC2 | — | `TestCombinedFlags::test_w_l_file` | — |
| AC3 | — | `TestCombinedFlags::test_l_c_file` | `test_oracle_combined_l_c` |
| AC4 | — | `TestCombinedFlags::test_w_c_file` | `test_oracle_combined_w_c` |
| AC5 | — | `TestCombinedFlags::test_l_w_c_file` | `test_oracle_combined_l_w_c` |
| AC6 | — | `TestCombinedFlags::test_c_w_l_file` | — |
| AC7 | — | `TestCombinedFlags::test_multi_file_all_flags` | — |
| AC8 | — | `TestCombinedFlags::test_l_w_stdin` | — |
| AC9 | — | `TestCombinedFlags::test_l_c_stdin` | — |
| AC10 | — | `TestCombinedFlags::test_l_w_c_stdin` | — |
| AC11 | — | `TestCombinedFlags::test_no_flag_unchanged` | — |
| AC12 | — | `TestCombinedFlags::test_flag_l_unchanged` | — |
| AC13 | — | `TestCombinedFlags::test_flag_w_unchanged` | — |
| AC14 | — | `TestCombinedFlags::test_flag_c_unchanged` | — |
