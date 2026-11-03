from __future__ import annotations

from dataclasses import dataclass
from typing import Any, List, Optional

from .keyboard_button import KeyboardButton
@dataclass
class ReplyKeyboardMarkup:
    """A custom keyboard with reply options.

    Attributes:
        keyboard: Array of button rows, each represented by an Array of KeyboardButton objects.
        resize_keyboard: Requests clients to resize the keyboard vertically for optimal fit.
        one_time_keyboard: Requests clients to hide the keyboard as soon as it's been used.
        input_field_placeholder: The placeholder to be shown in the input field when the keyboard is active.
        selective: Show keyboard to specific users only.
        is_persistent: Requests clients to always show the keyboard when the regular keyboard is hidden.
    """
    keyboard: List[List['KeyboardButton']]
    resize_keyboard: Optional[bool] = None
    one_time_keyboard: Optional[bool] = None
    input_field_placeholder: Optional[str] = None
    selective: Optional[bool] = None
    is_persistent: Optional[bool] = None

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
        return cls(
            keyboard=[[KeyboardButton.from_dict(b) for b in row] for row in data.get('keyboard', [])],
            resize_keyboard=data.get('resize_keyboard'),
            one_time_keyboard=data.get('one_time_keyboard'),
            input_field_placeholder=data.get('input_field_placeholder'),
            selective=data.get('selective'),
            is_persistent=data.get('is_persistent'),
        )
