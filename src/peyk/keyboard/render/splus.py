"""Splus keyboard rendering.

Splus keyboards are Telegram-shaped, so the Telegram renderers are reused.  The
capability gating in :func:`peyk.keyboard.render.common.resolve_inline` already
strips or rejects fields Splus does not confirm (colour styles, ``pay``,
``login_url``, ``switch_inline_query`` ...).
"""
from __future__ import annotations

from .telegram import force_reply, inline_keyboard, remove_keyboard, reply_keyboard

__all__ = ["force_reply", "inline_keyboard", "remove_keyboard", "reply_keyboard"]
