# Plan: Byte Counting (`-c`)

**Branch**: 007-byte-counting

## Architecture

Three files change. No new modules.

### 1. `pywcsk/counter.py` — add `count_bytes()`

```python
def count_bytes(data: bytes) -> int:
    """Return the number of bytes in data."""
    return len(data)
```

Update `analyze()` to populate `bytes_count`:

```python
def analyze(data: bytes) -> Counts:
    return Counts(
        lines=count_lines(data),
        words=count_words(data),
        bytes_count=count_bytes(data),
    )
```

`Counts.bytes_count` already exists in the dataclass — no schema change.
The docstring on `Counts` ("Fields beyond `lines` are populated by future
features") should be updated to reflect that `lines`, `words`, and
`bytes_count` are now all populated.

### 2. `pywcsk/cli.py` — two changes

**Add `-c` flag:**

```python
@click.option("-c", "show_bytes", is_flag=True, help="Count bytes.")
def main(files, show_lines, show_words, show_bytes):
```

**Extend multi-flag guard:**

```python
if sum([show_lines, show_words, show_bytes]) > 1:
    raise click.UsageError(
        "only one counting flag (-l, -w, -c) may be used at a time"
    )
```

Note the error message text changes slightly — `(-l, -w)` becomes
`(-l, -w, -c)`. The existing test `test_error_message_content` asserts
`"only one counting flag"` as a substring, so it will continue to pass
without modification.

**Extend value selection:**

```python
if show_bytes:
    value = counts.bytes_count
elif show_words:
    value = counts.words
else:
    value = counts.lines
```

Replaces the current `counts.words if show_words else counts.lines` ternary.
`show_bytes` takes priority in the elif chain; the no-flag default (`counts.lines`)
is preserved at the end.

### 3. `tests/test_flag_validation.py` — unskip two tests

Remove `@pytest.mark.skip` from `test_l_and_c_exits_nonzero` and
`test_w_and_c_exits_nonzero`. These tests were written in feature 006
anticipating this moment — they require no other changes.

## Test Strategy

| Layer | File | What it covers |
|-------|------|----------------|
| Unit | `tests/test_counter.py` (new class `TestCountBytes`) | `count_bytes()` edge cases; `analyze()` populates `bytes_count` |
| Integration | `tests/test_flag_c.py` (new file) | `-c` flag via `CliRunner` — files, stdin, regression for `-l`/`-w`/no-flag |
| Oracle | `tests/test_oracle.py` (appended section) | `pywcsk -c` vs `wc -c` on all four fixtures + stdin |
| Validation | `tests/test_flag_validation.py` (unskip 2 tests) | `-l -c` and `-w -c` now error correctly |

## `test_counter.py` — `TestAnalyze` update

`test_unimplemented_fields_zero` currently asserts `counts.bytes_count == 0`.
Once `analyze()` populates `bytes_count`, this test will fail. It must be
updated to remove the `bytes_count` assertion (or split into a separate check
for genuinely unimplemented fields: `chars` and `max_line_length`).

## Constraints

- `Counts.chars` and `Counts.max_line_length` remain 0 — not populated here.
- No fixture files added — all four existing fixtures cover AC1–AC4.
- The no-flag default (line count) is unchanged.
- `test_error_message_content` in `test_flag_validation.py` passes unchanged
  because it uses a substring match.
