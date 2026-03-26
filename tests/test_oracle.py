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


# ---------------------------------------------------------------------------
# Mixed whitespace oracle tests (feature 005-whitespace-word-splitting)
# ---------------------------------------------------------------------------


def test_oracle_mixed_tabs_spaces_newlines() -> None:
    """AC1: tabs, spaces, and newlines mixed — matches wc -w."""
    data = b"one\t two  \nthree\t\tfour\n"
    assert _pywcsk_word_stdin_count(data) == _wc_word_stdin_count(data)


def test_oracle_mixed_whitespace_only() -> None:
    """AC2: mixed whitespace only — both report 0."""
    data = b"  \t  \n  \t  \n"
    assert _pywcsk_word_stdin_count(data) == _wc_word_stdin_count(data)


def test_oracle_tab_space_around_newline() -> None:
    """AC3: tab+space before and after newlines — matches wc -w."""
    data = b"one \t\n two\t \nthree\n"
    assert _pywcsk_word_stdin_count(data) == _wc_word_stdin_count(data)


def test_oracle_leading_tabs_and_newlines() -> None:
    """AC4: leading tabs and newlines before first word — matches wc -w."""
    data = b"\t\none\t\ntwo \n"
    assert _pywcsk_word_stdin_count(data) == _wc_word_stdin_count(data)


def test_oracle_blank_line_between_words() -> None:
    """AC5: blank line between words — matches wc -w."""
    data = b"a  b\t\tc\n\nd\n"
    assert _pywcsk_word_stdin_count(data) == _wc_word_stdin_count(data)


# ---------------------------------------------------------------------------
# Byte-count oracle tests (feature 007-byte-counting)
# ---------------------------------------------------------------------------


def _wc_byte_count(path: Path) -> int:
    """Return byte count from system wc -c (integer, platform-safe)."""
    result = subprocess.run(
        ["wc", "-c", str(path)],
        capture_output=True,
        text=True,
        check=True,
    )
    return int(result.stdout.strip().split()[0])


def _pywcsk_byte_count(path: Path) -> int:
    """Return byte count from pywcsk -c (integer)."""
    result = CliRunner().invoke(main, ["-c", str(path)])
    assert result.exit_code == 0, f"pywcsk failed: {result.output}"
    return int(result.output.strip().split()[0])


def _wc_byte_stdin_count(data: bytes) -> int:
    """Return byte count from system wc -c on stdin."""
    result = subprocess.run(
        ["wc", "-c"],
        input=data,
        capture_output=True,
        check=True,
    )
    return int(result.stdout.strip().split()[0])


def _pywcsk_byte_stdin_count(data: bytes) -> int:
    """Return byte count from pywcsk -c on stdin."""
    result = CliRunner().invoke(main, ["-c"], input=data)
    assert result.exit_code == 0, f"pywcsk failed: {result.output}"
    return int(result.output.strip())


def test_oracle_bytes_empty() -> None:
    """AC2: empty file — both report 0."""
    path = FIXTURES / "empty.txt"
    assert _pywcsk_byte_count(path) == _wc_byte_count(path)


def test_oracle_bytes_hello() -> None:
    """AC1: hello.txt — byte counts match wc -c."""
    path = FIXTURES / "hello.txt"
    assert _pywcsk_byte_count(path) == _wc_byte_count(path)


def test_oracle_bytes_multi() -> None:
    """AC3: multi.txt — byte counts match wc -c."""
    path = FIXTURES / "multi.txt"
    assert _pywcsk_byte_count(path) == _wc_byte_count(path)


def test_oracle_bytes_no_newline() -> None:
    """AC4: no_newline.txt — byte counts match wc -c."""
    path = FIXTURES / "no_newline.txt"
    assert _pywcsk_byte_count(path) == _wc_byte_count(path)


def test_oracle_bytes_stdin() -> None:
    """AC5: stdin byte count matches wc -c."""
    data = b"hello world\n"
    assert _pywcsk_byte_stdin_count(data) == _wc_byte_stdin_count(data)


# ---------------------------------------------------------------------------
# Combined-flag oracle tests (feature 008)
# ---------------------------------------------------------------------------


def _wc_cols(flags: list[str], path: Path) -> list[int]:
    """Return integer column values from system wc with given flags."""
    result = subprocess.run(
        ["wc"] + flags + [str(path)],
        capture_output=True,
        text=True,
        check=True,
    )
    return [int(x) for x in result.stdout.strip().split() if not x.endswith(path.name)]


def _pywcsk_cols(flags: list[str], path: Path) -> list[int]:
    """Return integer column values from pywcsk with given flags."""
    result = CliRunner().invoke(main, flags + [str(path)])
    assert result.exit_code == 0, f"pywcsk failed: {result.output}"
    return [int(x) for x in result.output.strip().split() if not x.endswith(path.name)]


def test_oracle_combined_l_w() -> None:
    """AC1: -l -w column values match wc -l -w."""
    path = FIXTURES / "hello.txt"
    assert _pywcsk_cols(["-l", "-w"], path) == _wc_cols(["-l", "-w"], path)


def test_oracle_combined_l_c() -> None:
    """AC3: -l -c column values match wc -l -c."""
    path = FIXTURES / "hello.txt"
    assert _pywcsk_cols(["-l", "-c"], path) == _wc_cols(["-l", "-c"], path)


def test_oracle_combined_w_c() -> None:
    """AC4: -w -c column values match wc -w -c."""
    path = FIXTURES / "hello.txt"
    assert _pywcsk_cols(["-w", "-c"], path) == _wc_cols(["-w", "-c"], path)


def test_oracle_combined_l_w_c() -> None:
    """AC5: -l -w -c column values match wc -l -w -c."""
    path = FIXTURES / "multi.txt"
    assert _pywcsk_cols(["-l", "-w", "-c"], path) == _wc_cols(["-l", "-w", "-c"], path)
