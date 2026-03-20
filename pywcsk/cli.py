"""CLI for pywcsk."""

import click

from . import __version__


@click.group()
@click.version_option(version=__version__, prog_name="pywcsk")
def main() -> None:
    """Python wc using Spec Kit - pywcwk."""


if __name__ == "__main__":
    main()
