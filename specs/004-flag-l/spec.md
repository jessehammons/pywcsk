# Spec: `-l` Flag for Line Counting

**Branch**: 004-flag-l
**Status**: Merged
**Reference**: BSD `wc(1)` — `-l` flag behaviour

## Goal

Add an explicit `-l` flag that writes the number of lines to stdout, matching
`wc -l` exactly. A line is a sequence of characters terminated by a newline
`\n`; the line count equals the number of `\n` characters in the input
(unchanged from feature 002).

This makes line counting opt-in via flag, consistent with the `-w` flag added
in feature 003, and prepares for a future feature where the default output
(no flags) becomes lines + words + bytes combined.

## Acceptance Criteria

| ID | Given | When | Then |
|----|-------|------|------|
| AC1 | `hello.txt` contains `"hello\n"` | `pywcsk -l hello.txt` | stdout is `      1 hello.txt\n`, exit 0 |
| AC2 | `empty.txt` is 0 bytes | `pywcsk -l empty.txt` | stdout is `      0 empty.txt\n`, exit 0 |
| AC3 | `multi.txt` contains `"one two\nthree four\nfive\n"` | `pywcsk -l multi.txt` | stdout is `      3 multi.txt\n`, exit 0 |
| AC4 | `no_newline.txt` contains `"hello"` | `pywcsk -l no_newline.txt` | stdout is `      0 no_newline.txt\n`, exit 0 |
| AC5 | `"hello world\n"` on stdin | `pywcsk -l` (no args) | stdout is `      1\n`, no filename |
| AC6 | empty stdin | `pywcsk -l` (no args) | stdout is `      0\n` |
| AC7 | `"hello world\n"` on stdin | `pywcsk -w` (no `-l`) | stdout is `      2\n` — `-l` output absent |
| AC8 | `hello.txt` | `pywcsk hello.txt` (no flags) | stdout is `      1 hello.txt\n` — default behaviour unchanged |

## Relationship to Existing Behaviour

Feature 002 established that `pywcsk` with no flags prints the line count.
That default is **preserved unchanged** in this increment. Adding `-l` does
not alter the no-flag path; it provides an equivalent explicit form.

AC7 and AC8 are regression guards: `-l` must not interfere with `-w`, and the
no-flag default must not change.

## Flag Interaction

Combining `-l` and `-w` in a single invocation (e.g. `pywcsk -l -w file`) is
**out of scope** for this feature. Combined flag output is deferred to the
default-output feature. In this increment, if both flags are passed the
behaviour is undefined and not tested.

## Known Deviations from BSD `wc`

- Column width is fixed at 7 characters; dynamic scaling is deferred.
- Combined flag output (`-l -w`, `-l -w -c`, etc.) is deferred.

## Test Coverage Mapping

| AC | Unit test | Integration test | Oracle test |
|----|-----------|-----------------|-------------|
| AC1 | `TestCountLines::test_hello` (existing) | `TestFlagLFiles::test_hello_file` | `test_oracle_flag_l_hello` |
| AC2 | `TestCountLines::test_empty` (existing) | `TestFlagLFiles::test_empty_file` | `test_oracle_flag_l_empty` |
| AC3 | `TestCountLines::test_multi` (existing) | `TestFlagLFiles::test_multi_file` | `test_oracle_flag_l_multi` |
| AC4 | `TestCountLines::test_no_trailing_newline` (existing) | `TestFlagLFiles::test_no_newline_file` | `test_oracle_flag_l_no_newline` |
| AC5 | — | `TestFlagLStdin::test_stdin_one_line` | `test_oracle_flag_l_stdin` |
| AC6 | — | `TestFlagLStdin::test_stdin_empty` | — |
| AC7 | — | `TestFlagLRegressions::test_flag_w_unaffected` | — |
| AC8 | — | `TestFlagLRegressions::test_no_flag_default_unchanged` | — |
