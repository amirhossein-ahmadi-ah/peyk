from __future__ import annotations
from .base import BaseFilter, normalize_filter
class MagicData(BaseFilter):
    """Evaluate a magic filter against dispatcher dependency data."""
    def __init__(self, magic: object) -> None: self.magic = magic
    async def __call__(self, event: object, **data: object) -> bool | dict[str, object]:
        # MagicFilter itself can evaluate mappings through keyword lookup.
        value = data
        result = self.magic.resolve(value) if hasattr(self.magic, "resolve") else self.magic(value)  # type: ignore[attr-defined]
        if hasattr(result, "__await__"): result = await result
        return bool(result)
