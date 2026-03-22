"""CLI integration tests for mixed whitespace word splitting — spec 005 AC1–AC6."""

from click.testing import CliRunner

from pywcsk.cli import main


class TestMixedWhitespaceCLI:
    """Integration tests for -w with mixed whitespace inputs."""

    def test_tabs_spaces_newlines(self) -> None:
        """AC1: tabs, spaces, and newlines mixed as delimiters."""
        result = CliRunner().invoke(main, ["-w"], input=b"one\t two  \nthree\t\tfour\n")
        assert result.exit_code == 0
        assert result.output == "      4\n"

    def test_mixed_whitespace_only(self) -> None:
        """AC2: input containing only mixed whitespace has 0 words."""
        result = CliRunner().invoke(main, ["-w"], input=b"  \t  \n  \t  \n")
        assert result.exit_code == 0
        assert result.output == "      0\n"

    def test_tab_space_around_newline(self) -> None:
        """AC3: tab+space before and after newlines."""
        result = CliRunner().invoke(main, ["-w"], input=b"one \t\n two\t \nthree\n")
        assert result.exit_code == 0
        assert result.output == "      3\n"

    def test_leading_tabs_and_newlines(self) -> None:
        """AC4: leading tabs and newlines before first word."""
        result = CliRunner().invoke(main, ["-w"], input=b"\t\none\t\ntwo \n")
        assert result.exit_code == 0
        assert result.output == "      2\n"

    def test_blank_line_between_words(self) -> None:
        """AC5: blank line (double newline) between words."""
        result = CliRunner().invoke(main, ["-w"], input=b"a  b\t\tc\n\nd\n")
        assert result.exit_code == 0
        assert result.output == "      4\n"

    def test_crlf_line_endings(self) -> None:
        """AC6: CRLF line endings treated as whitespace."""
        result = CliRunner().invoke(main, ["-w"], input=b"one\r\ntwo\r\n")
        assert result.exit_code == 0
        assert result.output == "      2\n"
