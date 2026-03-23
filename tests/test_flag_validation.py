"""CLI integration tests for multiple flag validation — spec 006 AC1–AC7."""

from click.testing import CliRunner
import pytest

from pywcsk.cli import main

HELLO = b"hello world\n"


class TestFlagValidation:
    """Integration tests for counting flag mutual exclusion."""

    # ------------------------------------------------------------------
    # Regression guards — single flag and no-flag paths unchanged (AC1–AC3)
    # ------------------------------------------------------------------

    def test_no_flag_unchanged(self) -> None:
        """AC1: no flags still outputs line count, exits 0."""
        result = CliRunner().invoke(main, [], input=HELLO)
        assert result.exit_code == 0
        assert result.stdout == "      1\n"

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

    # ------------------------------------------------------------------
    # Invalid combinations — must error (AC4–AC6)
    # ------------------------------------------------------------------

    def test_l_and_w_exits_nonzero(self) -> None:
        """AC4: -l -w exits with code 2."""
        result = CliRunner().invoke(main, ["-l", "-w"], input=HELLO)
        assert result.exit_code == 2

    def test_w_and_l_exits_nonzero(self) -> None:
        """AC5: -w -l exits with code 2 — flag order must not matter."""
        result = CliRunner().invoke(main, ["-w", "-l"], input=HELLO)
        assert result.exit_code == 2

    def test_l_and_w_stdin_exits_nonzero(self) -> None:
        """AC6: -l -w with stdin exits with code 2."""
        result = CliRunner().invoke(main, ["-l", "-w"], input=HELLO)
        assert result.exit_code == 2

    # ------------------------------------------------------------------
    # Error message content (AC7)
    # ------------------------------------------------------------------

    def test_error_message_content(self) -> None:
        """AC7: error message is on stderr and contains expected text."""
        result = CliRunner().invoke(main, ["-l", "-w"], input=HELLO)
        assert "only one counting flag" in result.stderr

    # ------------------------------------------------------------------
    # Future-proof: -c combinations
    # Skipped until -c flag is implemented (feature 007)
    # ------------------------------------------------------------------

    @pytest.mark.skip(reason="-c flag not yet implemented (feature 007)")
    def test_l_and_c_exits_nonzero(self) -> None:
        """Future: -l -c should exit with code 2."""
        result = CliRunner().invoke(main, ["-l", "-c"], input=HELLO)
        assert result.exit_code == 2

    @pytest.mark.skip(reason="-c flag not yet implemented (feature 007)")
    def test_w_and_c_exits_nonzero(self) -> None:
        """Future: -w -c should exit with code 2."""
        result = CliRunner().invoke(main, ["-w", "-c"], input=HELLO)
        assert result.exit_code == 2
