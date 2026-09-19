"""Telegram ReactionType string-domain enum."""

from enum import StrEnum


class ReactionType(StrEnum):
    """Telegram reaction type discriminator values."""

    EMOJI = "emoji"
    CUSTOM_EMOJI = "custom_emoji"
    PAID = "paid"
