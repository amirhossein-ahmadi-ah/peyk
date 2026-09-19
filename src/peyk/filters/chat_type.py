from __future__ import annotations
from .base import BaseFilter
from peyk.types import ChatType as _ChatType

class ChatTypeFilter(BaseFilter):
    """Match a neutral chat type, treating Telegram ``supergroup`` as group."""
    def __init__(self, *chat_types: _ChatType | str) -> None:
        if not chat_types: raise ValueError("ChatTypeFilter requires at least one type")
        normalized: set[_ChatType] = set()
        for value in chat_types:
            if isinstance(value, str) and value == "supergroup": value = "group"
            normalized.add(_ChatType(value) if isinstance(value, str) else value)
        self.chat_types = frozenset(normalized)
    async def __call__(self, event: object, **data: object) -> bool:
        chat = getattr(event, "chat", None)
        if chat is not None: return chat.type in self.chat_types
        value = getattr(event, "chat_type", None)
        if value == "supergroup": value = "group"
        return value is not None and _ChatType(value) in self.chat_types

ChatType = ChatTypeFilter
