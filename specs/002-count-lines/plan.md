# Plan: Count Lines

**Branch**: 002-count-lines

## Architecture

Pipeline: `bytes → count_lines() → int → CLI formats and prints`

### New module: `pywcsk/counter.py`

Pure functions on `bytes`; no I/O, no Click imports.

```python
@dataclass
class Counts:
    lines: int = 0
    words: int = 0        # populated in a future feature
    bytes_count: int = 0  # populated in a future feature
    chars: int = 0        # populated in a future feature
    max_line_length: int = 0  # populated in a future feature

def count_lines(data: bytes) -> int: ...   # data.count(b"\n")
def analyze(data: bytes) -> Counts: ...    # returns Counts(lines=count_lines(data))
```

`Counts` is defined with all five fields now so downstream features can extend
`analyze()` without changing the data model.

### Updated: `pywcsk/cli.py`

- Read each file (or stdin) as bytes
- Call `analyze(data)` to get `Counts`
- Print `f"{counts.lines:>7} {filename}"` per file (no filename for stdin)
- Uses `click.get_binary_stream("stdin")` for CliRunner compatibility

## Test Strategy

| Layer | File | What it covers |
|-------|------|----------------|
| Unit | `tests/test_counter.py` | `count_lines()` edge cases; `analyze()` field population |
| Integration | `tests/test_count_lines.py` | CLI output format via `CliRunner` against fixture files |
| Oracle | `tests/test_oracle.py` | Line counts match system `wc -l` (integer comparison, platform-safe) |

Oracle tests are marked `@pytest.mark.oracle` and skipped if `wc` is not on
`$PATH`. Run selectively with `pytest -m oracle`.

## Fixtures

```
tests/fixtures/
    hello.txt       — "hello\n"          (1 line)
    empty.txt       — ""                 (0 lines)
    multi.txt       — 3 lines, 5 words   (3 lines)
    no_newline.txt  — "hello"            (0 lines — no trailing newline)
```
