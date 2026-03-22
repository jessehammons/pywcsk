# Plan: Mixed Whitespace Word Splitting

**Branch**: 005-whitespace-word-splitting

## Architecture

No changes to any source file. `count_words()` already handles all mixed
whitespace cases correctly via `bytes.split()`. This feature is entirely
additive test coverage.

## What Already Exists

`tests/test_counter.py::TestCountWords` has:
- `test_tab_separator` — single tab delimiter
- `test_multiple_spaces` — multiple spaces as one delimiter
- `test_mixed_whitespace` — `b"a\t b \n c\n"` (tab+space, space+newline)

`tests/test_count_words.py::TestCountWordsStdin` has:
- `test_stdin_tab_separator` — single tab via CLI
- `test_stdin_multiple_spaces` — multiple spaces via CLI

What is **not yet tested** explicitly: the richer combinations from the spec
(tab+space+newline in the same input, blank lines between words, leading mixed
whitespace, CRLF), and no oracle tests exist for any mixed whitespace input.

## New Tests

### Unit tests — append to `tests/test_counter.py`

Add a new class `TestMixedWhitespace` to `test_counter.py`. Keeps mixed
whitespace unit tests grouped separately from the basic `TestCountWords`
cases, making it easy to see what this feature adds.

```python
class TestMixedWhitespace:
    """Explicit mixed whitespace tests — spec 005 AC1–AC6."""

    def test_tabs_spaces_newlines(self): ...     # AC1
    def test_mixed_whitespace_only(self): ...    # AC2
    def test_tab_space_around_newline(self): ... # AC3
    def test_leading_tabs_and_newlines(self): .. # AC4
    def test_blank_line_between_words(self): ... # AC5
    def test_crlf_line_endings(self): ...        # AC6
```

### Integration tests — new file `tests/test_whitespace_splitting.py`

New file rather than appending to `test_count_words.py` — this feature has
its own spec number and its own focused concern. Follows the one-file-per-feature
pattern established by `test_count_words.py` and `test_flag_l.py`.

Tests invoke `pywcsk -w` via `CliRunner` with the exact byte literals from
the spec ACs.

### Oracle tests — append to `tests/test_oracle.py`

Add a `# feature 005` section with oracle tests for AC1–AC5. Each test pipes
the same byte literal to both `pywcsk -w` (via CliRunner) and `wc -w` (via
subprocess) and asserts integer equality.

AC6 (CRLF) is excluded from oracle tests — BSD `wc` on macOS strips `\r`
before counting, while GNU `wc` on Linux may differ. Unit test coverage is
sufficient for this case.

## Test Strategy

| Layer | File | ACs covered |
|-------|------|-------------|
| Unit | `tests/test_counter.py` (new class) | AC1–AC6 |
| Integration | `tests/test_whitespace_splitting.py` (new file) | AC1–AC6 |
| Oracle | `tests/test_oracle.py` (appended section) | AC1–AC5 |

## Constraints

- No source files modified.
- No existing tests modified.
- Existing 72 tests must continue to pass.
