"""Telegram BackgroundType string-domain enum."""

from enum import StrEnum


class BackgroundType(StrEnum):
    """Telegram background-type discriminator values."""

    FILL = "fill"
    WALLPAPER = "wallpaper"
    PATTERN = "pattern"
    CHAT_THEME = "chat_theme"
