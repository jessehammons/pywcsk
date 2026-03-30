# Spec: Default Combined Output

**Branch**: 009-default-combined-output
**Status**: Merged
**Reference**: BSD `wc(1)` — default (no-flag) output behaviour

## Goal

Align `pywcsk` default behaviour with standard `wc`: when no counting flags are
given, output lines, words, and bytes together in fixed column order. This
replaces the previous no-flag default of line count only, which was a temporary
placeholder established in feature 002.

## Non-Goals

- Dynamic column width (column width remains fixed at 7)
- Totals row for multiple files (deferred to feature 011)
- Additional flags (`-m` character count, `-L` max line length)

## Dependencies

- Feature 007 (`-c` byte counting) — must be merged; `Counts.bytes_count` must
  be populated by `analyze()`. ✅ Complete.
- Feature 008 (combined flags) — must be merged; `_format_counts()` must exist.
  ✅ Complete.

## Breaking Change

This is a deliberate breaking change to the no-flag default:

| | Before (002) | After (009) |
|--|--------------|-------------|
| `pywcsk hello.txt` | `      1 hello.txt` | `      1       1       6 hello.txt` |
| `pywcsk` with `"hello world\n"` on stdin | `      1` | `      1       2      12` |

Single-flag behaviour (`-l`, `-w`, `-c`) and combined-flag behaviour (`-l -w -c`)
are **unchanged**.

## Implementation

The only source change is in `_format_counts()` in `pywcsk/cli.py`. The
`if not parts` branch currently appends only `counts.lines`. Change it to
extend with all three in fixed order:

```python
# before
if not parts:
    parts.append(f"{counts.lines:>7}")

# after
if not parts:
    parts.extend([
        f"{counts.lines:>7}",
        f"{counts.words:>7}",
        f"{counts.bytes_count:>7}",
    ])
```

Column order (lines → words → bytes) is structurally enforced by the order of
the `extend` call — it cannot be affected by any flag or input value.

No other source changes required.

## Deletions and Modifications

### Existing tests to update (expected value change only)

Two existing tests assert the old single-column no-flag behaviour and must be
updated to expect three-column output. Both keep their existing name.

| File | Test | Old assertion | New assertion |
|------|------|--------------|---------------|
| `tests/test_flag_validation.py` | `test_no_flag_unchanged` | `"      1\n"` | `"      1       2      12\n"` (stdin uses `HELLO = b"hello world\n"`: 1 line, 2 words, 12 bytes) |
| `tests/test_combined_flags.py` | `test_no_flag_unchanged` | `f"      1 {HELLO_FILE}\n"` | `f"      1       1       6 {HELLO_FILE}\n"` |

### Comments and documentation to update

Two stale docstrings describe the default output as "line count only" and must
be updated:

| File | Test | Stale docstring | Updated docstring |
|------|------|----------------|-------------------|
| `tests/test_flag_validation.py` | `test_no_flag_unchanged` | `"AC1: no flags still outputs line count, exits 0."` | `"AC1: no flags outputs lines, words, and bytes, exits 0."` |
| `tests/test_combined_flags.py` | `test_no_flag_unchanged` | `"AC11: no flags still outputs line count only."` | `"AC11: no flags outputs lines, words, and bytes."` |

## Acceptance Criteria

Fixtures:

- `hello.txt` → 1 line, 1 word, 6 bytes
- `multi.txt` → 3 lines, 5 words, 24 bytes
- `empty.txt` → 0 lines, 0 words, 0 bytes
- `no_newline.txt` → 0 lines, 1 word, 5 bytes
- stdin `"hello world\n"` → 1 line, 2 words, 12 bytes

