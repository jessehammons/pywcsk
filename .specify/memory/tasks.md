# Tasks: pywcsk

**Spec**: `.specify/memory/spec.md` | **Plan**: `.specify/memory/plan.md`

Each task leaves all quality gates green: `pre-commit run --all-files && pytest --verbose --cov=pywcsk`

---

## Phase 1: Spec Kit Setup

- [ ] T001 Write `.specify/memory/` spec files and verify with `specify analyze`; manual man-page cross-check; spot-check spec acceptance criteria against live `wc` output

---

## Phase 2: CLI Skeleton (Shared Infrastructure)

- [ ] T002 [US1] Refactor `cli.py` from `@click.group()` to `@click.command()`; add stub `files` argument (`nargs=-1`); create `tests/test_cli.py` with `test_version_flag`, `test_help_flag`, `test_no_args_exits_zero`

---

## Phase 3: Counting Core (Foundational — blocks all user stories)

**⚠️ CRITICAL**: No CLI behavior can be implemented until `Counts` and `analyze()` are complete.

- [ ] T003 [US1] Create `pywcsk/counter.py` with `Counts` dataclass (all 5 fields, default 0) + `analyze()` populating `lines` only via `_count_lines`; create `tests/test_counter.py`
- [ ] T004 [US1] Extend `analyze()` to populate `words` via `_count_words`; extend `test_counter.py`
- [ ] T005 [US1] Extend `analyze()` to populate `bytes_count` via `_count_bytes`; extend `test_counter.py`; **create `tests/test_oracle.py`** with semantic oracle cases for default counts
- [ ] T006 [US4,US5] Extend `analyze()` to populate `chars` and `max_line_length`; extend `test_counter.py` with UTF-8 tests; extend oracle tests with semantic `-m` and `-L` cases

**Checkpoint**: `analyze()` is fully populated — all five fields correct for any `bytes` input.

---

## Phase 4: Formatter (Foundational — blocks output)

- [ ] T007 [US1] Create `pywcsk/formatter.py` with `format_row`, `compute_col_width`, `make_total`; imports `Counts` from `counter`; create `tests/test_formatter.py`

**Checkpoint**: Formatter produces correct column-ordered output strings from `Counts` objects.

---

## Phase 5: User Story 1 — Default Count (P1) 🎯 MVP

**Goal**: `pywcsk file` and `pywcsk` (stdin) produce correct default output.

**Independent Test**: `pywcsk tests/fixtures/hello.txt` → `      1       1       6 tests/fixtures/hello.txt`

- [ ] T008 [US1] Wire counter + formatter into CLI for default mode (lines+words+bytes); create `tests/fixtures/` (empty.txt, hello.txt, multi.txt), `tests/golden/*.default.expected`, and `tests/test_golden.py`

**Checkpoint**: User Story 1 (FR-001) fully functional. Oracle string comparison available from next task.

---

## Phase 6: User Story 2 — Flag Selection (P2)

**Goal**: `-l`, `-w`, `-c` each restrict output to a single column; combinations work; order is invariant.

**Independent Test**: `pywcsk -l hello.txt` → `      1 hello.txt`

- [ ] T009 [US2] Add `-l`, `-w`, `-c` click options; implement flag-selection logic; golden files for `hello.{l,w,c,lw,lwc}.expected`; **convert oracle cases to string comparison** (CLI now exists)

**Checkpoint**: User Story 2 (FR-002, FR-003, FR-004, FR-007) fully functional.

---

## Phase 7: Flag Precedence Logic

**Goal**: `_resolve_bytes_chars` correctly determines byte/char mode from raw argv.

- [ ] T010 [US4] Implement `_resolve_bytes_chars(argv)` in `cli.py`; create `tests/test_flag_precedence.py` with exhaustive cases (no flags, `-c`, `-m`, `-cm`, `-mc`, `-c -m`, `-m -c`, interleaved with other flags, repeated flags)

**Checkpoint**: Precedence logic verified in isolation before wiring to CLI.

---

