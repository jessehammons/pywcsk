# Tasks: Count Lines

## Tasks

- [x] T001 Create `pywcsk/counter.py` with `Counts` dataclass and `count_lines()` + `analyze()`
- [x] T002 Add `[tool.pytest.ini_options]` markers entry for `oracle` to `pyproject.toml`
- [x] T003 Create `tests/fixtures/` with `hello.txt`, `empty.txt`, `multi.txt`, `no_newline.txt`
- [x] T004 Create `tests/test_counter.py` — unit tests for `count_lines()` and `analyze()`
- [x] T005 Update `pywcsk/cli.py` to call `analyze()` and print line counts
- [x] T006 Create `tests/test_count_lines.py` — CLI integration tests via `CliRunner`
- [x] T007 Create `tests/test_oracle.py` — oracle tests comparing against `wc -l`
