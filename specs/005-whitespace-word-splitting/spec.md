# Spec: Mixed Whitespace Word Splitting

**Branch**: 005-whitespace-word-splitting
**Status**: Merged
**Reference**: BSD `wc(1)` — word splitting via `iswspace(3)`

## Goal

Explicitly document and test that `pywcsk -w` correctly handles all ASCII
whitespace combinations as word delimiters: spaces, tabs, newlines, and
multiples of each in any combination. No code changes are required — the
existing `bytes.split()` implementation already matches `wc -w` for all these
cases. This feature adds the explicit test coverage and oracle validation that
proves it.

## What Counts as Whitespace

For ASCII input, the whitespace characters recognised by `iswspace(3)` are:

| Character | Escape | Description |
|-----------|--------|-------------|
| Space | ` ` | ASCII 0x20 |
| Tab | `\t` | ASCII 0x09 |
| Newline | `\n` | ASCII 0x0A |
| Carriage return | `\r` | ASCII 0x0D |
| Form feed | `\f` | ASCII 0x0C |
| Vertical tab | `\v` | ASCII 0x0B |

Any sequence of one or more of these characters — in any combination — counts
as a single word boundary. `bytes.split()` with no argument matches this
behaviour exactly for ASCII input.

## Acceptance Criteria

| ID | Given | When | Then |
|----|-------|------|------|
| AC1 | `b"one\t two  \nthree\t\tfour\n"` (tabs, spaces, newlines mixed) | `pywcsk -w` (stdin) | stdout is `      4\n` |
| AC2 | `b"  \t  \n  \t  \n"` (whitespace only, mixed) | `pywcsk -w` (stdin) | stdout is `      0\n` |
| AC3 | `b"one \t\n two\t \nthree\n"` (tab+space before/after newlines) | `pywcsk -w` (stdin) | stdout is `      3\n` |
| AC4 | `b"\t\none\t\ntwo \n"` (leading tabs and newlines) | `pywcsk -w` (stdin) | stdout is `      2\n` |
| AC5 | `b"a  b\t\tc\n\nd\n"` (blank line between words) | `pywcsk -w` (stdin) | stdout is `      4\n` |
| AC6 | `b"one\r\ntwo\r\n"` (CRLF line endings) | `pywcsk -w` (stdin) | stdout is `      2\n` |

## Oracle Validation

All AC1–AC5 inputs are verified to produce identical results from both
`pywcsk -w` and `wc -w` (empirically confirmed during spec authoring). These
same inputs are used as oracle tests to make the agreement machine-verifiable.

AC6 (CRLF) is unit-tested only; `wc -w` on macOS strips `\r` from the count
in some modes, making a portable oracle comparison unreliable.

## Test Coverage Mapping

| AC | Unit test | Integration test | Oracle test |
|----|-----------|-----------------|-------------|
| AC1 | `TestMixedWhitespace::test_tabs_spaces_newlines` | `TestMixedWhitespaceCLI::test_tabs_spaces_newlines` | `test_oracle_mixed_tabs_spaces_newlines` |
| AC2 | `TestMixedWhitespace::test_mixed_whitespace_only` | `TestMixedWhitespaceCLI::test_mixed_whitespace_only` | `test_oracle_mixed_whitespace_only` |
| AC3 | `TestMixedWhitespace::test_tab_space_around_newline` | `TestMixedWhitespaceCLI::test_tab_space_around_newline` | `test_oracle_tab_space_around_newline` |
| AC4 | `TestMixedWhitespace::test_leading_tabs_and_newlines` | `TestMixedWhitespaceCLI::test_leading_tabs_and_newlines` | `test_oracle_leading_tabs_and_newlines` |
| AC5 | `TestMixedWhitespace::test_blank_line_between_words` | `TestMixedWhitespaceCLI::test_blank_line_between_words` | `test_oracle_blank_line_between_words` |
| AC6 | `TestMixedWhitespace::test_crlf_line_endings` | `TestMixedWhitespaceCLI::test_crlf_line_endings` | — (see Oracle Validation) |

## Known Deviations from BSD `wc`

- Unicode whitespace (e.g. non-breaking space U+00A0) is not treated as a word
  boundary; only ASCII whitespace characters are recognised. This is consistent
  with the ASCII-only scope documented in feature 003.
