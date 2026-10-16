"""Splus raw-model -> normalized dispatcher contracts.

Splus delivers Telegram-shaped ``Update`` objects, so normalization is the
Telegram normalization.  Splus only emits ``message``, ``edited_message`` and
``callback_query`` updates; the Telegram-only update kinds the shared function
also understands (channel posts, member updates, payments ...) simply never
occur, and anything unrecognized falls through as the raw update.
"""
from __future__ import annotations

from .telegram import (  # noqa: F401
    normalize_bot_membership_from_message,
    normalize_callback,
    normalize_chat_member,
    normalize_message,
    normalize_pre_checkout_query,
    normalize_shipping_query,
    normalize_update,
)

SPLUS_CAPABILITIES = __import__('peyk.platform_core.capabilities.legacy', fromlist=['legacy_capabilities']).legacy_capabilities('splus')
