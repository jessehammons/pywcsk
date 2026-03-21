# Plan: Count Words

**Branch**: 003-count-words

## Architecture

The pipeline is unchanged: `bytes → analyze() → Counts → CLI formats and prints`.
This feature extends two existing files and adds tests. No new modules needed.

### Extension: `pywcsk/counter.py`

Add `count_words()` alongside `count_lines()`:

```python
def count_words(data: bytes) -> int:
    """Return the number of whitespace-delimited tokens in data."""
    return len(data.split())
```

`bytes.split()` with no argument splits on any ASCII whitespace (`space`, `tab`,
`\n`, `\r`, `\f`, `\v`) and strips leading/trailing whitespace — exactly
matching `iswspace` behaviour for ASCII input. The return value is the length
of the resulting list; an empty or whitespace-only input returns `[]`, length 0.

Update `analyze()` to populate the `words` field:

```python
def analyze(data: bytes) -> Counts:
    return Counts(
        lines=count_lines(data),
        words=count_words(data),
    )
```

### Extension: `pywcsk/cli.py`

Add a `-w` flag. When `-w` is given, print only the word count:

```python
@click.option("-w", "show_words", is_flag=True, help="Count words.")
```

Output format mirrors `-l`: `f"{counts.words:>7} {filename}"` for files,
`f"{counts.words:>7}"` for stdin.

No flag (bare invocation) behaviour is **unchanged** — it still prints only
the line count, as in feature 002. Full default output (lines + words + bytes)
is deferred to a later feature.

### Why `-w` as a flag, not the default output

Default combined output requires column-width coordination across all three
values, a total row for multiple files, and is its own feature. Adding `-w` as
an isolated flag keeps this increment small and verifiable against `wc -w`
exactly.

## Test Strategy

| Layer | File | What it covers |
|-------|------|----------------|
| Unit | `tests/test_counter.py` | `count_words()` edge cases — empty, single, multi, spaces, tabs, no newline, whitespace-only |
| Integration | `tests/test_count_words.py` | CLI `-w` flag via `CliRunner` against fixture files and inline stdin |
| Oracle | `tests/test_oracle.py` | Add `@pytest.mark.oracle` tests comparing `pywcsk -w` against `wc -w` |

Oracle tests use integer comparison (not string) so they pass on both BSD `wc`
(7-column min) and GNU `wc` (no padding). They are appended to the existing
`tests/test_oracle.py` to keep all oracle tests in one place.

## Fixtures

Reuse existing fixtures from `tests/fixtures/`:

```
hello.txt       — "hello\n"                     → 1 word
empty.txt       — ""                             → 0 words
multi.txt       — "one two\nthree four\nfive\n"  → 5 words
no_newline.txt  — "hello"                        → 1 word  (differs from line count!)
```

No new fixture files are needed. Inline `bytes` literals in unit and
integration tests cover the whitespace edge cases (tabs, multiple spaces).

## Constraints

- `count_lines()` and its tests are not modified.
- `test_count_lines.py` and `test_oracle.py` (existing tests) are not broken.
- The `Counts.words` field already exists in the dataclass — no schema change.
