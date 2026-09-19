from __future__ import annotations

from dataclasses import dataclass
from typing import Any, List, Optional

@dataclass
class WebAppData:
    """Data sent from a Mini App to the bot."""
    data: str

    @classmethod
    def from_dict(cls, data: Optional[dict]) -> Optional['WebAppData']:
        """Parse raw Bale data into ``WebAppData``.

Args:
    data (Optional[dict]): Raw API object or ``None``.

Returns:
    Optional[WebAppData]: Parsed object or ``None``.

Raises:
    KeyError: If a required raw field is missing."""
        if data is None:
            return None
        return cls(data=data.get('data', ''))
