from __future__ import annotations

from dataclasses import dataclass
from typing import Any, List, Optional

@dataclass
class User:
    """Represent the Bale Bot API ``User`` object.

Preserves the existing dataclass fields and parsing behavior."""
    id: int
    is_bot: bool
    first_name: str
    last_name: Optional[str] = None
    username: Optional[str] = None
    language_code: Optional[str] = None

    @classmethod
    def from_dict(cls, data: Optional[dict]) -> Optional['User']:
        """Parse raw Bale data into ``User``.

Args:
    data (Optional[dict]): Raw API object or ``None``.

Returns:
    Optional[User]: Parsed object or ``None``.

Raises:
    KeyError: If a required raw field is missing."""
        if data is None:
            return None
        return cls(id=data['id'], is_bot=data.get('is_bot', False), first_name=data.get('first_name', ''), last_name=data.get('last_name'), username=data.get('username'), language_code=data.get('language_code'))
