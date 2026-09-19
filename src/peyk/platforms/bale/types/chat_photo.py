from __future__ import annotations

from dataclasses import dataclass
from typing import Any, List, Optional

@dataclass
class ChatPhoto:
    """Represent the Bale Bot API ``ChatPhoto`` object.

Preserves the existing dataclass fields and parsing behavior."""
    small_file_id: str
    small_file_unique_id: str
    big_file_id: str
    big_file_unique_id: str

    @classmethod
    def from_dict(cls, data: Optional[dict]) -> Optional['ChatPhoto']:
        """Parse raw Bale data into ``ChatPhoto``.

Args:
    data (Optional[dict]): Raw API object or ``None``.

Returns:
    Optional[ChatPhoto]: Parsed object or ``None``.

Raises:
    KeyError: If a required raw field is missing."""
        if data is None:
            return None
        return cls(small_file_id=data.get('small_file_id', ''), small_file_unique_id=data.get('small_file_unique_id', ''), big_file_id=data.get('big_file_id', ''), big_file_unique_id=data.get('big_file_unique_id', ''))
