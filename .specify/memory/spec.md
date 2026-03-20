# Feature Specification: pywcsk — Python wc using Spec Kit

**Created**: 2026-03-19
**Status**: Active
**Reference**: BSD `wc(1)` man page (macOS 14.7, April 11, 2020)
**Synopsis**: `pywcsk [--version] [-Lclmw] [file ...]`

---

## User Scenarios & Testing

### User Story 1 — Count lines, words, and bytes in a file (Priority: P1)

A developer wants to count lines, words, and bytes in one or more text files, just like the Unix `wc` command.

**Why this priority**: This is the core behavior. Everything else builds on it. Delivers immediate value.

**Independent Test**: `pywcsk tests/fixtures/hello.txt` produces `      1       1       6 tests/fixtures/hello.txt`

**Acceptance Scenarios**:

1. **Given** `hello.txt` containing `"hello\n"` (1 line, 1 word, 6 bytes), **When** `pywcsk hello.txt` is run with no flags, **Then** stdout is `      1       1       6 hello.txt\n` and exit code is 0
2. **Given** an empty file `empty.txt` (0 bytes), **When** `pywcsk empty.txt` is run, **Then** stdout is `      0       0       0 empty.txt\n`
3. **Given** `multi.txt` containing `"one two\nthree four\nfive\n"` (3 lines, 5 words, 24 bytes), **When** `pywcsk multi.txt`, **Then** stdout is `      3       5      24 multi.txt\n`
4. **Given** no file arguments and `"hello world\n"` on stdin, **When** `pywcsk` is run, **Then** stdout is `      1       2      12\n` (no filename field for stdin)
5. **Given** empty stdin, **When** `pywcsk` is run, **Then** stdout is `      0       0       0\n`
6. **Given** a file where the last line has no trailing newline (e.g. `"hello"`), **When** `pywcsk file.txt`, **Then** line count is `0` (lines = number of `\n` characters)

---

### User Story 2 — Select specific count columns with flags (Priority: P2)

A developer wants to see only specific counts rather than all three defaults.

**Why this priority**: Flag-filtered output is essential for scripting (e.g., `pywcsk -l file | xargs`).

**Independent Test**: `pywcsk -l hello.txt` produces `      1 hello.txt`

**Acceptance Scenarios**:

1. **Given** `hello.txt`, **When** `pywcsk -l hello.txt`, **Then** stdout is `      1 hello.txt\n`
2. **Given** `hello.txt`, **When** `pywcsk -w hello.txt`, **Then** stdout is `      1 hello.txt\n`
3. **Given** `hello.txt` (6 bytes), **When** `pywcsk -c hello.txt`, **Then** stdout is `      6 hello.txt\n`
4. **Given** `hello.txt`, **When** `pywcsk -lw hello.txt` OR `pywcsk -wl hello.txt`, **Then** stdout is `      1       1 hello.txt\n` (lines always before words regardless of flag order)
5. **Given** `hello.txt`, **When** `pywcsk -lwc hello.txt`, **Then** stdout is `      1       1       6 hello.txt\n`
6. **Given** a file, **When** any combination of `-l`, `-w`, `-c` is given, **Then** columns always appear in the order: lines, words, bytes — never reordered

---

### User Story 3 — Process multiple files with totals (Priority: P2)

A developer wants to count across multiple files and see a summary total.

**Why this priority**: Multi-file processing is a very common use case in shell pipelines.

**Independent Test**: `pywcsk hello.txt small.txt` produces three lines: one per file plus a `total` line.

**Acceptance Scenarios**:

1. **Given** `hello.txt` (1/1/6) and `small.txt` (1/1/3), **When** `pywcsk hello.txt small.txt`, **Then** stdout is:
   ```
         1       1       6 hello.txt
         1       1       3 small.txt
         2       2       9 total
   ```
2. **Given** only one file, **When** `pywcsk hello.txt`, **Then** no `total` line is printed
3. **Given** two files and `-l`, **When** `pywcsk -l hello.txt small.txt`, **Then** total row sums the line counts

