from __future__ import annotations

from dataclasses import dataclass
from typing import Any, List, Optional

@dataclass
class Location:
    """Represent the Bale Bot API ``Location`` object.

Preserves the existing dataclass fields and parsing behavior."""
    longitude: float
    latitude: float

    @classmethod
    def from_dict(cls, data: Optional[dict]) -> Optional['Location']:
        """Parse raw Bale data into ``Location``.

Args:
    data (Optional[dict]): Raw API object or ``None``.

Returns:
    Optional[Location]: Parsed object or ``None``.

Raises:
    KeyError: If a required raw field is missing."""
        if data is None:
            return None
        return cls(longitude=data.get('longitude', 0.0), latitude=data.get('latitude', 0.0))
