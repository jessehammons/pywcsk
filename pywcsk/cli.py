"""CLI for pywcsk."""

import click

from . import __version__
from .counter import analyze, Counts


def _format_counts(
    counts: Counts, show_lines: bool, show_words: bool, show_bytes: bool
) -> str:
    """Return space-joined column string for the selected counts in fixed order."""
    parts = []
    if show_lines:
        parts.append(f"{counts.lines:>7}")
    if show_words:
        parts.append(f"{counts.words:>7}")
    if show_bytes:
        parts.append(f"{counts.bytes_count:>7}")
    if not parts:
        parts.append(f"{counts.lines:>7}")
    return " ".join(parts)


@click.command()
@click.version_option(version=__version__, prog_name="pywcsk")
@click.option("-l", "show_lines", is_flag=True, help="Count lines.")
@click.option("-w", "show_words", is_flag=True, help="Count words.")
@click.option("-c", "show_bytes", is_flag=True, help="Count bytes.")
@click.argument("files", nargs=-1)
def main(
    files: tuple[str, ...], show_lines: bool, show_words: bool, show_bytes: bool
) -> None:
    """Count lines, words, and bytes — a Python implementation of wc."""
    if not files:
        data = click.get_binary_stream("stdin").read()
        counts = analyze(data)
        click.echo(_format_counts(counts, show_lines, show_words, show_bytes))
    else:
        for filename in files:
            with open(filename, "rb") as f:
                data = f.read()
            counts = analyze(data)
            click.echo(
                _format_counts(counts, show_lines, show_words, show_bytes)
                + f" {filename}"
            )


if __name__ == "__main__":
    main()
