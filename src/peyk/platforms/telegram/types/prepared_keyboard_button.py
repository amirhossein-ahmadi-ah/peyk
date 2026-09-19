from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Dict, List, Mapping, Optional, Sequence, Union

@dataclass
class PreparedKeyboardButton:
    """Describes a keyboard button to be used by a user of a Mini App.

Attributes:
    id: Unique identifier of the keyboard button"""
    text: str = ''

    @classmethod
    def from_dict(cls, data: Optional[dict]) -> Optional['PreparedKeyboardButton']:
        """Provides the from dict operation for the Telegram integration.

Args:
    data: Value used by this operation.

Returns:
    Result produced by the operation."""
        "Executes the from_dict operation.\n        \n        Args:\n            data: Value of the declared parameter type.\n        \n        \n        Returns:\n            The operation result (``Optional['PreparedKeyboardButton']``).\n        "
        if data is None:
            return None
        return cls(text=data.get('text', ''))
