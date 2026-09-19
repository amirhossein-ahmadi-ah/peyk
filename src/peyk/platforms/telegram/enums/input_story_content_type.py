"""Telegram InputStoryContentType string-domain enum."""

from enum import StrEnum


class InputStoryContentType(StrEnum):
    """Telegram input-story-content discriminator values."""

    PHOTO = "photo"
    VIDEO = "video"
