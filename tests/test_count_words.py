"""CLI integration tests for word counting — spec AC1–AC9."""

from pathlib import Path

from click.testing import CliRunner

from pywcsk.cli import main

FIXTURES = Path(__file__).parent / "fixtures"


class TestCountWordsFiles:
    """File argument tests — spec AC1–AC3."""

    def test_hello_file(self) -> None:
        """AC1: single word file."""
        path = str(FIXTURES / "hello.txt")
        result = CliRunner().invoke(main, ["-w", path])
        assert result.exit_code == 0
        count, filename = result.output.split()
        assert int(count) == 1
        assert filename == path

    def test_empty_file(self) -> None:
        """AC2: empty file reports 0."""
        path = str(FIXTURES / "empty.txt")
        result = CliRunner().invoke(main, ["-w", path])
        assert result.exit_code == 0
        count, filename = result.output.split()
        assert int(count) == 0
        assert filename == path

    def test_multi_file(self) -> None:
        """AC3: five-word file."""
        path = str(FIXTURES / "multi.txt")
        result = CliRunner().invoke(main, ["-w", path])
        assert result.exit_code == 0
        count, filename = result.output.split()
        assert int(count) == 5
        assert filename == path

    def test_no_newline_file(self) -> None:
        """AC7 via file: word at EOF without newline still counts."""
        path = str(FIXTURES / "no_newline.txt")
        result = CliRunner().invoke(main, ["-w", path])
        assert result.exit_code == 0
        assert result.output.startswith("      1 ")

    def test_flag_not_set_uses_lines(self) -> None:
        """Without -w, default output (lines, words, bytes) has line count as first column."""
        path = str(FIXTURES / "multi.txt")
        result = CliRunner().invoke(main, [path])
        assert result.exit_code == 0
        tokens = result.output.split()
        assert int(tokens[0]) == 3


class TestCountWordsStdin:
    """Stdin tests — spec AC4–AC9."""

    def test_stdin_multiple_spaces(self) -> None:
        """AC4: multiple spaces between words are one delimiter."""
        result = CliRunner().invoke(main, ["-w"], input=b"  hello   world  \n")
        assert result.exit_code == 0
        assert result.output == "      2\n"

    def test_stdin_tab_separator(self) -> None:
        """AC5: tab is whitespace."""
        result = CliRunner().invoke(main, ["-w"], input=b"hello\tworld\n")
        assert result.exit_code == 0
        assert result.output == "      2\n"

    def test_stdin_whitespace_only(self) -> None:
        """AC6: whitespace-only input is 0 words."""
        result = CliRunner().invoke(main, ["-w"], input=b"   \n")
        assert result.exit_code == 0
        assert result.output == "      0\n"

    def test_stdin_no_trailing_newline(self) -> None:
        """AC7: word at EOF without newline counts."""
        result = CliRunner().invoke(main, ["-w"], input=b"hello")
        assert result.exit_code == 0
        assert result.output == "      1\n"

    def test_stdin_multi_line(self) -> None:
        """AC8: words across lines are counted."""
        result = CliRunner().invoke(main, ["-w"], input=b"hello\nworld\n")
        assert result.exit_code == 0
        assert result.output == "      2\n"

    def test_stdin_empty(self) -> None:
        """AC9: empty stdin outputs 0."""
        result = CliRunner().invoke(main, ["-w"], input=b"")
        assert result.exit_code == 0
        assert result.output == "      0\n"
