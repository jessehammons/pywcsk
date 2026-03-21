# Spec: Count Lines

**Branch**: 002-count-lines
**Status**: Active
**Reference**: BSD `wc(1)` — `-l` flag and default line-counting behaviour

## Goal

Count the number of newline characters in one or more files, or in stdin when
no files are given. Output is a right-justified integer (minimum 7 characters
wide) followed by the filename (omitted for stdin).

A line is defined as a sequence of characters terminated by a newline `\n`.
Characters after the final newline are not counted (line count = number of `\n`
characters in the input).

## Acceptance Criteria

| ID | Given | When | Then |
|----|-------|------|------|
| AC1 | `hello.txt` contains `"hello\n"` | `pywcsk hello.txt` | stdout is `      1 hello.txt\n`, exit 0 |
| AC2 | `empty.txt` is 0 bytes | `pywcsk empty.txt` | stdout is `      0 empty.txt\n`, exit 0 |
| AC3 | `multi.txt` contains `"one two\nthree four\nfive\n"` | `pywcsk multi.txt` | stdout is `      3 multi.txt\n`, exit 0 |
| AC4 | `"hello"` (no trailing newline) | `pywcsk no_newline.txt` | line count is `0` |
| AC5 | `"hello world\n"` on stdin | `pywcsk` (no args) | stdout is `      1\n`, no filename |
| AC6 | empty stdin | `pywcsk` (no args) | stdout is `      0\n` |

## Known Deviations from BSD `wc`

- Column width is fixed at 7 characters in this increment; dynamic width scaling
  is deferred to a later feature.
- Words and bytes are not yet counted; `pywcsk` currently outputs only the line
  count. Full default output (`lines words bytes`) is a future feature.

## Test Coverage Mapping

| AC | Unit test | Integration test | Oracle test |
|----|-----------|-----------------|-------------|
| AC1 | `test_count_lines_hello` | `test_cli_hello_file` | `test_oracle_hello` |
| AC2 | `test_count_lines_empty` | `test_cli_empty_file` | `test_oracle_empty` |
| AC3 | `test_count_lines_multi` | `test_cli_multi_file` | `test_oracle_multi` |
| AC4 | `test_count_lines_no_newline` | `test_cli_no_newline_file` | `test_oracle_no_newline` |
| AC5 | — | `test_cli_stdin` | `test_oracle_stdin` |
| AC6 | — | `test_cli_empty_stdin` | — |
