"""CLI for pywcsk."""

import click

from . import __version__
from .counter import analyze


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
    if sum([show_lines, show_words, show_bytes]) > 1:
        raise click.UsageError(
            "only one counting flag (-l, -w, -c) may be used at a time"
        )
    if not files:
        data = click.get_binary_stream("stdin").read()
        counts = analyze(data)
        if show_bytes:
            value = counts.bytes_count
        elif show_words:
            value = counts.words
        else:
            value = counts.lines
        click.echo(f"{value:>7}")
    else:
        for filename in files:
            with open(filename, "rb") as f:
                data = f.read()
            counts = analyze(data)
            if show_bytes:
                value = counts.bytes_count
            elif show_words:
                value = counts.words
            else:
                value = counts.lines
            click.echo(f"{value:>7} {filename}")


if __name__ == "__main__":
    main()
