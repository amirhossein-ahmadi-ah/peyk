from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Dict, List, Mapping, Optional, Sequence, Union

@dataclass
class InlineKeyboardMarkup:
    """This object represents an inline keyboard that appears right next to the message it belongs to.

Attributes:
    inline_keyboard: Array of button rows, each represented by an Array of InlineKeyboardButton objects"""
    inline_keyboard: List[List[InlineKeyboardButton]] = field(default_factory=list)

    @classmethod
    def from_dict(cls, data: Optional[dict]) -> Optional['InlineKeyboardMarkup']:
        """Provides the from dict operation for the Telegram integration.

Args:
    data: Value used by this operation.

Returns:
    Result produced by the operation."""
        "Executes the from_dict operation.\n        \n        Args:\n            data: Value of the declared parameter type.\n        \n        \n        Returns:\n            The operation result (``Optional['InlineKeyboardMarkup']``).\n        "
        if data is None:
            return None
        rows = []
        for row in data.get('inline_keyboard', []) or []:
            rows.append([b for b in (InlineKeyboardButton.from_dict(item) for item in row) if b is not None])
        return cls(inline_keyboard=rows)

    def to_dict(self) -> Dict[str, object]:
        """Provides the to dict operation for the Telegram integration.

Returns:
    Result produced by the operation."""
        'Executes the to_dict operation.\n        \n        Returns:\n            The operation result (``Dict[str, object]``).\n        '
        return {'inline_keyboard': [[button.to_dict() for button in row] for row in self.inline_keyboard]}
