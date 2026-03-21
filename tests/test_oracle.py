"""Oracle tests — compare pywcsk line counts against system wc.

Uses integer comparison so tests pass on both BSD wc (macOS) and GNU wc
(Linux), which differ in output column width.

Run selectively: pytest -m oracle
"""

from pathlib import Path
import shutil
import subprocess

from click.testing import CliRunner
import pytest

from pywcsk.cli import main

pytestmark = pytest.mark.oracle

FIXTURES = Path(__file__).parent / "fixtures"


def _wc_line_count(path: Path) -> int:
    """Return line count from system wc -l (integer, platform-safe)."""
    result = subprocess.run(
        ["wc", "-l", str(path)],
        capture_output=True,
        text=True,
        check=True,
    )
    return int(result.stdout.strip().split()[0])


def _pywcsk_line_count(path: Path) -> int:
    """Return line count from pywcsk (integer)."""
    result = CliRunner().invoke(main, [str(path)])
    assert result.exit_code == 0, f"pywcsk failed: {result.output}"
    return int(result.output.strip().split()[0])


def _wc_stdin_count(data: bytes) -> int:
    """Return line count from system wc -l on stdin."""
    result = subprocess.run(
        ["wc", "-l"],
        input=data,
        capture_output=True,
        check=True,
    )
    return int(result.stdout.strip().split()[0])


def _pywcsk_stdin_count(data: bytes) -> int:
    """Return line count from pywcsk on stdin."""
    result = CliRunner().invoke(main, [], input=data)
    assert result.exit_code == 0, f"pywcsk failed: {result.output}"
    return int(result.output.strip())


@pytest.fixture(scope="session", autouse=True)
def require_wc() -> None:
    """Skip entire module if wc is not available."""
    if not shutil.which("wc"):
        pytest.skip("system wc not found on PATH")


def test_oracle_empty() -> None:
    """Empty file: pywcsk and wc -l both report 0."""
    path = FIXTURES / "empty.txt"
    assert _pywcsk_line_count(path) == _wc_line_count(path)


def test_oracle_hello() -> None:
    """Single-line file: counts match wc -l."""
    path = FIXTURES / "hello.txt"
    assert _pywcsk_line_count(path) == _wc_line_count(path)


def test_oracle_multi() -> None:
    """Multi-line file: counts match wc -l."""
    path = FIXTURES / "multi.txt"
    assert _pywcsk_line_count(path) == _wc_line_count(path)


def test_oracle_no_newline() -> None:
    """File without trailing newline: both report 0."""
    path = FIXTURES / "no_newline.txt"
    assert _pywcsk_line_count(path) == _wc_line_count(path)


def test_oracle_stdin_one_line() -> None:
    """One line on stdin: counts match wc -l."""
    data = b"hello world\n"
    assert _pywcsk_stdin_count(data) == _wc_stdin_count(data)


def test_oracle_stdin_multi() -> None:
    """Multiple lines on stdin: counts match wc -l."""
    data = b"one\ntwo\nthree\n"
    assert _pywcsk_stdin_count(data) == _wc_stdin_count(data)


# ---------------------------------------------------------------------------
# Word-count oracle tests (feature 003-count-words)
# ---------------------------------------------------------------------------


def _wc_word_count(path: Path) -> int:
    """Return word count from system wc -w (integer, platform-safe)."""
    result = subprocess.run(
        ["wc", "-w", str(path)],
        capture_output=True,
        text=True,
        check=True,
    )
    return int(result.stdout.strip().split()[0])


def _pywcsk_word_count(path: Path) -> int:
    """Return word count from pywcsk -w (integer)."""
    result = CliRunner().invoke(main, ["-w", str(path)])
    assert result.exit_code == 0, f"pywcsk failed: {result.output}"
    return int(result.output.strip().split()[0])


def _wc_word_stdin_count(data: bytes) -> int:
    """Return word count from system wc -w on stdin."""
    result = subprocess.run(
        ["wc", "-w"],
        input=data,
        capture_output=True,
        check=True,
    )
    return int(result.stdout.strip().split()[0])


def _pywcsk_word_stdin_count(data: bytes) -> int:
    """Return word count from pywcsk -w on stdin."""
    result = CliRunner().invoke(main, ["-w"], input=data)
    assert result.exit_code == 0, f"pywcsk failed: {result.output}"
    return int(result.output.strip())


def test_oracle_words_empty() -> None:
    """Empty file: pywcsk -w and wc -w both report 0."""
    path = FIXTURES / "empty.txt"
    assert _pywcsk_word_count(path) == _wc_word_count(path)


def test_oracle_words_hello() -> None:
    """Single-word file: counts match wc -w."""
    path = FIXTURES / "hello.txt"
    assert _pywcsk_word_count(path) == _wc_word_count(path)


def test_oracle_words_multi() -> None:
    """Multi-word file: counts match wc -w."""
    path = FIXTURES / "multi.txt"
    assert _pywcsk_word_count(path) == _wc_word_count(path)


def test_oracle_words_no_newline() -> None:
    """File without trailing newline: both report 1."""
    path = FIXTURES / "no_newline.txt"
    assert _pywcsk_word_count(path) == _wc_word_count(path)


def test_oracle_words_stdin_multi() -> None:
    """Multiple words on stdin: counts match wc -w."""
    data = b"one two\nthree four\nfive\n"
    assert _pywcsk_word_stdin_count(data) == _wc_word_stdin_count(data)


# ---------------------------------------------------------------------------
# Line-count flag oracle tests (feature 004-flag-l)
# ---------------------------------------------------------------------------


def _pywcsk_flag_l_count(path: Path) -> int:
    """Return line count from pywcsk -l (integer)."""
    result = CliRunner().invoke(main, ["-l", str(path)])
    assert result.exit_code == 0, f"pywcsk failed: {result.output}"
    return int(result.output.strip().split()[0])


def _pywcsk_flag_l_stdin_count(data: bytes) -> int:
    """Return line count from pywcsk -l on stdin."""
    result = CliRunner().invoke(main, ["-l"], input=data)
    assert result.exit_code == 0, f"pywcsk failed: {result.output}"
    return int(result.output.strip())


def test_oracle_flag_l_empty() -> None:
    """Empty file: pywcsk -l and wc -l both report 0."""
    path = FIXTURES / "empty.txt"
    assert _pywcsk_flag_l_count(path) == _wc_line_count(path)


def test_oracle_flag_l_hello() -> None:
    """Single-line file: pywcsk -l matches wc -l."""
    path = FIXTURES / "hello.txt"
    assert _pywcsk_flag_l_count(path) == _wc_line_count(path)


def test_oracle_flag_l_multi() -> None:
    """Multi-line file: pywcsk -l matches wc -l."""
    path = FIXTURES / "multi.txt"
    assert _pywcsk_flag_l_count(path) == _wc_line_count(path)


def test_oracle_flag_l_no_newline() -> None:
    """File without trailing newline: both report 0."""
    path = FIXTURES / "no_newline.txt"
    assert _pywcsk_flag_l_count(path) == _wc_line_count(path)


def test_oracle_flag_l_stdin() -> None:
    """Multiple lines on stdin: pywcsk -l matches wc -l."""
    data = b"one\ntwo\nthree\n"
    assert _pywcsk_flag_l_stdin_count(data) == _wc_stdin_count(data)
