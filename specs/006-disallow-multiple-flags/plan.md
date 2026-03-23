# Plan: Disallow Multiple Counting Flags

**Branch**: 006-disallow-multiple-flags

## Where to Enforce the Constraint

**CLI layer only — first line of `main()`.**

Three options were considered:

| Location | Verdict | Reason |
|----------|---------|--------|
| Click `callback` on each option | Rejected | Callbacks fire before all options are parsed; can't see the full flag set at callback time |
| Click `cls=` custom command subclass | Rejected | Over-engineering for a one-line guard |
| First line of `main()` body | Chosen | All flags are resolved by the time `main()` is called; simple, readable, easy to extend |

`counter.py` is not touched. The constraint is a CLI concern, not a counting concern.

## How Click Handles Multiple `is_flag` Options

Click parses all flags independently and passes them as booleans to `main()`.
When `-l -w` is given, both `show_lines=True` and `show_words=True` are passed.
Click itself does not enforce mutual exclusion — that is left to the application.

The guard reads:

```python
if sum([show_lines, show_words]) > 1:
    raise click.UsageError("only one counting flag (-l, -w) may be used at a time")
```

`click.UsageError` writes `"Error: <message>"` to stderr, appends the usage
line, and exits with code **2**. This is Click's standard usage error path —
no custom exit code handling required.

`sum([show_lines, show_words])` is preferred over `show_lines and show_words`
because it extends cleanly to three flags when `-c` is added: just append to
the list. No logic change needed at that point.

## Impact on Existing Code

The guard is inserted as the **first statement** in `main()` before any I/O.
The rest of `main()` is unchanged — the existing `if/else` for stdin vs files
and the `counts.words if show_words else counts.lines` selection are untouched.

No changes to `counter.py`, `Counts`, `analyze()`, or any test file other
than adding `tests/test_flag_validation.py`.

## Test Strategy

All tests are integration tests via `CliRunner`. No unit tests — the guard
is a one-line expression with no extractable pure logic.

**New file: `tests/test_flag_validation.py`**

Follows the per-feature test file pattern. Contains one class:

```
class TestFlagValidation:
    test_no_flag_unchanged          # AC1 — regression
    test_flag_l_unchanged           # AC2 — regression
    test_flag_w_unchanged           # AC3 — regression
    test_l_and_w_exits_nonzero      # AC4
    test_w_and_l_exits_nonzero      # AC5 — order independence
    test_l_and_w_stdin_exits_nonzero # AC6 — stdin path
    test_error_message_content      # AC7
```

**Regression guards (AC1–AC3)** confirm the guard does not fire for zero or
one flag. These run against existing fixtures so any breakage is immediately
visible.

**Order tests (AC4, AC5)** use identical inputs in different flag order.
Both must exit 2 — Click resolves flags independently of order so both
should pass, but explicit testing prevents a future refactor from
accidentally making order matter.

**Error message test (AC7)** asserts the stderr string contains
`"only one counting flag"` — a substring match, not exact, so minor
wording changes don't break the test.

**No oracle tests** — `wc` accepts multiple flags without error; the error
behaviour is an intentional deviation.

## Constraints

- `counter.py` unchanged.
- All existing 89 tests continue to pass.
- The `sum([...]) > 1` pattern must be used so adding `-c` later requires
  only appending to the list, not restructuring the condition.
