"""Telegram ChatBoostSourceType string-domain enum."""

from enum import StrEnum


class ChatBoostSourceType(StrEnum):
    """Telegram chat-boost source discriminator values."""

    PREMIUM = "premium"
    GIFT_CODE = "gift_code"
    GIVEAWAY = "giveaway"