---

### User Story 4 — Count Unicode characters with `-m` (Priority: P3)

A developer working with multibyte text wants to count Unicode code points rather than bytes.

**Why this priority**: Important for internationalised text processing.

**Independent Test**: `pywcsk -m cafe.txt` on a UTF-8 file with `"café\n"` produces `      5 cafe.txt`

**Acceptance Scenarios**:

1. **Given** `cafe.txt` containing UTF-8 `"café\n"` (6 bytes, 5 chars), **When** `pywcsk -m cafe.txt`, **Then** stdout is `      5 cafe.txt\n`
2. **Given** `cafe.txt`, **When** `pywcsk -c cafe.txt`, **Then** stdout is `      6 cafe.txt\n` (bytes, not chars)
3. **Given** `-m` then `-c` on the command line, **When** `pywcsk -m -c cafe.txt`, **Then** `-c` wins (last flag): stdout is `      6 cafe.txt\n`
4. **Given** `-c` then `-m` on the command line, **When** `pywcsk -c -m cafe.txt`, **Then** `-m` wins (last flag): stdout is `      5 cafe.txt\n`
5. **Given** combined short flags, **When** `pywcsk -mc cafe.txt`, **Then** `-c` wins (rightmost in the combined string): stdout is `      6 cafe.txt\n`
6. **Given** combined short flags, **When** `pywcsk -cm cafe.txt`, **Then** `-m` wins: stdout is `      5 cafe.txt\n`
7. **Given** an ASCII-only file, **When** `pywcsk -m file.txt`, **Then** char count equals byte count

---

### User Story 5 — Find the longest line with `-L` (Priority: P3)

A developer wants to find the length of the longest line in one or more files.

**Why this priority**: Useful utility flag; supported by both BSD and GNU `wc`.

**Independent Test**: `pywcsk -L lines.txt` on a file whose longest line is 25 chars produces `     25 lines.txt`

**Acceptance Scenarios**:

1. **Given** `lines.txt` with longest line of 25 chars (no tabs), **When** `pywcsk -L lines.txt`, **Then** stdout is `     25 lines.txt\n`
2. **Given** `empty.txt`, **When** `pywcsk -L empty.txt`, **Then** stdout is `      0 empty.txt\n`
3. **Given** `-l` and `-L` both specified, **When** `pywcsk -lL lines.txt`, **Then** stdout shows lines then max_line_length: `      N      25 lines.txt\n`
4. **Given** `short_lines.txt` (max=5) and `long_lines.txt` (max=20), **When** `pywcsk -L short_lines.txt long_lines.txt`, **Then** total row is `     20 total\n` (max across files, not sum)
5. **Given** a file containing tab characters, **When** `pywcsk -L tab_file.txt`, **Then** each tab counts as 1 character (pywcsk deviation from BSD tabstop-8; see constitution)

---

### User Story 6 — Graceful error handling (Priority: P2)

A developer accidentally passes a nonexistent or unreadable file; `pywcsk` reports the error and continues.

**Why this priority**: Robustness is required for a Unix utility used in pipelines.

**Independent Test**: `pywcsk hello.txt missing.txt small.txt` counts both valid files, errors to stderr for the missing one, exits 1.

**Acceptance Scenarios**:

1. **Given** a nonexistent file, **When** `pywcsk missing.txt`, **Then** stderr contains `pywcsk: missing.txt: No such file or directory` and exit code is 1
2. **Given** one valid and one missing file, **When** `pywcsk hello.txt missing.txt`, **Then** `hello.txt` is counted and printed, error on stderr, exit code is 1
3. **Given** two valid and one missing, **When** `pywcsk hello.txt missing.txt small.txt`, **Then** both valid files counted, total row reflects only the two successful files, exit code is 1
4. **Given** all files missing, **When** `pywcsk missing1.txt missing2.txt`, **Then** no count rows printed, no total row, exit code is 1
5. **Given** a directory path as argument, **When** `pywcsk somedir/`, **Then** stderr contains an error message, exit code is 1

