"""Unit tests for pywcsk.counter — pure function tests, no I/O."""

import pytest

from pywcsk.counter import analyze, count_lines, Counts


class TestCountLines:
    """Tests for count_lines() — spec AC1–AC4."""

    def test_empty(self) -> None:
        """AC2: empty input has 0 lines."""
        assert count_lines(b"") == 0

    def test_hello(self) -> None:
        """AC1: single line with trailing newline."""
        assert count_lines(b"hello\n") == 1

    def test_multi(self) -> None:
        """AC3: three lines."""
        assert count_lines(b"one two\nthree four\nfive\n") == 3

    def test_no_trailing_newline(self) -> None:
        """AC4: no trailing newline means 0 lines counted."""
        assert count_lines(b"hello") == 0

    def test_blank_lines(self) -> None:
        """Blank lines each count as a line."""
        assert count_lines(b"\n\n\n") == 3

    def test_whitespace_only_line(self) -> None:
        """A line of spaces terminated by newline counts as one line."""
        assert count_lines(b"   \n") == 1

    @pytest.mark.parametrize(
        "data,expected",
        [
            (b"a\n", 1),
            (b"a\nb\n", 2),
            (b"a\nb\nc\n", 3),
        ],
    )
    def test_parametrized(self, data: bytes, expected: int) -> None:
        """Line count equals number of newline characters."""
        assert count_lines(data) == expected


class TestAnalyze:
    """Tests for analyze() — verifies Counts dataclass population."""

    def test_lines_populated(self) -> None:
        """analyze() sets lines field correctly."""
        assert analyze(b"hello\n").lines == 1

    def test_other_fields_zero(self) -> None:
        """Fields not yet implemented default to 0."""
        counts = analyze(b"hello\n")
        assert counts.words == 0
        assert counts.bytes_count == 0
        assert counts.chars == 0
        assert counts.max_line_length == 0

    def test_returns_counts_instance(self) -> None:
        """analyze() returns a Counts dataclass."""
        assert isinstance(analyze(b""), Counts)