| ID | Given | When | Then |
|----|-------|------|------|
| AC1a | `hello.txt` | `pywcsk hello.txt` (no flags) | stdout is `      1       1       6 hello.txt\n`, exit 0 |
| AC1b | `multi.txt` | `pywcsk multi.txt` (no flags) | stdout is `      3       5      24 multi.txt\n`, exit 0 |
| AC1c | `no_newline.txt` | `pywcsk no_newline.txt` (no flags) | stdout is `      0       1       5 no_newline.txt\n`, exit 0 |
| AC2 | `"hello world\n"` on stdin | `pywcsk` (no flags) | stdout is `      1       2      12\n`, no filename, exit 0 |
| AC3 | any input | column format | each column is right-aligned in a 7-character field; columns are separated by a single space; verified by exact string assertions in AC1–AC2 |
| AC4a | `hello.txt` | `pywcsk hello.txt` vs `wc hello.txt` | integer column values match system `wc` |
| AC4b | `multi.txt` | `pywcsk multi.txt` vs `wc multi.txt` | integer column values match system `wc` |
| AC5a | `-l` only | `pywcsk -l hello.txt` | stdout is `      1 hello.txt\n` — single-flag unchanged |
| AC5b | `-w` only | `pywcsk -w hello.txt` | stdout is `      1 hello.txt\n` — single-flag unchanged |
| AC5c | `-c` only | `pywcsk -c hello.txt` | stdout is `      6 hello.txt\n` — single-flag unchanged |
| AC6 | `-l -w -c` | `pywcsk -l -w -c hello.txt` | stdout is `      1       1       6 hello.txt\n` — combined-flag output unchanged; satisfied by existing `TestCombinedFlags::test_l_w_c_file` from feature 008, no new test required |
| AC7 | `empty.txt` | `pywcsk empty.txt` (no flags) | stdout is `      0       0       0 empty.txt\n`, exit 0 |
| AC8 | no flags | `pywcsk hello.txt` | column values individually match `count_lines()`, `count_words()`, `count_bytes()` — verified by AC1a and the existing unit test suite |

**Notes on specific ACs:**

- AC1c and AC7 distinguish correct three-column output from an accidental
  single-column match — a file with 0 lines and 0 bytes would expose a
  regression that AC1a/AC1b would not.
- AC3 has no dedicated test — it is verified implicitly by the exact string
  assertions in AC1 and AC2. A dedicated formatting test would duplicate those
  assertions without adding coverage.
- AC4 (oracle) uses integer column comparison, not string equality, making it
  platform-safe across BSD and GNU `wc` column-width differences.
- AC5a–AC5c all use `hello.txt`. This is intentional — their purpose is to
  confirm flag routing (the `if not parts` branch is not reached when a flag is
  set), not fixture coverage.
- AC6 is satisfied by the existing `TestCombinedFlags::test_l_w_c_file` from
  feature 008. No new test is added — the existing test already guards this
  path. If the `if not parts` branch incorrectly triggers when all three flags
  are set, that test would catch it.
- AC7 (empty file) and AC1c (no trailing newline) are not oracle-tested —
  excluded as a conservative choice. Both BSD and GNU `wc` agree on their
  output for these fixtures, but the integration tests are sufficient given the
  values are already verified and pinned.
- AC2 (stdin, no flags) has no oracle test — stdin oracle tests require piping
  through `subprocess`, adding complexity for minimal gain when the integration
  test already pins the exact output.

## Test Coverage Mapping

| AC | Integration test | Oracle test |
|----|-----------------|-------------|
| AC1a | `TestDefaultOutput::test_hello_file` | `test_oracle_default_hello` |
| AC1b | `TestDefaultOutput::test_multi_file` | `test_oracle_default_multi` |
| AC1c | `TestDefaultOutput::test_no_newline_file` | — |
| AC2 | `TestDefaultOutput::test_stdin` | — |
| AC3 | _(verified by AC1/AC2 exact strings)_ | — |
| AC4a | — | `test_oracle_default_hello` |
| AC4b | — | `test_oracle_default_multi` |
| AC5a | `TestDefaultOutput::test_flag_l_unchanged` | — |
| AC5b | `TestDefaultOutput::test_flag_w_unchanged` | — |
| AC5c | `TestDefaultOutput::test_flag_c_unchanged` | — |
| AC6 | _(satisfied by `TestCombinedFlags::test_l_w_c_file` — feature 008)_ | — |
| AC7 | `TestDefaultOutput::test_empty_file` | — |
| AC8 | _(verified by AC1a + existing unit suite)_ | — |

### Unit test layer (`_format_counts`)

`tests/test_formatter.py` — `TestFormatCounts` — satisfies constitution Principle III (unit test
layer) for the `_format_counts()` formatter function. Six tests cover all flag combinations
(show_lines only, show_words only, show_bytes only, all three flags, no flags, column-width
invariant) and directly verify the no-flag default branch added in this feature.

### Updated tests (existing tests, corrected expected values)

Both tests require two changes each — assertion value and docstring. See the
"Deletions and Modifications" tables above for the exact strings.

| File | Test | Assertion change | Docstring change |
|------|------|-----------------|-----------------|
| `tests/test_flag_validation.py` | `test_no_flag_unchanged` | `"      1\n"` → `"      1       2      12\n"` | "line count" → "lines, words, and bytes" |
| `tests/test_combined_flags.py` | `test_no_flag_unchanged` | `f"      1 {HELLO_FILE}\n"` → `f"      1       1       6 {HELLO_FILE}\n"` | "line count only" → "lines, words, and bytes" |
