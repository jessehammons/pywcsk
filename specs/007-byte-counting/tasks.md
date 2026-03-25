# Tasks: Byte Counting (`-c`)

## Tasks

- [x] T001 Add `count_bytes()` to `pywcsk/counter.py`; update `analyze()` to populate `bytes_count`; update `Counts` docstring
- [x] T002 Fix `TestAnalyze::test_unimplemented_fields_zero` in `tests/test_counter.py` — remove `bytes_count == 0` assertion
- [x] T003 Add `TestCountBytes` class to `tests/test_counter.py` — unit tests for `count_bytes()` and `analyze().bytes_count`
- [x] T004 Add `-c` flag to `pywcsk/cli.py`; extend multi-flag guard to include `show_bytes`; replace ternary with `if/elif/else`
- [x] T005 Create `tests/test_flag_c.py` — integration tests for `-c` via `CliRunner` (AC1–AC7)
- [x] T006 Append oracle tests for `pywcsk -c` to `tests/test_oracle.py` (AC1–AC5)
- [x] T007 Unskip `test_l_and_c_exits_nonzero` and `test_w_and_c_exits_nonzero` in `tests/test_flag_validation.py`
- [x] T008 Run full test suite and pre-commit; confirm all green
