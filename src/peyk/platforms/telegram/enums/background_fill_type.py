"""Telegram BackgroundFillType string-domain enum."""

from enum import StrEnum


class BackgroundFillType(StrEnum):
    """Telegram background-fill discriminator values."""

    SOLID = "solid"
    GRADIENT = "gradient"
    FREEFORM_GRADIENT = "freeform_gradient"
