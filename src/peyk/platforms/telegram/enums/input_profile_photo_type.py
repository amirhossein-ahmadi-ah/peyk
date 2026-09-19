"""Telegram InputProfilePhotoType string-domain enum."""

from enum import StrEnum


class InputProfilePhotoType(StrEnum):
    """Telegram input-profile-photo discriminator values."""

    STATIC = "static"
    ANIMATED = "animated"
