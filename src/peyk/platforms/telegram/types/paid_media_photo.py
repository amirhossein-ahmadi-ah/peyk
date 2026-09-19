from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Dict, List, Mapping, Optional, Sequence, Union

@dataclass
class PaidMediaPhoto:
    """The paid media is a photo.

Attributes:
    type: Type of the paid media, always 'photo'
    photo: The photo"""
    photo: List[PhotoSize]
    type: str = 'photo'

    @classmethod
    def from_dict(cls, data: Optional[dict]) -> Optional['PaidMediaPhoto']:
        """Provides the from dict operation for the Telegram integration.

Args:
    data: Value used by this operation.

Returns:
    Result produced by the operation."""
        "Executes the from_dict operation.\n        \n        Args:\n            data: Value of the declared parameter type.\n        \n        \n        Returns:\n            The operation result (``Optional['PaidMediaPhoto']``).\n        "
        if data is None:
            return None
        return cls(photo=_parse_api_value('Array of PhotoSize', data.get('photo')), type=_parse_api_value('String', data.get('type')))
