"""Integration tests for combined counting flags — spec 008 AC1–AC14."""

from pathlib import Path

from click.testing import CliRunner

from pywcsk.cli import main

FIXTURES = Path(__file__).parent / "fixtures"
HELLO_FILE = FIXTURES / "hello.txt"
MULTI_FILE = FIXTURES / "multi.txt"
STDIN = b"hello world\n"


class TestCombinedFlags:
    """Integration tests for multi-flag combined output."""

    # ------------------------------------------------------------------
    # Two-flag file output — AC1–AC4
    # ------------------------------------------------------------------

    def test_l_w_file(self) -> None:
        """AC1: -l -w produces lines then words column."""
        result = CliRunner().invoke(main, ["-l", "-w", str(HELLO_FILE)])
        assert result.exit_code == 0
        assert result.stdout == f"      1       1 {HELLO_FILE}\n"

    def test_w_l_file(self) -> None:
        """AC2: -w -l produces same output as -l -w — flag order does not affect column order."""
        result = CliRunner().invoke(main, ["-w", "-l", str(HELLO_FILE)])
        assert result.exit_code == 0
        assert result.stdout == f"      1       1 {HELLO_FILE}\n"

    def test_l_c_file(self) -> None:
        """AC3: -l -c produces lines then bytes column."""
        result = CliRunner().invoke(main, ["-l", "-c", str(HELLO_FILE)])
        assert result.exit_code == 0
        assert result.stdout == f"      1       6 {HELLO_FILE}\n"

    def test_w_c_file(self) -> None:
        """AC4: -w -c produces words then bytes column."""
        result = CliRunner().invoke(main, ["-w", "-c", str(HELLO_FILE)])
        assert result.exit_code == 0
        assert result.stdout == f"      1       6 {HELLO_FILE}\n"

    # ------------------------------------------------------------------
    # Three-flag file output — AC5–AC7
    # ------------------------------------------------------------------

    def test_l_w_c_file(self) -> None:
        """AC5: -l -w -c produces lines, words, bytes columns."""
        result = CliRunner().invoke(main, ["-l", "-w", "-c", str(HELLO_FILE)])
        assert result.exit_code == 0
        assert result.stdout == f"      1       1       6 {HELLO_FILE}\n"

    def test_c_w_l_file(self) -> None:
        """AC6: -c -w -l produces same output as -l -w -c — flag order does not affect column order."""
        result = CliRunner().invoke(main, ["-c", "-w", "-l", str(HELLO_FILE)])
        assert result.exit_code == 0
        assert result.stdout == f"      1       1       6 {HELLO_FILE}\n"

    def test_multi_file_all_flags(self) -> None:
        """AC7: -l -w -c on multi.txt produces correct three-column output."""
        result = CliRunner().invoke(main, ["-l", "-w", "-c", str(MULTI_FILE)])
        assert result.exit_code == 0
        assert result.stdout == f"      3       5      24 {MULTI_FILE}\n"

    # ------------------------------------------------------------------
    # Stdin combined output — AC8–AC10
    # ------------------------------------------------------------------

    def test_l_w_stdin(self) -> None:
        """AC8: -l -w on stdin produces two-column output with no filename."""
        result = CliRunner().invoke(main, ["-l", "-w"], input=STDIN)
        assert result.exit_code == 0
        assert result.stdout == "      1       2\n"

    def test_l_c_stdin(self) -> None:
        """AC9: -l -c on stdin produces two-column output with no filename."""
        result = CliRunner().invoke(main, ["-l", "-c"], input=STDIN)
        assert result.exit_code == 0
        assert result.stdout == "      1      12\n"

    def test_l_w_c_stdin(self) -> None:
        """AC10: -l -w -c on stdin produces three-column output with no filename."""
        result = CliRunner().invoke(main, ["-l", "-w", "-c"], input=STDIN)
        assert result.exit_code == 0
        assert result.stdout == "      1       2      12\n"

    # ------------------------------------------------------------------
    # Regression guards — single-flag and no-flag paths unchanged — AC11–AC14
    # ------------------------------------------------------------------

    def test_no_flag_unchanged(self) -> None:
        """AC11: no flags still outputs line count only."""
        result = CliRunner().invoke(main, [str(HELLO_FILE)])
        assert result.exit_code == 0
        assert result.stdout == f"      1 {HELLO_FILE}\n"

    def test_flag_l_unchanged(self) -> None:
        """AC12: -l alone still outputs line count only."""
        result = CliRunner().invoke(main, ["-l", str(HELLO_FILE)])
        assert result.exit_code == 0
        assert result.stdout == f"      1 {HELLO_FILE}\n"

    def test_flag_w_unchanged(self) -> None:
        """AC13: -w alone still outputs word count only."""
        result = CliRunner().invoke(main, ["-w", str(HELLO_FILE)])
        assert result.exit_code == 0
        assert result.stdout == f"      1 {HELLO_FILE}\n"

    def test_flag_c_unchanged(self) -> None:
        """AC14: -c alone still outputs byte count only."""
        result = CliRunner().invoke(main, ["-c", str(HELLO_FILE)])
        assert result.exit_code == 0
        assert result.stdout == f"      6 {HELLO_FILE}\n"
