"""Telegram InputPaidMediaType string-domain enum."""

from enum import StrEnum


class InputPaidMediaType(StrEnum):
    """Telegram input-paid-media discriminator values."""

    PHOTO = "photo"
    VIDEO = "video"
    LIVE_PHOTO = "live_photo"
