"""Basic tests for pywcsk."""

import pywcsk


def test_version() -> None:
    """Test that version is defined."""
    assert pywcsk.__version__ == "0.1.0"


def test_import() -> None:
    """Test that pywcsk can be imported."""
    assert pywcsk is not None
