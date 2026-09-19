from __future__ import annotations
from dataclasses import dataclass, field
import re
from typing import Any, Dict, List, Mapping, Optional, Sequence, Union
from .chat import Chat
from .message_entity import MessageEntity
from .poll_media import PollMedia
from .user import User

@dataclass
class PollOption:
    """This object contains information about one answer option in a poll.

Attributes:
    persistent_id: Unique identifier of the option, persistent on option addition and deletion
    text: Option text, 1-100 characters
    voter_count: Number of users who voted for this option; may be 0 if unknown
    text_entities: Special entities that appear in the option text. Currently, only custom emoji entities are allowed in poll option texts
    media: Media added to the poll option
    added_by_user: User who added the option; omitted if the option wasn't added by a user after poll creation
    added_by_chat: Chat that added the option; omitted if the option wasn't added by a chat after poll creation
    addition_date: Point in time (Unix timestamp) when the option was added; omitted if the option existed in the original poll"""
    persistent_id: Optional[str] = None
    text: str = ''
    text_entities: Optional[List[MessageEntity]] = None
    media: Optional[PollMedia] = None
    voter_count: int = 0
    added_by_user: Optional[User] = None
    added_by_chat: Optional[Chat] = None
    addition_date: Optional[int] = None

    @classmethod
    def from_dict(cls, data: Optional[dict]) -> Optional['PollOption']:
        """Parse a Telegram API mapping into this type.

Args:
    data: Raw Telegram API mapping, or ``None``.

Returns:
    Parsed type instance, or ``None`` when ``data`` is ``None``."""
        if data is None:
            return None
        return cls(persistent_id=data.get('persistent_id'), text=data.get('text', ''), text_entities=MessageEntity.list_from(data.get('text_entities')), media=PollMedia.from_dict(data.get('media')), voter_count=data.get('voter_count', 0), added_by_user=User.from_dict(data.get('added_by_user')), added_by_chat=Chat.from_dict(data.get('added_by_chat')), addition_date=data.get('addition_date'))
