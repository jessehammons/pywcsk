"""Counting core for pywcsk — pure functions on bytes, no I/O."""

from dataclasses import dataclass


@dataclass
class Counts:
    """Holds all count values for a single input.

    Populated fields: lines, words, bytes_count.
    Future fields: chars (-m), max_line_length (-L).
    """

    lines: int = 0
    words: int = 0
    bytes_count: int = 0
    chars: int = 0
    max_line_length: int = 0


def count_lines(data: bytes) -> int:
    """Return the number of newline characters in data."""
    return data.count(b"\n")


def count_words(data: bytes) -> int:
    """Return the number of whitespace-delimited tokens in data."""
    return len(data.split())


def count_bytes(data: bytes) -> int:
    """Return the number of bytes in data."""
    return len(data)


def analyze(data: bytes) -> Counts:
    """Return a Counts populated from raw file bytes."""
    return Counts(
        lines=count_lines(data),
        words=count_words(data),
        bytes_count=count_bytes(data),
    )
