# Spec: Count Words

**Branch**: 003-count-words
**Status**: Active
**Reference**: BSD `wc(1)` — `-w` flag and word-counting behaviour

## Goal

Count the number of words in one or more files, or in stdin when no files are
given. Output is a right-justified integer (minimum 7 characters wide) followed
by the filename (omitted for stdin).

A **word** is defined as a maximal sequence of non-whitespace characters. Word
boundaries are any characters for which `iswspace(3)` returns true. For ASCII
input this is: space (` `), tab (`\t`), newline (`\n`), carriage return (`\r`),
form feed (`\f`), and vertical tab (`\v`). This matches Python's `bytes.split()`
with no argument.

Note: unlike line counting, a word at end-of-file with **no trailing newline**
still counts. Words are separated by whitespace; the presence or absence of a
final newline does not affect the count.

## Acceptance Criteria

| ID | Given | When | Then |
|----|-------|------|------|
| AC1 | `hello.txt` contains `"hello\n"` | `pywcsk -w hello.txt` | stdout is `      1 hello.txt\n`, exit 0 |
| AC2 | `empty.txt` is 0 bytes | `pywcsk -w empty.txt` | stdout is `      0 empty.txt\n`, exit 0 |
| AC3 | `multi.txt` contains `"one two\nthree four\nfive\n"` | `pywcsk -w multi.txt` | stdout is `      5 multi.txt\n`, exit 0 |
| AC4 | `"  hello   world  \n"` (multiple spaces) | `pywcsk -w` (stdin) | stdout is `      2\n` |
| AC5 | `"hello\tworld\n"` (tab separator) | `pywcsk -w` (stdin) | stdout is `      2\n` |
| AC6 | `"   \n"` (whitespace only) | `pywcsk -w` (stdin) | stdout is `      0\n` |
| AC7 | `"hello"` (no trailing newline) | `pywcsk -w` (stdin) | stdout is `      1\n` |
| AC8 | `"hello\nworld\n"` (words across lines) | `pywcsk -w` (stdin) | stdout is `      2\n` |
| AC9 | empty stdin | `pywcsk -w` (no args) | stdout is `      0\n` |

## Word Splitting Rules

Python's `bytes.split()` (no argument) matches `iswspace` for all ASCII
characters. This is the canonical implementation. Specifically:

- Multiple consecutive whitespace characters count as a single delimiter
- Leading and trailing whitespace is ignored
- A file containing only whitespace has 0 words
- A file with no trailing newline: the final token still counts as a word

## Known Deviations from BSD `wc`

- Column width is fixed at 7 characters in this increment; dynamic width
  scaling is deferred to a later feature.
- Default output (lines + words + bytes together) is deferred; this feature
  adds only the `-w` flag.
- Unicode/multibyte word splitting is not implemented; input is treated as
  a byte sequence and split on ASCII whitespace only.

## Test Coverage Mapping

| AC | Unit test | Integration test | Oracle test |
|----|-----------|-----------------|-------------|
| AC1 | `test_count_words_hello` | `test_cli_hello_file` | `test_oracle_hello` |
| AC2 | `test_count_words_empty` | `test_cli_empty_file` | `test_oracle_empty` |
| AC3 | `test_count_words_multi` | `test_cli_multi_file` | `test_oracle_multi` |
| AC4 | `test_count_words_multiple_spaces` | `test_cli_stdin_multiple_spaces` | — |
| AC5 | `test_count_words_tab` | `test_cli_stdin_tab` | — |
| AC6 | `test_count_words_whitespace_only` | `test_cli_stdin_whitespace_only` | — |
| AC7 | `test_count_words_no_newline` | `test_cli_stdin_no_newline` | — |
| AC8 | `test_count_words_across_lines` | `test_cli_stdin_multi_line` | `test_oracle_stdin_multi` |
| AC9 | `test_count_words_empty` | `test_cli_stdin_empty` | — |
