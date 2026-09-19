from __future__ import annotations

from dataclasses import dataclass
from typing import Any, List, Optional

from .message import Message
from .user import User
@dataclass
class CallbackQuery:
    """Represent the Bale Bot API ``CallbackQuery`` object.

Preserves the existing dataclass fields and parsing behavior."""
    id: str
    from_: Optional[User] = None
    message: Optional[Message] = None
    data: Optional[str] = None

    @classmethod
    def from_dict(cls, data: Optional[dict]) -> Optional['CallbackQuery']:
        """Parse raw Bale data into ``CallbackQuery``.

Args:
    data (Optional[dict]): Raw API object or ``None``.

Returns:
    Optional[CallbackQuery]: Parsed object or ``None``.

Raises:
    KeyError: If a required raw field is missing."""
        if data is None:
            return None
        return cls(id=data['id'], from_=User.from_dict(data.get('from')), message=Message.from_dict(data.get('message')), data=data.get('data'))