## Phase 8: User Story 4 — Character Count (P3)

**Goal**: `-m` counts Unicode code points; last of `-c`/`-m` wins.

**Independent Test**: `pywcsk -m cafe.txt` on UTF-8 `"café\n"` → `      5 cafe.txt`

- [ ] T011 [US4] Wire `-m` into CLI using `_resolve_bytes_chars`; create `tests/fixtures/cafe.txt`; golden files `cafe.{m,c,cm,mc}.expected`; oracle tests for `-m` on ASCII fixtures

**Checkpoint**: User Story 4 (FR-005, FR-008) fully functional.

---

## Phase 9: User Story 5 — Longest Line (P3)

**Goal**: `-L` reports max line length; `-L` total is max not sum.

**Independent Test**: `pywcsk -L lines.txt` → `     25 lines.txt`

- [ ] T012 [US5] Add `-L` option; create `tests/fixtures/lines.txt`; golden files `lines.{L,lL}.expected`; **convert oracle `-L` cases to string comparison**; tab-expansion cases remain `xfail`

**Checkpoint**: User Story 5 partial (FR-006) functional for single file.

---

## Phase 10: User Story 3 — Multiple Files (P2)

**Goal**: Multiple files produce per-file rows plus a `total` row; `-L` total is max.

**Independent Test**: `pywcsk hello.txt small.txt` → 3 rows including `total`

- [ ] T013 [US3] Add total row when >1 file processed; create `tests/fixtures/small.txt`; golden file `hello_and_small.default.expected`; oracle string-comparison multi-file case
- [ ] T014 [US3,US5] Verify `-L` total is max not sum (explicit test coverage); create `tests/fixtures/short_lines.txt`, `long_lines.txt`; golden file `short_and_long_lines.L.expected`

**Checkpoint**: User Story 3 (FR-009, FR-010) and User Story 5 fully functional.

---

## Phase 11: User Story 6 — Error Handling (P2)

**Goal**: Errors go to stderr; processing continues; exit code is 1 on any error.

**Independent Test**: `pywcsk hello.txt missing.txt small.txt` counts valid files, errors to stderr, exits 1.

- [ ] T015 [US6] Handle `OSError`, `IsADirectoryError`, all-files-fail; total row reflects only successful files; tests: `test_all_missing_files_exit_1`, `test_two_valid_one_missing_shows_total`, `test_directory_as_argument`

**Checkpoint**: User Story 6 (FR-012) fully functional.

---

## Phase 12: Column Width Scaling

**Goal**: Column width determined by the largest count across all files; all rows use the same width.

- [ ] T016 Refactor CLI loop to two-pass (count all → format all); tests for wide-column consistency across files in same invocation

**Checkpoint**: FR-011 (column width scaling) fully functional.

---

## Phase 13: User Story 7 — Stdin via `-` (P3)

**Goal**: `-` as filename reads from stdin; that row shows no filename.

**Independent Test**: `echo "hello\n" | pywcsk -` → `      1       1       6`

- [ ] T017 [US7] Handle `-` in file loop; golden file `dash_stdin.default.expected`; tests: `test_dash_reads_stdin`, `test_dash_and_file`, `test_dash_in_middle`

**Checkpoint**: User Story 7 (FR-013) fully functional.

---

## Phase 14: Polish & Documentation

- [ ] T018 Fill in `README.md`: synopsis, installation, usage examples, flags table, known deviations from BSD `wc`; `pre-commit run --all-files` must pass on new content

---

## Dependencies & Execution Order

- **T001**: No dependencies — start here
- **T002**: No dependencies — can start after T001
- **T003–T006**: Sequential (each extends `analyze()`)
- **T007**: Depends on T006 (`Counts` must be complete)
- **T008**: Depends on T007 (formatter must exist)
- **T009–T017**: Each depends on T008 (CLI must exist); otherwise sequential
- **T018**: Depends on all prior tasks

## Parallel Opportunities

- T002 and T003 can run in parallel (different files)
- T010 (flag precedence) has no CLI dependency and can be done any time after T002
