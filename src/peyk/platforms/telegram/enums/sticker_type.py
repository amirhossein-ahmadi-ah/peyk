"""Telegram StickerType string-domain enum."""

from enum import StrEnum


class StickerType(StrEnum):
    """Telegram sticker type values."""

    REGULAR = "regular"
    MASK = "mask"
    CUSTOM_EMOJI = "custom_emoji"
