# Plan: CLI Skeleton

**Branch**: 001-cli-skeleton

## Approach

- Change `cli.py` from `@click.group()` to `@click.command()`
- Add `@click.version_option` using `__version__` from `pywcsk/__init__.py`
- Add `@click.argument("files", nargs=-1)` as a stub for future file processing
- Tests via Click's `CliRunner` in `tests/test_cli.py`

## Files Changed

- `pywcsk/cli.py` — refactored entry point
- `tests/test_cli.py` — new integration test file
