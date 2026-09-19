from __future__ import annotations

from dataclasses import dataclass
from typing import Any, List, Optional

from .chat_photo import ChatPhoto
@dataclass
class Chat:
    """Represent the Bale Bot API ``Chat`` object.

Preserves the existing dataclass fields and parsing behavior."""
    id: int
    type: str
    title: Optional[str] = None
    username: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    photo: Optional[ChatPhoto] = None
    bio: Optional[str] = None
    description: Optional[str] = None
    invite_link: Optional[str] = None
    linked_chat_id: Optional[str] = None

    @classmethod
    def from_dict(cls, data: Optional[dict]) -> Optional['Chat']:
        """Parse raw Bale data into ``Chat``.

Args:
    data (Optional[dict]): Raw API object or ``None``.

Returns:
    Optional[Chat]: Parsed object or ``None``.

Raises:
    KeyError: If a required raw field is missing."""
        if data is None:
            return None
        return cls(id=data['id'], type=data.get('type', ''), title=data.get('title'), username=data.get('username'), first_name=data.get('first_name'), last_name=data.get('last_name'), photo=ChatPhoto.from_dict(data.get('photo')), bio=data.get('bio'), description=data.get('description'), invite_link=data.get('invite_link'), linked_chat_id=data.get('linked_chat_id'))
