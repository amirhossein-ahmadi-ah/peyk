"""Telegram OwnedGiftType string-domain enum."""

from enum import StrEnum


class OwnedGiftType(StrEnum):
    """Telegram owned-gift discriminator values."""

    REGULAR = "regular"
    UNIQUE = "unique"
