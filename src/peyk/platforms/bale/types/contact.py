from __future__ import annotations

from dataclasses import dataclass
from typing import Any, List, Optional

@dataclass
class Contact:
    """Represent the Bale Bot API ``Contact`` object.

Preserves the existing dataclass fields and parsing behavior."""
    phone_number: str
    first_name: str
    last_name: Optional[str] = None
    user_id: Optional[int] = None

    @classmethod
    def from_dict(cls, data: Optional[dict]) -> Optional['Contact']:
        """Parse raw Bale data into ``Contact``.

Args:
    data (Optional[dict]): Raw API object or ``None``.

Returns:
    Optional[Contact]: Parsed object or ``None``.

Raises:
    KeyError: If a required raw field is missing."""
        if data is None:
            return None
        return cls(phone_number=data.get('phone_number', ''), first_name=data.get('first_name', ''), last_name=data.get('last_name'), user_id=data.get('user_id'))
