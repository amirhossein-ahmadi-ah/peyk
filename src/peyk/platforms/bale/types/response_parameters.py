from __future__ import annotations

from dataclasses import dataclass
from typing import Any, List, Optional

@dataclass
class ResponseParameters:
    """Extra information about an unsuccessful API request."""
    retry_after: Optional[int] = None

    @classmethod
    def from_dict(cls, data: Optional[dict]) -> Optional['ResponseParameters']:
        """Parse raw Bale data into ``ResponseParameters``.

Args:
    data (Optional[dict]): Raw API object or ``None``.

Returns:
    Optional[ResponseParameters]: Parsed object or ``None``.

Raises:
    KeyError: If a required raw field is missing."""
        if data is None:
            return None
        return cls(retry_after=data.get('retry_after'))
