"""Integration tests for the pywcsk CLI (Click CliRunner)."""

from click.testing import CliRunner

from pywcsk import __version__
from pywcsk.cli import main


def test_version_flag() -> None:
    """--version prints version string and exits 0."""
    result = CliRunner().invoke(main, ["--version"])
    assert result.exit_code == 0
    assert __version__ in result.output


def test_help_flag() -> None:
    """--help prints usage information and exits 0."""
    result = CliRunner().invoke(main, ["--help"])
    assert result.exit_code == 0
    assert "Usage:" in result.output


def test_no_args_exits_zero() -> None:
    """Invoking with no arguments exits 0 (reads stdin, which is empty)."""
    result = CliRunner().invoke(main, [], input="")
    assert result.exit_code == 0
