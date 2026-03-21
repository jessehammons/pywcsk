# Plan: `-l` Flag for Line Counting

**Branch**: 004-flag-l

## Architecture

No new modules. No changes to `counter.py`. This feature is entirely a
`cli.py` change — adding `-l` as an explicit flag alongside the existing `-w`.

### Current state of `cli.py`

```python
@click.option("-w", "show_words", is_flag=True, help="Count words.")
def main(files, show_words):
    value = counts.words if show_words else counts.lines
```

The no-flag path already falls through to `counts.lines`. Adding `-l` makes
that explicit without changing the fallback.

### Change: `pywcsk/cli.py`

Add a `-l` flag in parallel with `-w`:

```python
@click.option("-l", "show_lines", is_flag=True, help="Count lines.")
@click.option("-w", "show_words", is_flag=True, help="Count words.")
def main(files, show_lines, show_words):
    value = counts.words if show_words else counts.lines
```

The `show_lines` parameter is accepted but the output logic is unchanged: when
neither flag is set, `counts.lines` is the default; when `-l` is set,
`counts.lines` is also the output. The flag's purpose here is to be
recognised without error and to set up the parameter name for the future
combined-output feature where flag presence will determine which columns print.

### No changes to `counter.py`

`count_lines()` is already implemented and fully tested. `analyze()` already
populates `counts.lines`. Nothing to extend.

## Test Strategy

| Layer | File | What it covers |
|-------|------|----------------|
| Unit | — | Not needed; `count_lines()` fully covered by existing `tests/test_counter.py` |
| Integration | `tests/test_flag_l.py` | CLI `-l` flag via `CliRunner` — files, stdin, regression for `-w` and no-flag default |
| Oracle | `tests/test_oracle.py` | Append oracle tests comparing `pywcsk -l` against `wc -l` |

### Why a new file `tests/test_flag_l.py`

Mirrors the pattern established in feature 003: one integration test file per
flag (`test_count_words.py` for `-w`, `test_flag_l.py` for `-l`). Keeps test
files focused and makes it easy to find tests for a given flag.

## Regression Strategy

Two explicit regression guards (AC7, AC8):

- `test_flag_w_unaffected` — invoke with `-w`, assert word count is in output
  and line-only format is not
- `test_no_flag_default_unchanged` — invoke with no flags, assert output still
  matches line count (feature 002 contract preserved)

## Constraints

- `counter.py` is not modified.
- Existing tests (`test_counter.py`, `test_count_lines.py`, `test_count_words.py`,
  `test_oracle.py` lines section) must continue to pass unchanged.
- Combined `-l -w` behaviour is not implemented or tested.
