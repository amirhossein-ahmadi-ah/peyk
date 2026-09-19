"""Unsupported-feature policy controls."""
from enum import Enum

class UnsupportedPolicy(str, Enum):
    """How unsupported cosmetic operations are handled."""
    DEFAULT = "default"
    RAISE = "raise"
    DEGRADE = "degrade"
    STRIP = "strip"

class StyleFallback(str, Enum):
    """Fallback for button styles on platforms without native color styles."""
    NONE = "none"
    EMOJI = "emoji"
