# Plan: Combined Flags (`-l -w -c`)

**Branch**: 008-combined-flags-lwc

## Architecture

Two source files change; one test file is surgically pruned; one new test file
is added; one test file gains a new section. No changes to `counter.py` —
`analyze()` already populates `lines`, `words`, and `bytes_count`.

---

## 1. `pywcsk/cli.py`

### 1a. Delete the multi-flag guard (lines 19–22)

Remove this block entirely — no replacement:

```python
if sum([show_lines, show_words, show_bytes]) > 1:
    raise click.UsageError(
        "only one counting flag (-l, -w, -c) may be used at a time"
    )
```

After deletion, `click` is still imported for `@click.command`, `@click.option`,
`@click.argument`, `@click.version_option`, `@click.get_binary_stream`, and
`@click.echo`. The `click.UsageError` path is the only dead import concern —
confirm `click` is still used elsewhere before removing any import.

### 1b. Replace single-value selection with multi-column output

The current `if show_bytes / elif show_words / else` chain in **both** the
stdin branch and the files branch produces a single `value`. Replace both
occurrences with a `parts` list evaluated in fixed order: lines → words →
bytes. The `if not parts` branch preserves the no-flag default (line count).

**Stdin branch** — replace:
```python
if show_bytes:
    value = counts.bytes_count
elif show_words:
    value = counts.words
else:
    value = counts.lines
click.echo(f"{value:>7}")
```
with:
```python
parts = []
if show_lines:
    parts.append(f"{counts.lines:>7}")
if show_words:
    parts.append(f"{counts.words:>7}")
if show_bytes:
    parts.append(f"{counts.bytes_count:>7}")
if not parts:
    parts.append(f"{counts.lines:>7}")
click.echo(" ".join(parts))
```

**Files branch** — replace:
```python
if show_bytes:
    value = counts.bytes_count
elif show_words:
    value = counts.words
else:
    value = counts.lines
click.echo(f"{value:>7} {filename}")
```
with:
```python
parts = []
if show_lines:
    parts.append(f"{counts.lines:>7}")
if show_words:
    parts.append(f"{counts.words:>7}")
if show_bytes:
    parts.append(f"{counts.bytes_count:>7}")
if not parts:
    parts.append(f"{counts.lines:>7}")
click.echo(" ".join(parts) + f" {filename}")
```

Column order is structurally enforced — the three `if` checks always run in
lines → words → bytes sequence, so CLI flag order cannot affect output order.

---

## 2. `tests/test_flag_validation.py` — full cleanup

This file currently has 9 tests across four groups. After this change:
- **6 tests are deleted** — they assert the now-removed exit-2 behavior
- **3 tests are kept** — single-flag regression guards
- **Module docstring updated** — no longer describes mutual exclusion
- **Class docstring updated** — no longer describes mutual exclusion

### Tests to delete (lines 39–76)

| Method | Why deleted |
|--------|-------------|
| `test_l_and_w_exits_nonzero` | asserts `exit_code == 2` for `-l -w` |
| `test_w_and_l_exits_nonzero` | asserts `exit_code == 2` for `-w -l` |
| `test_l_and_w_stdin_exits_nonzero` | asserts `exit_code == 2` for `-l -w` on stdin |
| `test_error_message_content` | asserts `"only one counting flag"` in stderr |
| `test_l_and_c_exits_nonzero` | asserts `exit_code == 2` for `-l -c` |
| `test_w_and_c_exits_nonzero` | asserts `exit_code == 2` for `-w -c` |

### Tests to keep (lines 17–33, unchanged)

| Method | What it guards |
|--------|---------------|
| `test_no_flag_unchanged` | no flags → line count, exit 0 |
| `test_flag_l_unchanged` | `-l` alone → line count, exit 0 |
| `test_flag_w_unchanged` | `-w` alone → word count, exit 0 |

### Docstring and comment updates

- **Line 1** module docstring: change from `"CLI integration tests for multiple
  flag validation — spec 006 AC1–AC7."` to `"CLI integration tests for
  single-flag regression guards — spec 006/008."`
- **Line 11** class docstring: change from `"Integration tests for counting flag
  mutual exclusion."` to `"Regression guards: single-flag and no-flag paths
  are unaffected by combined-flag support (spec 008)."`
- **Lines 13–15** comment block `# Regression guards — single flag...`:
  remove the `(AC1–AC3)` suffix from the comment.
