# Spec: Disallow Multiple Counting Flags

**Branch**: 006-disallow-multiple-flags
**Status**: Merged
**Reference**: Intentional temporary constraint — not from BSD `wc(1)`

## Goal

Enforce that at most one counting flag (`-l`, `-w`) may be provided in a
single invocation. If more than one is given, the CLI exits with a non-zero
status and prints a clear error message to stderr. This prevents silent
incorrect output from the current undefined multi-flag behaviour and makes
the limitation explicit until a future "combined output" feature implements
`-l -w` correctly.

## Current Behaviour (Before This Feature)

`pywcsk -l -w file` silently exits 0 and outputs one value. Which value is
returned is an implementation detail of the current `if/else` branch — it is
not specified and must not be relied upon.

## Scope

Only the currently implemented counting flags are in scope: `-l` and `-w`.
When `-c` is implemented in a future feature, it will be added to this
validation at that time.

## Error Format

Uses Click's `UsageError`, which:
- writes `Error: <message>` to stderr
- prints the command usage line
- exits with code **2** (Click's standard usage error exit code)

Error message: `"only one counting flag (-l, -w) may be used at a time"`

**Testing note:** In Click 8, `CliRunner` always separates stdout and stderr.
Tests that assert on stderr content must check `result.stderr`, not
`result.output`.

## Acceptance Criteria

| ID | Given | When | Then |
|----|-------|------|------|
| AC1 | no flags | `pywcsk file` | line count output, exit 0 — default unchanged |
| AC2 | `-l` only | `pywcsk -l file` | line count output, exit 0 — unchanged |
| AC3 | `-w` only | `pywcsk -w file` | word count output, exit 0 — unchanged |
| AC4 | `-l -w` | `pywcsk -l -w file` | stderr contains error message, exit 2 |
| AC5 | `-w -l` | `pywcsk -w -l file` | stderr contains error message, exit 2 |
| AC6 | `-l -w` on stdin | `pywcsk -l -w` | stderr contains error message, exit 2 |
| AC7 | error message content | `pywcsk -l -w file` | stderr contains `"only one counting flag"` |

## Notes

- AC4 and AC5 are separate ACs because flag order must not affect the outcome.
- No oracle tests apply — `wc` does not error on multiple flags; it outputs
  combined columns, which is the eventual correct behaviour for pywcsk.
- AC1–AC3 are regression guards to confirm single-flag and no-flag paths
  are unaffected by the validation logic.

## Test Coverage Mapping

| AC | Unit test | Integration test | Oracle test |
|----|-----------|-----------------|-------------|
| AC1 | — | `TestFlagValidation::test_no_flag_unchanged` | — |
| AC2 | — | `TestFlagValidation::test_flag_l_unchanged` | — |
| AC3 | — | `TestFlagValidation::test_flag_w_unchanged` | — |
| AC4 | — | `TestFlagValidation::test_l_and_w_exits_nonzero` | — |
| AC5 | — | `TestFlagValidation::test_w_and_l_exits_nonzero` | — |
| AC6 | — | `TestFlagValidation::test_l_and_w_stdin_exits_nonzero` | — |
| AC7 | — | `TestFlagValidation::test_error_message_content` | — |

### Previously Skipped Tests (now active)

Two tests were originally marked `@pytest.mark.skip` pending `-c` flag
implementation. Both were unskipped in feature 007:

| Test | Status |
|------|--------|
| `TestFlagValidation::test_l_and_c_exits_nonzero` | Active (unskipped in 007) |
| `TestFlagValidation::test_w_and_c_exits_nonzero` | Active (unskipped in 007) |
