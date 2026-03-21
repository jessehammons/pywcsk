"""Unit tests for pywcsk.counter — pure function tests, no I/O."""

import pytest

from pywcsk.counter import analyze, count_lines, count_words, Counts


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

    def test_words_populated(self) -> None:
        """analyze() sets words field correctly."""
        assert analyze(b"hello world\n").words == 2

    def test_unimplemented_fields_zero(self) -> None:
        """Fields not yet implemented default to 0."""
        counts = analyze(b"hello\n")
        assert counts.bytes_count == 0
        assert counts.chars == 0
        assert counts.max_line_length == 0

    def test_returns_counts_instance(self) -> None:
        """analyze() returns a Counts dataclass."""
        assert isinstance(analyze(b""), Counts)


class TestCountWords:
    """Tests for count_words() — spec AC1–AC9."""

    def test_empty(self) -> None:
        """AC2/AC9: empty input has 0 words."""
        assert count_words(b"") == 0

    def test_single_word(self) -> None:
        """AC1: single word with trailing newline."""
        assert count_words(b"hello\n") == 1

    def test_multi_word_single_line(self) -> None:
        """Two words on one line."""
        assert count_words(b"hello world\n") == 2

    def test_multi_line(self) -> None:
        """AC3/AC8: words spread across multiple lines."""
        assert count_words(b"one two\nthree four\nfive\n") == 5

    def test_multiple_spaces(self) -> None:
        """AC4: multiple spaces between words count as one delimiter."""
        assert count_words(b"  hello   world  \n") == 2

    def test_tab_separator(self) -> None:
        """AC5: tab is whitespace."""
        assert count_words(b"hello\tworld\n") == 2

    def test_whitespace_only(self) -> None:
        """AC6: only whitespace → 0 words."""
        assert count_words(b"   \n") == 0

    def test_no_trailing_newline(self) -> None:
        """AC7: word at EOF without newline still counts."""
        assert count_words(b"hello") == 1

    def test_mixed_whitespace(self) -> None:
        """Tabs, spaces, and newlines are all delimiters."""
        assert count_words(b"a\t b \n c\n") == 3

    @pytest.mark.parametrize(
        "data,expected",
        [
            (b"a\n", 1),
            (b"a b\n", 2),
            (b"a b c\n", 3),
        ],
    )
    def test_parametrized(self, data: bytes, expected: int) -> None:
        """Word count equals number of whitespace-delimited tokens."""
        assert count_words(data) == expected
