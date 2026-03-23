"""CLI for pywcsk."""

import click

from . import __version__
from .counter import analyze


@click.command()
@click.version_option(version=__version__, prog_name="pywcsk")
@click.option("-l", "show_lines", is_flag=True, help="Count lines.")
@click.option("-w", "show_words", is_flag=True, help="Count words.")
@click.argument("files", nargs=-1)
def main(files: tuple[str, ...], show_lines: bool, show_words: bool) -> None:
    """Count lines, words, and bytes — a Python implementation of wc."""
    if sum([show_lines, show_words]) > 1:
        raise click.UsageError("only one counting flag (-l, -w) may be used at a time")
    if not files:
        data = click.get_binary_stream("stdin").read()
        counts = analyze(data)
        value = counts.words if show_words else counts.lines
        click.echo(f"{value:>7}")
    else:
        for filename in files:
            with open(filename, "rb") as f:
                data = f.read()
            counts = analyze(data)
            value = counts.words if show_words else counts.lines
            click.echo(f"{value:>7} {filename}")


if __name__ == "__main__":
    main()
