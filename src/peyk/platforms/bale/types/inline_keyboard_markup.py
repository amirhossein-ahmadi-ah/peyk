from __future__ import annotations

from dataclasses import dataclass
from typing import Any, List, Optional

from .inline_keyboard_button import InlineKeyboardButton
@dataclass
class InlineKeyboardMarkup:
    """An inline keyboard that appears right next to the message it belongs to."""
    inline_keyboard: List[List['InlineKeyboardButton']]

    @classmethod
    def from_dict(cls, data: Optional[dict]) -> Optional['InlineKeyboardMarkup']:
        """Parse raw Bale data into ``InlineKeyboardMarkup``.

Args:
    data (Optional[dict]): Raw API object or ``None``.

Returns:
    Optional[InlineKeyboardMarkup]: Parsed object or ``None``.

Raises:
    KeyError: If a required raw field is missing."""
        if data is None:
            return None
        return cls(inline_keyboard=[[InlineKeyboardButton.from_dict(b) for b in row] for row in data.get('inline_keyboard', [])])
