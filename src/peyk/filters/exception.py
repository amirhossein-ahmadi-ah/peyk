from __future__ import annotations
from .base import BaseFilter

class ExceptionTypeFilter(BaseFilter):
    """Match an ``ErrorEvent`` by exception type."""
    def __init__(self, *types: type[BaseException]) -> None: self.types = types
    async def __call__(self, event: object, **data: object) -> bool: return isinstance(getattr(event, "exception", None), self.types)

class ExceptionMessageFilter(BaseFilter):
    """Match an ``ErrorEvent`` by exception message."""
    def __init__(self, message: str, *, contains: bool = False) -> None: self.message, self.contains = message, contains
    async def __call__(self, event: object, **data: object) -> bool:
        value = str(getattr(event, "exception", ""))
        return self.message in value if self.contains else value == self.message
