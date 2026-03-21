"""CLI integration tests for -l flag — spec AC1–AC8."""

from pathlib import Path

from click.testing import CliRunner

from pywcsk.cli import main

FIXTURES = Path(__file__).parent / "fixtures"


class TestFlagLFiles:
    """File argument tests — spec AC1–AC4."""

    def test_hello_file(self) -> None:
        """AC1: single-line file."""
        path = str(FIXTURES / "hello.txt")
        result = CliRunner().invoke(main, ["-l", path])
        assert result.exit_code == 0
        count, filename = result.output.split()
        assert int(count) == 1
        assert filename == path

    def test_empty_file(self) -> None:
        """AC2: empty file reports 0."""
        path = str(FIXTURES / "empty.txt")
        result = CliRunner().invoke(main, ["-l", path])
        assert result.exit_code == 0
        count, filename = result.output.split()
        assert int(count) == 0
        assert filename == path

    def test_multi_file(self) -> None:
        """AC3: three-line file."""
        path = str(FIXTURES / "multi.txt")
        result = CliRunner().invoke(main, ["-l", path])
        assert result.exit_code == 0
        count, filename = result.output.split()
        assert int(count) == 3
        assert filename == path

    def test_no_newline_file(self) -> None:
        """AC4: file with no trailing newline has 0 lines."""
        path = str(FIXTURES / "no_newline.txt")
        result = CliRunner().invoke(main, ["-l", path])
        assert result.exit_code == 0
        assert result.output.startswith("      0 ")


class TestFlagLStdin:
    """Stdin tests — spec AC5–AC6."""

    def test_stdin_one_line(self) -> None:
        """AC5: one line on stdin."""
        result = CliRunner().invoke(main, ["-l"], input=b"hello world\n")
        assert result.exit_code == 0
        assert result.output == "      1\n"

    def test_stdin_empty(self) -> None:
        """AC6: empty stdin outputs 0."""
        result = CliRunner().invoke(main, ["-l"], input=b"")
        assert result.exit_code == 0
        assert result.output == "      0\n"


class TestFlagLRegressions:
    """Regression guards — spec AC7–AC8."""

    def test_flag_w_unaffected(self) -> None:
        """AC7: -w still outputs word count, not line count."""
        result = CliRunner().invoke(main, ["-w"], input=b"hello world\n")
        assert result.exit_code == 0
        assert result.output == "      2\n"

    def test_no_flag_default_unchanged(self) -> None:
        """AC8: no flags still outputs line count (feature 002 contract)."""
        path = str(FIXTURES / "multi.txt")
        result = CliRunner().invoke(main, [path])
        assert result.exit_code == 0
        count, _ = result.output.split()
        assert int(count) == 3
