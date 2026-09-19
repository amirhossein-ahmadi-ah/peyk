from __future__ import annotations
from .base import BaseFilter
from peyk.platform_core.contracts import IncomingMessage

class TextEquals(BaseFilter):
    """Match a message whose text equals ``value``."""
    def __init__(self, value: str, case_sensitive: bool = True) -> None:
        self.value, self.case_sensitive = value, case_sensitive
    async def __call__(self, event: object, **data: object) -> bool:
        if not isinstance(event, IncomingMessage) or event.text is None: return False
        return event.text == self.value if self.case_sensitive else event.text.casefold() == self.value.casefold()

class TextContains(BaseFilter):
    """Match a message containing ``value``."""
    def __init__(self, value: str, case_sensitive: bool = True) -> None:
        self.value, self.case_sensitive = value, case_sensitive
    async def __call__(self, event: object, **data: object) -> bool:
        if not isinstance(event, IncomingMessage) or event.text is None: return False
        return self.value in event.text if self.case_sensitive else self.value.casefold() in event.text.casefold()
