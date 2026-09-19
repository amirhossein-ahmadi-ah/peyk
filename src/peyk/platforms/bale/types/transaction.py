from __future__ import annotations

from dataclasses import dataclass
from typing import Any, List, Optional

@dataclass
class Transaction:
    """A wallet transaction (from `inquireTransaction`)."""
    id: str
    status: str
    userID: int
    amount: int
    createdAt: int

    @classmethod
    def from_dict(cls, data: Optional[dict]) -> Optional['Transaction']:
        """Parse raw Bale data into ``Transaction``.

Args:
    data (Optional[dict]): Raw API object or ``None``.

Returns:
    Optional[Transaction]: Parsed object or ``None``.

Raises:
    KeyError: If a required raw field is missing."""
        if data is None:
            return None
        return cls(id=data.get('id', ''), status=data.get('status', ''), userID=data.get('userID', 0), amount=data.get('amount', 0), createdAt=data.get('createdAt', 0))
