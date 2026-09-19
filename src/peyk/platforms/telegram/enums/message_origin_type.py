"""Telegram MessageOriginType string-domain enum."""

from enum import StrEnum


class MessageOriginType(StrEnum):
    """Telegram message-origin discriminator values."""

    USER = "user"
    HIDDEN_USER = "hidden_user"
    CHAT = "chat"
    CHANNEL = "channel"
