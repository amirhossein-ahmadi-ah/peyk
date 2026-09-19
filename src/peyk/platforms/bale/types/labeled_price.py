from __future__ import annotations

from dataclasses import dataclass
from typing import Any, List, Optional

@dataclass
class LabeledPrice:
    """A portion of the price for goods or services."""
    label: str
    amount: int

    @classmethod
    def from_dict(cls, data: Optional[dict]) -> Optional['LabeledPrice']:
        """Parse raw Bale data into ``LabeledPrice``.

Args:
    data (Optional[dict]): Raw API object or ``None``.

Returns:
    Optional[LabeledPrice]: Parsed object or ``None``.

Raises:
    KeyError: If a required raw field is missing."""
        if data is None:
            return None
        return cls(label=data.get('label', ''), amount=data.get('amount', 0))

    @classmethod
    def list_from_result(cls, data: Optional[List[dict]]) -> Optional[List['LabeledPrice']]:
        """Parse raw Bale data into ``LabeledPrice``.

Args:
    data (Optional[dict]): Raw API object or ``None``.

Returns:
    Optional[LabeledPrice]: Parsed object or ``None``.

Raises:
    KeyError: If a required raw field is missing."""
        if data is None:
            return None
        return [cls.from_dict(item) for item in data]
