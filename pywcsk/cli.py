"""CLI for pywcsk."""

import click

from . import __version__


@click.command()
@click.version_option(version=__version__, prog_name="pywcsk")
@click.argument("files", nargs=-1)
def main(files: tuple[str, ...]) -> None:
    """Count lines, words, and bytes — a Python implementation of wc."""


if __name__ == "__main__":
    main()
