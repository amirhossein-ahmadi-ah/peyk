from __future__ import annotations

from dataclasses import dataclass
from typing import Any, List, Optional

@dataclass
class WebAppInfo:
    """Information about a Mini App."""
    url: str

    @classmethod
    def from_dict(cls, data: Optional[dict]) -> Optional['WebAppInfo']:
        """Parse raw Bale data into ``WebAppInfo``.

Args:
    data (Optional[dict]): Raw API object or ``None``.

Returns:
    Optional[WebAppInfo]: Parsed object or ``None``.

Raises:
    KeyError: If a required raw field is missing."""
        if data is None:
            return None
        return cls(url=data.get('url', ''))