- **Lines 37–66** comment blocks for the deleted groups (`# Invalid
  combinations — must error (AC4–AC6)` and `# Error message content (AC7)` and
  `# Future-proof: -c combinations`) are deleted along with their tests.

---

## 3. `tests/test_combined_flags.py` — new file

New integration test file: `TestCombinedFlags` class, 14 tests, one per AC.
Fixture files accessed via `Path(__file__).parent / "fixtures" / "<name>"`.

```
TestCombinedFlags
  test_l_w_file              AC1  -l -w hello.txt → "      1       1 hello.txt\n"
  test_w_l_file              AC2  -w -l hello.txt → same output as AC1
  test_l_c_file              AC3  -l -c hello.txt → "      1       6 hello.txt\n"
  test_w_c_file              AC4  -w -c hello.txt → "      1       6 hello.txt\n"
  test_l_w_c_file            AC5  -l -w -c hello.txt → "      1       1       6 hello.txt\n"
  test_c_w_l_file            AC6  -c -w -l hello.txt → same output as AC5
  test_multi_file_all_flags  AC7  -l -w -c multi.txt → "      3       5      24 multi.txt\n"
  test_l_w_stdin             AC8  -l -w stdin → "      1       2\n"
  test_l_c_stdin             AC9  -l -c stdin → "      1      12\n"
  test_l_w_c_stdin           AC10 -l -w -c stdin → "      1       2      12\n"
  test_no_flag_unchanged     AC11 no flags → "      1 hello.txt\n"
  test_flag_l_unchanged      AC12 -l → "      1 hello.txt\n"
  test_flag_w_unchanged      AC13 -w → "      1 hello.txt\n"
  test_flag_c_unchanged      AC14 -c → "      6 hello.txt\n"
```

Stdin tests (AC8–AC10) use `input=b"hello world\n"` (1 line, 2 words, 12 bytes).
File tests use fixture paths. AC11–AC14 share `hello.txt`.

---

## 4. `tests/test_oracle.py` — append section

Append a `# Combined-flag oracle tests (feature 008)` section. Four tests,
each running `wc` with the same flags and comparing integer columns.

Shared helpers (local to the section, not module-level):

```python
def _wc_cols(flags, path):
    result = subprocess.run(["wc"] + flags + [str(path)],
                            capture_output=True, text=True, check=True)
    return [int(x) for x in result.stdout.strip().split()
            if not x.endswith(path.name)]

def _pywcsk_cols(flags, path):
    result = CliRunner().invoke(main, flags + [str(path)])
    assert result.exit_code == 0
    return [int(x) for x in result.output.strip().split()
            if not x.endswith(path.name)]
```

Tests:

| Test | Flags | Fixture |
|------|-------|---------|
| `test_oracle_combined_l_w` | `["-l", "-w"]` | `hello.txt` |
| `test_oracle_combined_l_c` | `["-l", "-c"]` | `hello.txt` |
| `test_oracle_combined_w_c` | `["-w", "-c"]` | `hello.txt` |
| `test_oracle_combined_l_w_c` | `["-l", "-w", "-c"]` | `multi.txt` |

Parsing by integer comparison (not string equality) is platform-safe across
BSD and GNU `wc` column width differences.

---

## Dead Code Audit

All locations referencing the old single-flag restriction, verified by grep:

| Location | Line(s) | Action |
|----------|---------|--------|
| `pywcsk/cli.py` | 19–22 | Delete guard block |
| `tests/test_flag_validation.py` | 1 | Update module docstring |
| `tests/test_flag_validation.py` | 11 | Update class docstring |
| `tests/test_flag_validation.py` | 39–76 | Delete 6 tests + 3 comment headers |

No other source or test files reference the restriction. No `@pytest.mark.skip`
decorators remain from feature 006/007 (all were unskipped in 007). No
`UsageError` import or usage survives after the guard block is deleted.

---

## Test Strategy

| Layer | File | Covers |
|-------|------|--------|
| Integration | `tests/test_combined_flags.py` (new) | All 14 ACs |
| Oracle | `tests/test_oracle.py` (appended) | Combined flags vs system `wc` |
| Regression | `tests/test_flag_validation.py` (pruned) | Single-flag and no-flag paths |

---

## Constraints

- No changes to `counter.py` — all counts already populated by `analyze()`.
- No new fixture files — `hello.txt` and `multi.txt` cover all ACs.
- The `click` import in `cli.py` remains valid after guard removal.
- `Counts.chars` and `Counts.max_line_length` stay at 0 — not in scope.
