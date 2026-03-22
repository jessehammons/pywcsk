# Spec: CLI Skeleton

**Branch**: 001-cli-skeleton
**Status**: Merged

## Goal

Establish the pywcsk CLI entry point using Click. The command accepts an
optional list of file arguments and exposes `--version` and `--help`.

## Acceptance Criteria

| ID | Given | When | Then |
|----|-------|------|------|
| AC1 | any environment | `pywcsk --version` | prints version string, exits 0 |
| AC2 | any environment | `pywcsk --help` | prints usage information, exits 0 |
| AC3 | no arguments | `pywcsk` | reads stdin, exits 0, no output |
| AC4 | two file arguments | `pywcsk file1 file2` | accepted without error |

## Test Coverage Mapping

| AC | Unit test | Integration test | Oracle test |
|----|-----------|-----------------|-------------|
| AC1 | — | `test_version_flag` | — |
| AC2 | — | `test_help_flag` | — |
| AC3 | — | `test_no_args_exits_zero` | — |
| AC4 | — | `test_no_args_exits_zero` | — |
