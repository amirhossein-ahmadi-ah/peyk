"""Telegram StoryAreaType string-domain enum."""

from enum import StrEnum


class StoryAreaType(StrEnum):
    """Telegram story-area discriminator values."""

    LOCATION = "location"
    SUGGESTED_REACTION = "suggested_reaction"
    LINK = "link"
    WEATHER = "weather"
    UNIQUE_GIFT = "unique_gift"
