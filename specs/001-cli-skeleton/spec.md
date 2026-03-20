# Spec: CLI Skeleton

**Branch**: 001-cli-skeleton
**Status**: Complete

## Goal

Establish the pywcsk CLI entry point using Click. The command accepts an
optional list of file arguments and exposes `--version` and `--help`.

## Acceptance Criteria

1. `pywcsk --version` prints the version string and exits 0
2. `pywcsk --help` prints usage information and exits 0
3. `pywcsk` with no arguments exits 0 (reads stdin; no output yet)
4. `pywcsk file1 file2` is accepted without error (files not yet processed)
