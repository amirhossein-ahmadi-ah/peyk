from __future__ import annotations

from dataclasses import dataclass
from typing import Any, List, Optional

@dataclass
class MessageEntity:
    """A special entity in a text message (mention, bot_command, etc.)."""
    type: str
    offset: int
    length: int

    @classmethod
    def from_dict(cls, data: Optional[dict]) -> Optional['MessageEntity']:
        """Parse raw Bale data into ``MessageEntity``.

Args:
    data (Optional[dict]): Raw API object or ``None``.

Returns:
    Optional[MessageEntity]: Parsed object or ``None``.

Raises:
    KeyError: If a required raw field is missing."""
        if data is None:
            return None
        return cls(type=data.get('type', ''), offset=data.get('offset', 0), length=data.get('length', 0))

    @classmethod
    def list_from_result(cls, data: Optional[List[dict]]) -> Optional[List['MessageEntity']]:
        """Parse raw Bale data into ``MessageEntity``.

Args:
    data (Optional[dict]): Raw API object or ``None``.

Returns:
    Optional[MessageEntity]: Parsed object or ``None``.

Raises:
    KeyError: If a required raw field is missing."""
        if data is None:
            return None
        return [cls.from_dict(item) for item in data]
