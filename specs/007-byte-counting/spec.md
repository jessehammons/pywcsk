# Spec: Byte Counting (`-c`)

**Branch**: 007-byte-counting
**Status**: Merged
**Reference**: BSD `wc(1)` — `-c` flag behaviour

## Goal

Count the number of bytes in one or more files, or in stdin when no files are
given. Output is a right-justified integer (minimum 7 characters wide) followed
by the filename (omitted for stdin). The byte count equals `len(data)` —
the total number of raw bytes in the input, regardless of encoding.

## Bytes vs Characters

`-c` counts **bytes**, not characters. For ASCII input these are equal. For
multibyte encodings (e.g. UTF-8), they differ:

| Input | Bytes (`-c`) | Chars (`-m`) |
|-------|-------------|-------------|
| `"hello\n"` | 6 | 6 |
| `"café\n"` | 6 | 5 (`é` is 2 bytes) |

`-m` (character counting) is a future feature. This spec covers `-c` only.
`Counts.bytes_count` stores the raw byte count; a future `Counts.chars` field
will store the character count when `-m` is implemented.

## Acceptance Criteria

| ID | Given | When | Then |
|----|-------|------|------|
| AC1 | `hello.txt` contains `"hello\n"` (6 bytes) | `pywcsk -c hello.txt` | stdout is `      6 hello.txt\n`, exit 0 |
| AC2 | `empty.txt` is 0 bytes | `pywcsk -c empty.txt` | stdout is `      0 empty.txt\n`, exit 0 |
| AC3 | `multi.txt` contains `"one two\nthree four\nfive\n"` (24 bytes) | `pywcsk -c multi.txt` | stdout is `     24 multi.txt\n`, exit 0 |
| AC4 | `no_newline.txt` contains `"hello"` (5 bytes, no trailing newline) | `pywcsk -c no_newline.txt` | stdout is `      5 no_newline.txt\n`, exit 0 |
| AC5 | `"hello world\n"` on stdin (12 bytes) | `pywcsk -c` (no args) | stdout is `     12\n`, no filename |
| AC6 | empty stdin | `pywcsk -c` (no args) | stdout is `      0\n` |
| AC7 | `-c` combined with `-l` or `-w` | `pywcsk -c -l file` | stderr contains error, exit 2 |

## Notes

- AC4 confirms bytes are counted regardless of trailing newline — unlike line
  counting, where a missing final `\n` yields 0 lines.
- AC7 confirms the existing multi-flag guard (feature 006) covers `-c`. The
  `sum([show_lines, show_words, show_bytes])` guard in `cli.py` must be
  extended to include `show_bytes` as part of this feature.
- No oracle tests for multibyte input — `wc -c` behaviour on non-ASCII is
  platform-consistent (always raw bytes), so fixture files remain ASCII-only.
  The bytes-vs-chars distinction is documented above and deferred to `-m`.

## Flag Interaction with Feature 006

Feature 006 guards against multiple counting flags using:
```
sum([show_lines, show_words]) > 1
```
This feature extends that guard to:
```
sum([show_lines, show_words, show_bytes]) > 1
```
The skipped tests `test_l_and_c_exits_nonzero` and `test_w_and_c_exits_nonzero`
in `tests/test_flag_validation.py` must be unskipped as part of this feature.

## Test Coverage Mapping

| AC | Unit test | Integration test | Oracle test |
|----|-----------|-----------------|-------------|
| AC1 | `TestCountBytes::test_hello` | `TestFlagCFiles::test_hello_file` | `test_oracle_bytes_hello` |
| AC2 | `TestCountBytes::test_empty` | `TestFlagCFiles::test_empty_file` | `test_oracle_bytes_empty` |
| AC3 | `TestCountBytes::test_multi` | `TestFlagCFiles::test_multi_file` | `test_oracle_bytes_multi` |
| AC4 | `TestCountBytes::test_no_trailing_newline` | `TestFlagCFiles::test_no_newline_file` | `test_oracle_bytes_no_newline` |
| AC5 | — | `TestFlagCStdin::test_stdin_bytes` | `test_oracle_bytes_stdin` |
| AC6 | — | `TestFlagCStdin::test_stdin_empty` | — |
| AC7 | — | `TestFlagValidation::test_l_and_c_exits_nonzero`, `TestFlagValidation::test_w_and_c_exits_nonzero` | — |
