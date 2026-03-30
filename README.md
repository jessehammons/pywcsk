# pywcsk

Python implementation of the Unix `wc` command, built incrementally using
[GitHub Spec Kit](https://github.com/behrangsa/spec-kit) (spec-driven development).

## Feature Dev Workflow
Basic feature workflow
# make feature branch
`git checkout -b 009-default-combined-output`

# run pre-commit checks until everything clears green
# this can sometimes be substantial and require AI dev steps
`venv/bin/pre-commit run --all-files`

#run all tests
`venv/bin/pytest --verbose --cov=pywcsk`

# do manual testing / smoke tests
`printf "one\ntwo\t\r\t\nthree\tfour\nfive\n" | ./venv/bin/pywcsk -c -w -l`

# push branch to GitHub
`git push -u origin 008-combined-flags-lwc`

# now make Pull Request on GitHub and merge
# now on main  branch, /speckit.analyze and market feature as Merged on main branch

## Development Workflow

This project uses Spec Kit for spec-driven development. Spec files live in
`specs/`. The workflow has two kinds of gates: **automated** (pre-commit)
and **manual** (Claude Code slash commands).

### Automated gates (run on every commit)

Pre-commit enforces these mechanically — commits are blocked if they fail:

| Hook | What it checks |
|------|---------------|
| `check-toml` | TOML syntax |
| `check-yaml` | YAML syntax |
| `trailing-whitespace` | No trailing whitespace |
| `end-of-file-fixer` | Files end with a newline |
| `black` | Formatting |
| `flake8` | Style, linting, and complexity |
| `bandit` | Security scan |
| `mypy --strict` | Type correctness of all Python source |

Run all hooks manually at any time:

```bash
venv/bin/pre-commit run --all-files
```

### Manual Spec Kit gates (run in Claude Code)

These are AI-powered and require an interactive Claude Code session. Run them
at each stage in order — they cannot be automated in pre-commit or CI.

#### Full workflow (per feature)

```
specify → clarify → checklist → plan → tasks → analyze → implement → analyze
```

| Step | Command | When | What it does |
|------|---------|------|-------------|
| 1 | `/speckit.specify` | Starting a new feature | Writes `spec.md` with goal, ACs, and test coverage mapping |
| 2 | `/speckit.clarify` | After `spec.md` is written | Finds ambiguities (≤5 questions) and encodes resolutions back into `spec.md` |
| 3 | `/speckit.checklist` | After clarification | Validates requirements quality: clarity, completeness, testability |
| 4 | `/speckit.plan` | After checklist passes | Writes `plan.md`: architecture, which files change, and how |
| 5 | `/speckit.tasks` | After `plan.md` is written | Breaks `plan.md` into incremental `tasks.md` with explicit done criteria |
| 6 | `/speckit.analyze` | After `tasks.md` exists | Cross-artifact consistency check across `spec.md`, `plan.md`, `tasks.md`; finds gaps and conflicts |
| 7 | `/speckit.implement` | After analysis is clean | Executes tasks one by one; leaves all quality gates green after each task |
| 8 | `/speckit.analyze` | After implementation | Confirms all ACs covered, all tests pass, no dead code remains |

**Rules of thumb:**
- Run `/speckit.clarify` and `/speckit.checklist` while the spec is fresh —
  ambiguities baked into `plan.md` are harder to fix than ambiguities caught in `spec.md`.
- Run `/speckit.analyze` a second time post-merge to produce the final sign-off record.
- If `spec.md` changes significantly mid-implementation, re-run `/speckit.clarify`
  and `/speckit.analyze` before continuing.

### Full command reference

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
