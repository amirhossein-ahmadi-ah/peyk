from __future__ import annotations
from dataclasses import dataclass, field
import re
from typing import Any, Dict, List, Mapping, Optional, Sequence, Union
from .message_entity import MessageEntity

@dataclass
class TextQuote:
    """This object contains information about the quoted part of a message that is replied to by the given message.

Attributes:
    text: Text of the quoted part of a message that is replied to by the given message
    position: Approximate quote position in the original message in UTF-16 code units as specified by the sender
    entities: Special entities that appear in the quote. Currently, only bold, italic, underline, strikethrough, spoiler, custom_emoji, and date_time entities are kept in quotes.
    is_manual: True, if the quote was chosen manually by the message sender. Otherwise, the quote was added automatically by the server."""
    text: str
    entities: Optional[List[MessageEntity]] = None
    position: Optional[int] = None
    is_manual: Optional[bool] = None

    @classmethod
    def from_dict(cls, data: Optional[dict]) -> Optional['TextQuote']:
        """Parse a Telegram API mapping into this type.

Args:
    data: Raw Telegram API mapping, or ``None``.

Returns:
    Parsed type instance, or ``None`` when ``data`` is ``None``."""
        if data is None:
            return None
        return cls(text=data.get('text', ''), entities=MessageEntity.list_from(data.get('entities')), position=data.get('position'), is_manual=data.get('is_manual'))
