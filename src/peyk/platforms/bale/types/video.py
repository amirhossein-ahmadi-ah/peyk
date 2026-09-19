from __future__ import annotations

from dataclasses import dataclass
from typing import Any, List, Optional

@dataclass
class Video:
    """Represent the Bale Bot API ``Video`` object.

Preserves the existing dataclass fields and parsing behavior."""
    file_id: str
    file_unique_id: str
    width: int
    height: int
    duration: int
    file_name: Optional[str] = None
    mime_type: Optional[str] = None
    file_size: Optional[int] = None

    @classmethod
    def from_dict(cls, data: Optional[dict]) -> Optional['Video']:
        """Parse raw Bale data into ``Video``.

Args:
    data (Optional[dict]): Raw API object or ``None``.

Returns:
    Optional[Video]: Parsed object or ``None``.

Raises:
    KeyError: If a required raw field is missing."""
        if data is None:
            return None
        return cls(file_id=data.get('file_id', ''), file_unique_id=data.get('file_unique_id', ''), width=data.get('width', 0), height=data.get('height', 0), duration=data.get('duration', 0), file_name=data.get('file_name'), mime_type=data.get('mime_type'), file_size=data.get('file_size'))
