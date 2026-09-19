"""Errors shared by platform capability enforcement."""
from __future__ import annotations

from peyk.platform_core.capabilities import Support, Feature


class UnsupportedFeatureError(RuntimeError):
    """Raised when a requested functional feature is not supported by a platform."""

    def __init__(self, feature: Feature, platform: str, support: Support) -> None:
        self.feature = feature
        self.platform = platform
        self.support = support
        super().__init__(f"Feature {feature.value!r} is not supported on {platform!r} ({support.level.value}).")
