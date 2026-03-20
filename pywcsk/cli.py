"""CLI for pywcsk."""

import click

from . import __version__
from .counter import analyze


@click.command()
@click.version_option(version=__version__, prog_name="pywcsk")
@click.argument("files", nargs=-1)
def main(files: tuple[str, ...]) -> None:
    """Count lines, words, and bytes — a Python implementation of wc."""
    if not files:
        data = click.get_binary_stream("stdin").read()
        counts = analyze(data)
        click.echo(f"{counts.lines:>7}")
    else:
        for filename in files:
            with open(filename, "rb") as f:
                data = f.read()
            counts = analyze(data)
            click.echo(f"{counts.lines:>7} {filename}")


if __name__ == "__main__":
    main()
