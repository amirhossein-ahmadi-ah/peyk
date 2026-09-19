from __future__ import annotations

from dataclasses import dataclass
from typing import Any, List, Optional

@dataclass
class ReplyKeyboardRemove:
    """A request to remove the custom keyboard."""
    remove_keyboard: bool = True

    @classmethod
    def from_dict(cls, data: Optional[dict]) -> Optional['ReplyKeyboardRemove']:
        """Parse raw Bale data into ``ReplyKeyboardRemove``.

Args:
    data (Optional[dict]): Raw API object or ``None``.

Returns:
    Optional[ReplyKeyboardRemove]: Parsed object or ``None``.

Raises:
    KeyError: If a required raw field is missing."""
        if data is None:
            return None
        return cls(remove_keyboard=data.get('remove_keyboard', True))
