"""CLI integration tests for single-flag regression guards — spec 006/008."""

from click.testing import CliRunner

from pywcsk.cli import main

HELLO = b"hello world\n"


class TestFlagValidation:
    """Regression guards: single-flag and no-flag paths are unaffected by combined-flag support (spec 008)."""

    # ------------------------------------------------------------------
    # Regression guards — single flag and no-flag paths unchanged
    # ------------------------------------------------------------------

    def test_no_flag_unchanged(self) -> None:
        """AC1: no flags outputs lines, words, and bytes, exits 0."""
        result = CliRunner().invoke(main, [], input=HELLO)
        assert result.exit_code == 0
        assert result.stdout == "      1       2      12\n"

    def test_flag_l_unchanged(self) -> None:
        """AC2: -l alone still outputs line count, exits 0."""
        result = CliRunner().invoke(main, ["-l"], input=HELLO)
        assert result.exit_code == 0
        assert result.stdout == "      1\n"

    def test_flag_w_unchanged(self) -> None:
        """AC3: -w alone still outputs word count, exits 0."""
        result = CliRunner().invoke(main, ["-w"], input=HELLO)
        assert result.exit_code == 0
        assert result.stdout == "      2\n"
