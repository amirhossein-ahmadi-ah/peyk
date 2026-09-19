from __future__ import annotations

from dataclasses import dataclass
from typing import Any, List, Optional

@dataclass
class File:
    """Represent the Bale Bot API ``File`` object.

Preserves the existing dataclass fields and parsing behavior."""
    file_id: str
    file_unique_id: str
    file_size: Optional[int] = None
    file_path: Optional[str] = None

    @classmethod
    def from_dict(cls, data: Optional[dict]) -> Optional['File']:
        """Parse raw Bale data into ``File``.

Args:
    data (Optional[dict]): Raw API object or ``None``.

Returns:
    Optional[File]: Parsed object or ``None``.

Raises:
    KeyError: If a required raw field is missing."""
        if data is None:
            return None
        return cls(file_id=data.get('file_id', ''), file_unique_id=data.get('file_unique_id', ''), file_size=data.get('file_size'), file_path=data.get('file_path'))
