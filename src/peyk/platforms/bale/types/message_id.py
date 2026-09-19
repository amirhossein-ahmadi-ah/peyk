from __future__ import annotations

from dataclasses import dataclass
from typing import Any, List, Optional

@dataclass
class MessageId:
    """Represent the Bale Bot API ``MessageId`` object.

Preserves the existing dataclass fields and parsing behavior."""
    message_id: int

    @classmethod
    def from_dict(cls, data: Optional[dict]) -> Optional['MessageId']:
        """Parse raw Bale data into ``MessageId``.

Args:
    data (Optional[dict]): Raw API object or ``None``.

Returns:
    Optional[MessageId]: Parsed object or ``None``.

Raises:
    KeyError: If a required raw field is missing."""
        if data is None:
            return None
        return cls(message_id=data['message_id'])
