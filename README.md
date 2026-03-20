# pywcsk

Python implementation of the Unix `wc` command, built incrementally using
[GitHub Spec Kit](https://github.com/behrangsa/spec-kit) (spec-driven development).

## Development Workflow

This project uses Spec Kit for spec-driven development. Spec files live in
`.specify/memory/`. The workflow has two kinds of gates: **automated** (pre-commit)
and **manual** (Claude Code slash commands).

### Automated gates (run on every commit)

Pre-commit enforces these mechanically — commits are blocked if they fail:

| Hook | What it checks |
|------|---------------|
| `markdownlint` | Markdown structure of spec files |
| `check-spec-integrity` | No placeholder text (`TODO`, `TKTK`, `TBD`, `FIXME`, `???`); no gaps in `FR-NNN` or `T NNN` sequences; no `[USN]` references to undefined user stories |
| `mypy --strict` | Type correctness of all Python source |
| `flake8` | Style and linting |
| `bandit` | Security scan |
| `black` | Formatting |

Run all hooks manually at any time:

```bash
venv/bin/pre-commit run --all-files
```

### Manual Spec Kit gates (run in Claude Code)

These are AI-powered and require an interactive Claude Code session. Run them
at the indicated workflow stage — they cannot be automated in pre-commit or CI.

| Command | When to run | What it does |
|---------|------------|-------------|
| `/speckit.clarify` | After writing or significantly changing `spec.md` | Interactive Q&A (≤5 questions) to resolve ambiguities; encodes answers back into `spec.md` |
| `/speckit.checklist` | After clarification is complete | Validates requirements quality: clarity, completeness, testability ("unit tests for requirements writing") |
| `/speckit.analyze` | After `tasks.md` exists; before starting implementation on a feature | Cross-artifact consistency check across `spec.md`, `plan.md`, and `tasks.md`; finds gaps, conflicts, and coverage holes |
| `/speckit.implement` | When ready to execute a task | Works through `tasks.md` tasks one by one, leaving all quality gates green after each |

**Rule of thumb**: run `/speckit.analyze` before starting any new implementation
task to confirm the spec, plan, and task list are consistent. If spec files change
significantly mid-implementation, re-run `/speckit.clarify` and `/speckit.analyze`.

### Spec Kit command reference (full set)

| Command | Purpose |
|---------|---------|
| `/speckit.specify` | Write `spec.md` for a new feature |
| `/speckit.clarify` | Reduce ambiguity in `spec.md` (interactive) |
| `/speckit.checklist` | Validate requirements quality |
| `/speckit.plan` | Generate `plan.md` (architecture, module design) |
| `/speckit.tasks` | Break `plan.md` into incremental `tasks.md` |
| `/speckit.analyze` | Cross-artifact consistency report |
| `/speckit.implement` | Execute tasks from `tasks.md` |
| `/speckit.taskstoissues` | Convert `tasks.md` to GitHub Issues |
| `/speckit.constitution` | Amend `constitution.md` |

## Setup

```bash
/opt/homebrew/bin/python3 -m venv venv
venv/bin/pip install -e ".[dev]"
venv/bin/pre-commit install
```

## Running tests

```bash
venv/bin/pytest --verbose --cov=pywcsk
```
