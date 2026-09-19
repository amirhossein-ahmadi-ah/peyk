"""Telegram PaidMediaType string-domain enum."""

from enum import StrEnum


class PaidMediaType(StrEnum):
    """Telegram paid-media discriminator values."""

    PHOTO = "photo"
    VIDEO = "video"
    PREVIEW = "preview"
    LIVE_PHOTO = "live_photo"
