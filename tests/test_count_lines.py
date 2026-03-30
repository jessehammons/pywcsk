"""CLI integration tests for line counting — spec AC1–AC6."""

from pathlib import Path

from click.testing import CliRunner

from pywcsk.cli import main

FIXTURES = Path(__file__).parent / "fixtures"


class TestCountLinesFiles:
    """File argument tests — spec AC1–AC4."""

    def test_hello_file(self) -> None:
        """AC1: single line file."""
        path = str(FIXTURES / "hello.txt")
        result = CliRunner().invoke(main, [path])
        assert result.exit_code == 0
        tokens = result.output.split()
        assert int(tokens[0]) == 1
        assert tokens[-1] == path

    def test_empty_file(self) -> None:
        """AC2: empty file reports 0."""
        path = str(FIXTURES / "empty.txt")
        result = CliRunner().invoke(main, [path])
        assert result.exit_code == 0
        tokens = result.output.split()
        assert int(tokens[0]) == 0
        assert tokens[-1] == path

    def test_multi_file(self) -> None:
        """AC3: three-line file."""
        path = str(FIXTURES / "multi.txt")
        result = CliRunner().invoke(main, [path])
        assert result.exit_code == 0
        tokens = result.output.split()
        assert int(tokens[0]) == 3
        assert tokens[-1] == path

    def test_no_newline_file(self) -> None:
        """AC4: file with no trailing newline has 0 lines."""
        result = CliRunner().invoke(main, [str(FIXTURES / "no_newline.txt")])
        assert result.exit_code == 0
        assert result.output.startswith("      0 ")


class TestCountLinesStdin:
    """Stdin tests — spec AC5–AC6."""

    def test_stdin_one_line(self) -> None:
        """AC5: one line on stdin, no filename in output."""
        result = CliRunner().invoke(main, [], input=b"hello world\n")
        assert result.exit_code == 0
        assert int(result.output.split()[0]) == 1

    def test_stdin_empty(self) -> None:
        """AC6: empty stdin outputs 0, no filename."""
        result = CliRunner().invoke(main, [], input=b"")
        assert result.exit_code == 0
        assert int(result.output.split()[0]) == 0

    def test_stdin_multi_line(self) -> None:
        """Multiple lines on stdin are counted correctly."""
        result = CliRunner().invoke(main, [], input=b"a\nb\nc\n")
        assert result.exit_code == 0
        assert int(result.output.split()[0]) == 3
