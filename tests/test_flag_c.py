"""CLI integration tests for -c flag (byte counting) — spec 007 AC1–AC7."""

from pathlib import Path

from click.testing import CliRunner

from pywcsk.cli import main

FIXTURES = Path(__file__).parent / "fixtures"


class TestFlagCFiles:
    """File argument tests — spec AC1–AC4."""

    def test_hello_file(self) -> None:
        """AC1: hello.txt is 6 bytes."""
        path = str(FIXTURES / "hello.txt")
        result = CliRunner().invoke(main, ["-c", path])
        assert result.exit_code == 0
        count, filename = result.output.split()
        assert int(count) == 6
        assert filename == path

    def test_empty_file(self) -> None:
        """AC2: empty file reports 0 bytes."""
        path = str(FIXTURES / "empty.txt")
        result = CliRunner().invoke(main, ["-c", path])
        assert result.exit_code == 0
        count, filename = result.output.split()
        assert int(count) == 0
        assert filename == path

    def test_multi_file(self) -> None:
        """AC3: multi.txt is 24 bytes."""
        path = str(FIXTURES / "multi.txt")
        result = CliRunner().invoke(main, ["-c", path])
        assert result.exit_code == 0
        count, filename = result.output.split()
        assert int(count) == 24
        assert filename == path

    def test_no_newline_file(self) -> None:
        """AC4: no_newline.txt is 5 bytes — all bytes counted despite no trailing newline."""
        path = str(FIXTURES / "no_newline.txt")
        result = CliRunner().invoke(main, ["-c", path])
        assert result.exit_code == 0
        assert result.output.startswith("      5 ")


class TestFlagCStdin:
    """Stdin tests — spec AC5–AC6."""

    def test_stdin_bytes(self) -> None:
        """AC5: byte count from stdin, no filename."""
        result = CliRunner().invoke(main, ["-c"], input=b"hello world\n")
        assert result.exit_code == 0
        assert result.output == "     12\n"

    def test_stdin_empty(self) -> None:
        """AC6: empty stdin reports 0."""
        result = CliRunner().invoke(main, ["-c"], input=b"")
        assert result.exit_code == 0
        assert result.output == "      0\n"


class TestFlagCRegressions:
    """Regression guards — existing flags unaffected."""

    def test_no_flag_still_counts_lines(self) -> None:
        """No flags: default output is lines, words, bytes."""
        result = CliRunner().invoke(main, [], input=b"one\ntwo\nthree\n")
        assert result.exit_code == 0
        assert result.output == "      3       3      14\n"

    def test_flag_l_still_counts_lines(self) -> None:
        """-l alone: line count unchanged."""
        result = CliRunner().invoke(main, ["-l"], input=b"one\ntwo\nthree\n")
        assert result.exit_code == 0
        assert result.output == "      3\n"

    def test_flag_w_still_counts_words(self) -> None:
        """-w alone: word count unchanged."""
        result = CliRunner().invoke(main, ["-w"], input=b"one two three\n")
        assert result.exit_code == 0
        assert result.output == "      3\n"
