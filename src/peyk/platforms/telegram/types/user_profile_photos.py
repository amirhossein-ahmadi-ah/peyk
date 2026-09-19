from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Dict, List, Mapping, Optional, Sequence, Union

@dataclass
class UserProfilePhotos:
    """This object represent a user's profile pictures.

Attributes:
    total_count: Total number of profile pictures the target user has
    photos: Requested profile pictures (in up to 4 sizes each)"""
    total_count: int = 0
    photos: Optional[List[List[PhotoSize]]] = None

    @classmethod
    def from_dict(cls, data: Optional[dict]) -> Optional['UserProfilePhotos']:
        """Provides the from dict operation for the Telegram integration.

Args:
    data: Value used by this operation.

Returns:
    Result produced by the operation."""
        "Executes the from_dict operation.\n        \n        Args:\n            data: Value of the declared parameter type.\n        \n        \n        Returns:\n            The operation result (``Optional['UserProfilePhotos']``).\n        "
        if data is None:
            return None
        photos_raw = data.get('photos', [])
        return cls(total_count=data.get('total_count', 0), photos=[PhotoSize.list_from(p) for p in photos_raw] if photos_raw else None)
