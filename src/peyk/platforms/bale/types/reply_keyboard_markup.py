from __future__ import annotations

from dataclasses import dataclass
from typing import Any, List, Optional

from .keyboard_button import KeyboardButton
@dataclass
class ReplyKeyboardMarkup:
    """A custom keyboard with reply options."""
    keyboard: List[List['KeyboardButton']]

    @classmethod
    def from_dict(cls, data: Optional[dict]) -> Optional['ReplyKeyboardMarkup']:
        """Parse raw Bale data into ``ReplyKeyboardMarkup``.

Args:
    data (Optional[dict]): Raw API object or ``None``.

Returns:
    Optional[ReplyKeyboardMarkup]: Parsed object or ``None``.

Raises:
    KeyError: If a required raw field is missing."""
        if data is None:
            return None
        return cls(keyboard=[[KeyboardButton.from_dict(b) for b in row] for row in data.get('keyboard', [])])
