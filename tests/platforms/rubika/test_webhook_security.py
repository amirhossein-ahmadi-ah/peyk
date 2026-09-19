"""Tests for the generic constant-time compare helper."""

from __future__ import annotations

from peyk.platforms.rubika.webhook_security import constant_time_compare


def test_same_strings_match() -> None:
    assert constant_time_compare("abc", "abc") is True


def test_different_strings_no_match() -> None:
    assert constant_time_compare("abc", "xyz") is False


def test_none_never_matches() -> None:
    assert constant_time_compare(None, "abc") is False
    assert constant_time_compare("abc", None) is False


def test_empty_never_matches() -> None:
    assert constant_time_compare("", "abc") is False
    assert constant_time_compare("abc", "") is False