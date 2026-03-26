# Tasks: Combined Flags (`-l -w -c`)

## Tasks

- [x] T001 Delete the `sum([show_lines, show_words, show_bytes]) > 1` guard block (lines 19–22) from `pywcsk/cli.py`; confirm `click` import remains valid
- [x] T002 Replace the `if show_bytes / elif show_words / else` single-value chains in both the stdin branch and the files branch of `pywcsk/cli.py` with `parts`-list multi-column logic in fixed order (lines → words → bytes); preserve `if not parts` default
- [x] T003 Delete the 6 obsolete tests from `tests/test_flag_validation.py`: `test_l_and_w_exits_nonzero`, `test_w_and_l_exits_nonzero`, `test_l_and_w_stdin_exits_nonzero`, `test_error_message_content`, `test_l_and_c_exits_nonzero`, `test_w_and_c_exits_nonzero` — along with their three comment headers (`# Invalid combinations`, `# Error message content`, `# Future-proof: -c combinations`)
- [x] T004 Update `tests/test_flag_validation.py` module docstring (line 1) and class docstring (line 11) to remove mutual-exclusion language; strip `(AC1–AC3)` suffix from the remaining regression-guard comment
- [x] T005 Create `tests/test_combined_flags.py` with `TestCombinedFlags` — 14 integration tests covering all spec ACs (AC1–AC14)
- [x] T006 Append `# Combined-flag oracle tests (feature 008)` section to `tests/test_oracle.py` with helpers `_wc_cols` / `_pywcsk_cols` and four tests: `test_oracle_combined_l_w`, `test_oracle_combined_l_c`, `test_oracle_combined_w_c`, `test_oracle_combined_l_w_c`
- [x] T007 Run full test suite (`pytest`) and all pre-commit hooks (`pre-commit run --all-files`); confirm both pass clean; verify no test references `exit_code == 2` for multi-flag input and no source references `UsageError` or `only one counting flag`
