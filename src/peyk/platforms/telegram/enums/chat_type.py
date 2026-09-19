"""Telegram chat type values used by the Bot API."""

from enum import StrEnum


class ChatType(StrEnum):
    """Finite Telegram chat-type values."""

    PRIVATE = "private"
    GROUP = "group"
    SUPERGROUP = "supergroup"
    CHANNEL = "channel"
