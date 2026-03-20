# pywcsk Constitution

## Core Principles

### I. Pure Counting Core (NON-NEGOTIABLE)
`counter.py` is the only module that computes counts. It contains only pure functions on `bytes`; it MUST NOT perform I/O, import Click, or have side effects. Every other module depends on it; it depends on nothing in the project. The `Counts` dataclass lives here and is the single shared data type that crosses all module boundaries.

### II. Pipeline Architecture (NON-NEGOTIABLE)
Data flows in one direction only: `bytes → analyze() → Counts → formatter → str`. The CLI never touches raw integers. The formatter never calls counting functions. Violating this boundary requires a constitution amendment.

### III. Test-First, All Three Layers (NON-NEGOTIABLE)
Every behavior requires tests written and failing **before** implementation:
1. **Unit tests** — pure functions in isolation (`tests/test_counter.py`, `tests/test_formatter.py`, `tests/test_flag_precedence.py`)
2. **Integration tests** — CLI via Click's `CliRunner` (`tests/test_cli.py`)
3. **Golden output tests** — CLI output compared against stored `.expected` files (`tests/test_golden.py`, `tests/fixtures/`, `tests/golden/`)

No task is complete until all three layers pass for that task's behavior. Additionally, oracle tests (`tests/test_oracle.py`) comparing against system `wc` are maintained incrementally from Task 005 onward.

### IV. Output Column Ordering is Invariant (NON-NEGOTIABLE)
Output columns always appear in this fixed order: **lines → words → bytes/chars → max_line_length → filename**. This order never changes regardless of which flags are specified or in what order the user types them. This is a POSIX requirement.

### V. Flag Mutual Exclusion: Last Wins
`-c` (bytes) and `-m` (chars) are mutually exclusive; the **last one on the command line wins**. This matches BSD `wc` behavior. Implementation uses `_resolve_bytes_chars(argv)` to inspect raw argument order before Click's callback machinery runs.

### VI. All Files Counted Before Any Output
All input files must be fully counted before the first output line is printed. This is required for correct column-width computation: every row must use the width needed by the largest count across all files.

## Known Deviations from BSD `wc`

| Behavior | BSD `wc` | pywcsk | Rationale |
|---|---|---|---|
| `-L` tab width | tabstop-8 expansion | 1 character per tab | Avoids locale/terminal complexity |
| `--libxo` | supported | not implemented | FreeBSD-only library |
| SIGINFO | supported | not implemented | BSD-only signal |

Oracle tests for behaviors affected by these deviations are marked `@pytest.mark.xfail(strict=False)` with an explanatory reason string.

## Quality Gates

Every commit must pass:
- `mypy --strict` — zero errors
- `flake8` with all configured plugins — zero violations
- `bandit` — zero findings outside configured skips
- `pre-commit run --all-files` — all hooks green
- `pytest --verbose --cov=pywcsk` — all tests passing

## Out of Scope

- `--libxo` (FreeBSD libxo structured output)
- SIGINFO signal handling (BSD-only)

These will not be implemented regardless of future spec requests without a constitution amendment.

## Governance

This constitution supersedes all other practices. Amendments require: written rationale, update to the relevant task spec, and update to this document's version and date.

**Version**: 1.0.0 | **Ratified**: 2026-03-19 | **Last Amended**: 2026-03-19
