# Plan: Default Combined Output

**Branch**: 009-default-combined-output

## Architecture

Five files change. The source change is one line. All other changes are tests.
No changes to `counter.py` or `Counts` — all fields already populated.

---

## 1. `pywcsk/cli.py` — one line changed

In `_format_counts()`, replace the `if not parts` single-append with a
three-item extend:

```python
# before (line 21)
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

No other changes to `cli.py`. The docstring on `_format_counts` ("Return
space-joined column string for the selected counts in fixed order") remains
accurate — it does not describe the default behaviour specifically.

---

## 2. `tests/test_flag_validation.py` — update one test

`test_no_flag_unchanged` uses `input=HELLO` where `HELLO = b"hello world\n"`
(1 line, 2 words, 12 bytes). Two changes to this test:

**Assertion:** `"      1\n"` → `"      1       2      12\n"`

**Docstring:** `"AC1: no flags still outputs line count, exits 0."` →
`"AC1: no flags outputs lines, words, and bytes, exits 0."`

---

## 3. `tests/test_combined_flags.py` — update one test

`test_no_flag_unchanged` invokes `main` with `[str(HELLO_FILE)]` where
`HELLO_FILE` is `hello.txt` (1 line, 1 word, 6 bytes). Two changes:

**Assertion:** `f"      1 {HELLO_FILE}\n"` → `f"      1       1       6 {HELLO_FILE}\n"`

**Docstring:** `"AC11: no flags still outputs line count only."` →
`"AC11: no flags outputs lines, words, and bytes."`

---

## 4. `tests/test_default_output.py` — new file

New integration test class `TestDefaultOutput`, 8 tests covering AC1a–AC1c,
AC2, AC5a–AC5c, and AC7. Fixture paths via
`Path(__file__).parent / "fixtures" / "<name>"`.

```
TestDefaultOutput
  test_hello_file        AC1a  no flags, hello.txt  → "      1       1       6 {path}\n"
  test_multi_file        AC1b  no flags, multi.txt  → "      3       5      24 {path}\n"
  test_no_newline_file   AC1c  no flags, no_newline → "      0       1       5 {path}\n"
  test_stdin             AC2   no flags, stdin      → "      1       2      12\n"
  test_empty_file        AC7   no flags, empty.txt  → "      0       0       0 {path}\n"
  test_flag_l_unchanged  AC5a  -l, hello.txt        → "      1 {path}\n"
  test_flag_w_unchanged  AC5b  -w, hello.txt        → "      1 {path}\n"
  test_flag_c_unchanged  AC5c  -c, hello.txt        → "      6 {path}\n"
```

`test_stdin` uses `input=b"hello world\n"` (1 line, 2 words, 12 bytes).

AC3, AC6, and AC8 have no dedicated tests — AC3 and AC8 are verified
implicitly by the exact string assertions above; AC6 is satisfied by the
existing `TestCombinedFlags::test_l_w_c_file` from feature 008.

---

## 5. `tests/test_oracle.py` — append two tests

Append a `# Default output oracle tests (feature 009)` section. The existing
`_wc_cols(flags, path)` and `_pywcsk_cols(flags, path)` helpers from feature
008 work as-is for the no-flag case — calling them with `[]` invokes
`wc path` and `pywcsk path` respectively, and the filename-filtering logic
(`if not x.endswith(path.name)`) handles the default `wc` output format
correctly.

```python
def test_oracle_default_hello() -> None:
    """AC4a: default output column values match wc for hello.txt."""
    path = FIXTURES / "hello.txt"
    assert _pywcsk_cols([], path) == _wc_cols([], path)


def test_oracle_default_multi() -> None:
    """AC4b: default output column values match wc for multi.txt."""
    path = FIXTURES / "multi.txt"
    assert _pywcsk_cols([], path) == _wc_cols([], path)
```

No new helpers required.

---

## Test Strategy

| Layer | File | Covers |
|-------|------|--------|
| Integration | `tests/test_default_output.py` (new) | AC1a–AC1c, AC2, AC5a–AC5c, AC7 |
| Oracle | `tests/test_oracle.py` (appended) | AC4a, AC4b |
| Regression update | `tests/test_flag_validation.py` | AC1 assertion + docstring |
| Regression update | `tests/test_combined_flags.py` | AC11 assertion + docstring |

---

## Constraints

- No changes to `counter.py` — all counts already populated by `analyze()`.
- No new fixture files — all four existing fixtures cover all ACs.
- No new oracle helpers — `_wc_cols` / `_pywcsk_cols` handle `[]` flags correctly.
- `_format_counts` docstring requires no update — it does not describe the default.
- `main` docstring ("Count lines, words, and bytes — a Python implementation of wc")
  already accurately describes the default; no update needed.