---

### User Story 7 — Read from stdin using `-` as filename (Priority: P3)

A developer wants to mix stdin with file arguments using the conventional `-` placeholder.

**Why this priority**: Standard Unix convention; enables use in complex pipelines.

**Independent Test**: `echo "hello\n" | pywcsk -` produces `      1       1       6`

**Acceptance Scenarios**:

1. **Given** `"hello\n"` on stdin, **When** `pywcsk -` is run, **Then** stdout is `      1       1       6\n` (no filename field; stdin rows never show a filename)
2. **Given** stdin and one file, **When** `echo "hi\n" | pywcsk - hello.txt`, **Then** two count rows plus a total row are printed
3. **Given** `-` between two files, **When** `pywcsk file1.txt - file2.txt`, **Then** output rows appear in that order (file1, stdin, file2, total)

---

### Edge Cases

- File with no trailing newline (e.g. `"hello"`): line count is 0 (lines = count of `\n` chars)
- Line of only whitespace: counts as 0 words
- Very large files: column width scales to accommodate the digit count (minimum 7 chars wide)
- `-c` and `-m` in the same invocation: rightmost flag wins
- `-L` with multiple files: total reports the maximum, not the sum
- Empty stdin: all counts are 0, no filename shown

---

## Requirements

### Functional Requirements

- **FR-001**: `pywcsk` MUST count lines, words, and bytes by default (no flags specified)
- **FR-002**: `pywcsk -l` MUST report only line count
- **FR-003**: `pywcsk -w` MUST report only word count
- **FR-004**: `pywcsk -c` MUST report only byte count (see FR-008 for mutual exclusion with `-m`)
- **FR-005**: `pywcsk -m` MUST report only character count (locale-aware Unicode code points; see FR-008 for mutual exclusion with `-c`)
- **FR-006**: `pywcsk -L` MUST report the length of the longest line, measured in characters (tab counts as 1; see constitution for known deviation from BSD tabstop-8)
- **FR-007**: Output column order MUST always be: lines, words, bytes/chars, max_line_length, filename — regardless of the order flags appear on the command line
- **FR-008**: `-c` and `-m` are mutually exclusive; the last one specified on the command line wins
- **FR-009**: With multiple input files, MUST print one row per file followed by a `total` row
- **FR-010**: `-L` total across multiple files MUST be the maximum max_line_length, not the sum
- **FR-011**: Column width MUST be at least 7; MUST scale wider if any count value exceeds 7 digits; all rows in a single invocation MUST use the same column width
- **FR-012**: On file open/read error, MUST write a message to stderr, continue processing remaining files, and exit with code > 0
- **FR-013**: `-` as a filename argument MUST read from stdin; that row's output MUST NOT include a filename field
- **FR-014**: `pywcsk --version` MUST print the current version string and exit 0
- **FR-015**: `--libxo` and SIGINFO are explicitly NOT implemented (see constitution)

### Key Entities

- **`Counts`**: Immutable record with fields `lines: int`, `words: int`, `bytes_count: int`, `chars: int`, `max_line_length: int` — all default to 0
- **`analyze(data: bytes) -> Counts`**: The single entry point that produces a fully-populated `Counts` from raw file bytes

---

## Success Criteria

### Measurable Outcomes

- **SC-001**: `pywcsk <file>` output matches `wc <file>` string-for-string on all ASCII fixtures, on both macOS (BSD wc) and ubuntu-latest (GNU wc)
- **SC-002**: `pywcsk -l/-w/-c <file>` output matches `wc -l/-w/-c <file>` string-for-string on ASCII fixtures on both platforms
- **SC-003**: All 18 implementation tasks complete with unit, integration, and golden output tests all green
- **SC-004**: `mypy --strict`, `flake8`, `bandit`, and `pre-commit run --all-files` all pass with zero errors/warnings
- **SC-005**: Oracle tests pass on both macOS and ubuntu-latest; known deviations (tab `-L`, multibyte `-m`) are `xfail` with documented reasons
