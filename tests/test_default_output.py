"""Integration tests for default (no-flag) combined output — spec 009 AC1a–AC1c, AC2, AC5a–AC5c, AC7."""

from pathlib import Path

from click.testing import CliRunner

from pywcsk.cli import main

FIXTURES = Path(__file__).parent / "fixtures"
HELLO_FILE = FIXTURES / "hello.txt"
MULTI_FILE = FIXTURES / "multi.txt"
NO_NEWLINE_FILE = FIXTURES / "no_newline.txt"
EMPTY_FILE = FIXTURES / "empty.txt"
STDIN = b"hello world\n"


class TestDefaultOutput:
    """Integration tests for default no-flag output: lines, words, bytes."""

    # ------------------------------------------------------------------
    # Default file output — AC1a, AC1b, AC1c, AC7
    # ------------------------------------------------------------------

    def test_hello_file(self) -> None:
        """AC1a: no flags on hello.txt outputs lines, words, bytes."""
        result = CliRunner().invoke(main, [str(HELLO_FILE)])
        assert result.exit_code == 0
        assert result.stdout == f"      1       1       6 {HELLO_FILE}\n"

    def test_multi_file(self) -> None:
        """AC1b: no flags on multi.txt outputs lines, words, bytes."""
        result = CliRunner().invoke(main, [str(MULTI_FILE)])
        assert result.exit_code == 0
        assert result.stdout == f"      3       5      24 {MULTI_FILE}\n"

    def test_no_newline_file(self) -> None:
        """AC1c: no flags on no_newline.txt outputs lines, words, bytes."""
        result = CliRunner().invoke(main, [str(NO_NEWLINE_FILE)])
        assert result.exit_code == 0
        assert result.stdout == f"      0       1       5 {NO_NEWLINE_FILE}\n"

    def test_empty_file(self) -> None:
        """AC7: no flags on empty.txt outputs three zero columns."""
        result = CliRunner().invoke(main, [str(EMPTY_FILE)])
        assert result.exit_code == 0
        assert result.stdout == f"      0       0       0 {EMPTY_FILE}\n"

    # ------------------------------------------------------------------
    # Default stdin output — AC2
    # ------------------------------------------------------------------

    def test_stdin(self) -> None:
        """AC2: no flags on stdin outputs lines, words, bytes with no filename."""
        result = CliRunner().invoke(main, [], input=STDIN)
        assert result.exit_code == 0
        assert result.stdout == "      1       2      12\n"

    # ------------------------------------------------------------------
    # Regression guards — single-flag paths unchanged — AC5a, AC5b, AC5c
    # ------------------------------------------------------------------

    def test_flag_l_unchanged(self) -> None:
        """AC5a: -l alone still outputs line count only."""
        result = CliRunner().invoke(main, ["-l", str(HELLO_FILE)])
        assert result.exit_code == 0
        assert result.stdout == f"      1 {HELLO_FILE}\n"

    def test_flag_w_unchanged(self) -> None:
        """AC5b: -w alone still outputs word count only."""
        result = CliRunner().invoke(main, ["-w", str(HELLO_FILE)])
        assert result.exit_code == 0
        assert result.stdout == f"      1 {HELLO_FILE}\n"

    def test_flag_c_unchanged(self) -> None:
        """AC5c: -c alone still outputs byte count only."""
        result = CliRunner().invoke(main, ["-c", str(HELLO_FILE)])
        assert result.exit_code == 0
        assert result.stdout == f"      6 {HELLO_FILE}\n"
