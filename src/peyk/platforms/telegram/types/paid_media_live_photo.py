from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Dict, List, Mapping, Optional, Sequence, Union

@dataclass
class PaidMediaLivePhoto:
    """The paid media is a live photo.

Attributes:
    type: Type of the paid media, always 'live_photo'
    live_photo: The photo"""
    type: str = 'live_photo'
    live_photo: Optional[LivePhoto] = None

    @classmethod
    def from_dict(cls, data: Optional[dict]) -> Optional['PaidMediaLivePhoto']:
        """Provides the from dict operation for the Telegram integration.

Args:
    data: Value used by this operation.

Returns:
    Result produced by the operation."""
        "Executes the from_dict operation.\n        \n        Args:\n            data: Value of the declared parameter type.\n        \n        \n        Returns:\n            The operation result (``Optional['PaidMediaLivePhoto']``).\n        "
        if data is None:
            return None
        return cls(type=data.get('type', 'live_photo'), live_photo=LivePhoto.from_dict(data.get('live_photo')))
