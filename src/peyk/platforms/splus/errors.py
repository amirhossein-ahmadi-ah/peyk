"""Soroush Plus (Splus) application-level API errors.

Splus answers with the same ``{"ok": ..., "result": ..., "description": ...,
"error_code": ...}`` envelope as the Telegram Bot API, so the error type is a
thin subclass of :class:`peyk.platforms.telegram.errors.TelegramAPIError`.
Catching ``TelegramAPIError`` therefore also catches Splus failures, while
``except SplusAPIError`` isolates the Splus ones.
"""
from __future__ import annotations

from peyk.platforms.telegram.errors import ResponseParameters, TelegramAPIError


class SplusAPIError(TelegramAPIError):
    """Raised when a Splus API response has ``ok: false`` (no rate hint)."""


__all__ = ["ResponseParameters", "SplusAPIError"]
