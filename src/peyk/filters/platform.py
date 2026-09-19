from __future__ import annotations
from .base import BaseFilter
from peyk.platform_core.capabilities import Feature, get_capabilities

class PlatformFilter(BaseFilter):
    """Match events handled by one of the named platforms."""
    def __init__(self, *platforms: str) -> None: self.platforms = frozenset(platforms)
    async def __call__(self, event: object, **data: object) -> bool:
        bot = data.get("bot") or getattr(event, "bot", None)
        return getattr(bot, "platform", None) in self.platforms

class SupportsFilter(BaseFilter):
    """Match when the injected bot advertises audited support for a feature."""
    def __init__(self, feature: Feature) -> None: self.feature = feature
    async def __call__(self, event: object, **data: object) -> bool:
        bot = data.get("bot") or getattr(event, "bot", None)
        return bool(bot is not None and getattr(bot, "supports")(self.feature))
