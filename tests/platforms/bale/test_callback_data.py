from __future__ import annotations

import pytest

from peyk.platforms.bale.client import (
    MAX_CALLBACK_DATA_BYTES,
    build_inline_keyboard_button,
    validate_callback_data,
)


def test_under_limit_ascii_is_valid() -> None:
    validate_callback_data("action:confirm")  # must not raise


def test_at_exactly_64_bytes_ascii_is_valid() -> None:
    data = "a" * MAX_CALLBACK_DATA_BYTES
    assert len(data.encode("utf-8")) == 64
    validate_callback_data(data)  # must not raise


def test_over_64_bytes_ascii_raises() -> None:
    data = "a" * (MAX_CALLBACK_DATA_BYTES + 1)
    with pytest.raises(ValueError):
        validate_callback_data(data)


def test_empty_string_raises() -> None:
    """Bale's limit is 1-64 bytes -- zero-length callback_data is invalid too."""
    with pytest.raises(ValueError):
        validate_callback_data("")


def test_persian_text_at_boundary_is_byte_length_not_char_count() -> None:
    """Each of these Persian characters encodes to 2 bytes in UTF-8.

    32 characters -> exactly 64 bytes -> valid. This is the case a
    naive `len(data) <= 64` character-count check would get right by
    coincidence but for the wrong reason -- the next test is the one
    that actually distinguishes byte-length checking from char-count
    checking.
    """
    data = "م" * 32
    assert len(data) == 32
    assert len(data.encode("utf-8")) == 64
    validate_callback_data(data)  # must not raise


def test_persian_text_under_64_chars_but_over_64_bytes_raises() -> None:
    """33 two-byte characters = 66 bytes: over the limit despite only

    33 *characters* -- well under 64. A char-count-based check would
    wrongly accept this; only a byte-length check catches it.
    """
    data = "م" * 33
    assert len(data) == 33
    assert len(data.encode("utf-8")) == 66
    with pytest.raises(ValueError):
        validate_callback_data(data)


def test_mixed_ascii_and_persian_over_limit_raises() -> None:
    data = "go:" + ("سلام" * 15)  # "سلام" is 4 chars / 8 bytes in UTF-8
    assert len(data.encode("utf-8")) > MAX_CALLBACK_DATA_BYTES
    with pytest.raises(ValueError):
        validate_callback_data(data)


def test_build_inline_keyboard_button_validates_and_builds() -> None:
    button = build_inline_keyboard_button("Confirm", "action:confirm")
    assert button == {"text": "Confirm", "callback_data": "action:confirm"}


def test_build_inline_keyboard_button_propagates_validation_error() -> None:
    with pytest.raises(ValueError):
        build_inline_keyboard_button("Too long", "x" * 65)
