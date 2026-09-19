from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Dict, List, Mapping, Optional, Sequence, Union

@dataclass
class PaidMediaPurchased:
    """This object contains information about a paid media purchase.

Attributes:
    from: User who purchased the media
    paid_media_payload: Bot-specified paid media payload"""
    user: Optional[User] = None
    paid_media_payload: str = ''

    @classmethod
    def from_dict(cls, data: Optional[dict]) -> Optional['PaidMediaPurchased']:
        """Provides the from dict operation for the Telegram integration.

Args:
    data: Value used by this operation.

Returns:
    Result produced by the operation."""
        "Executes the from_dict operation.\n        \n        Args:\n            data: Value of the declared parameter type.\n        \n        \n        Returns:\n            The operation result (``Optional['PaidMediaPurchased']``).\n        "
        if data is None:
            return None
        return cls(user=User.from_dict(data.get('user')), paid_media_payload=data.get('paid_media_payload', ''))
