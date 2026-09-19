from __future__ import annotations

from dataclasses import dataclass
from typing import Any, List, Optional

@dataclass
class PhotoSize:
    """Represent the Bale Bot API ``PhotoSize`` object.

Preserves the existing dataclass fields and parsing behavior."""
    file_id: str
    file_unique_id: str
    width: int
    height: int
    file_size: Optional[int] = None

    @classmethod
    def from_dict(cls, data: Optional[dict]) -> Optional['PhotoSize']:
        """Parse raw Bale data into ``PhotoSize``.

Args:
    data (Optional[dict]): Raw API object or ``None``.

Returns:
    Optional[PhotoSize]: Parsed object or ``None``.

Raises:
    KeyError: If a required raw field is missing."""
        if data is None:
            return None
        return cls(file_id=data.get('file_id', ''), file_unique_id=data.get('file_unique_id', ''), width=data.get('width', 0), height=data.get('height', 0), file_size=data.get('file_size'))

    @classmethod
    def list_from_result(cls, data: Optional[List[dict]]) -> Optional[List['PhotoSize']]:
        """Parse raw Bale data into ``PhotoSize``.

Args:
    data (Optional[dict]): Raw API object or ``None``.

Returns:
    Optional[PhotoSize]: Parsed object or ``None``.

Raises:
    KeyError: If a required raw field is missing."""
        if data is None:
            return None
        return [cls.from_dict(item) for item in data]
