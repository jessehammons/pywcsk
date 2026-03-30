"""Unit tests for pywcsk.cli._format_counts — formatter layer, no I/O."""

from pywcsk.cli import _format_counts
from pywcsk.counter import Counts


SAMPLE = Counts(lines=1, words=2, bytes_count=12)


class TestFormatCounts:
    """Tests for _format_counts() — pure formatter, no Click."""

    def test_show_lines_only(self) -> None:
        """Single -l flag: only lines column emitted."""
        assert (
            _format_counts(SAMPLE, show_lines=True, show_words=False, show_bytes=False)
            == "      1"
        )

    def test_show_words_only(self) -> None:
        """Single -w flag: only words column emitted."""
        assert (
            _format_counts(SAMPLE, show_lines=False, show_words=True, show_bytes=False)
            == "      2"
        )

    def test_show_bytes_only(self) -> None:
        """Single -c flag: only bytes column emitted."""
        assert (
            _format_counts(SAMPLE, show_lines=False, show_words=False, show_bytes=True)
            == "     12"
        )

    def test_show_all_flags(self) -> None:
        """All three flags: columns in fixed order lines→words→bytes."""
        assert (
            _format_counts(SAMPLE, show_lines=True, show_words=True, show_bytes=True)
            == "      1       2      12"
        )

    def test_no_flags_default(self) -> None:
        """AC (009): no flags outputs lines, words, and bytes in fixed order."""
        assert (
            _format_counts(SAMPLE, show_lines=False, show_words=False, show_bytes=False)
            == "      1       2      12"
        )

    def test_column_width_seven(self) -> None:
        """Each field is right-aligned in a 7-character field."""
        counts = Counts(lines=3, words=5, bytes_count=24)
        result = _format_counts(
            counts, show_lines=False, show_words=False, show_bytes=False
        )
        # Three 7-char fields joined by single spaces: 3*7 + 2 separators = 23 chars
        assert len(result) == 23
        assert result[7] == " " and result[15] == " "
