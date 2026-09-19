from __future__ import annotations

from dataclasses import dataclass
from typing import Any, List, Optional

@dataclass
class Invoice:
    """An invoice or crowdfunding request message."""
    title: str
    description: str
    total_amount: int

    @classmethod
    def from_dict(cls, data: Optional[dict]) -> Optional['Invoice']:
        """Parse raw Bale data into ``Invoice``.

Args:
    data (Optional[dict]): Raw API object or ``None``.

Returns:
    Optional[Invoice]: Parsed object or ``None``.

Raises:
    KeyError: If a required raw field is missing."""
        if data is None:
            return None
        return cls(title=data.get('title', ''), description=data.get('description', ''), total_amount=data.get('total_amount', 0))
