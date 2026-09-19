from __future__ import annotations

from dataclasses import dataclass
from typing import Any, List, Optional

from .user import User
@dataclass
class PreCheckoutQuery:
    """An incoming pre-checkout query (sent before payment finalization)."""
    id: str
    from_: Optional[User] = None
    currency: Optional[str] = None
    total_amount: Optional[int] = None
    invoice_payload: Optional[str] = None

    @classmethod
    def from_dict(cls, data: Optional[dict]) -> Optional['PreCheckoutQuery']:
        """Parse raw Bale data into ``PreCheckoutQuery``.

Args:
    data (Optional[dict]): Raw API object or ``None``.

Returns:
    Optional[PreCheckoutQuery]: Parsed object or ``None``.

Raises:
    KeyError: If a required raw field is missing."""
        if data is None:
            return None
        return cls(id=data.get('id', ''), from_=User.from_dict(data.get('from')), currency=data.get('currency'), total_amount=data.get('total_amount'), invoice_payload=data.get('invoice_payload'))
