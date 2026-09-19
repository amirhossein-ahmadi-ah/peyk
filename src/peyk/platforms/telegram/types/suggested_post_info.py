from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Dict, List, Mapping, Optional, Sequence, Union

@dataclass
class SuggestedPostInfo:
    """Contains information about a suggested post.

Attributes:
    state: State of the suggested post. Currently, it can be one of 'pending', 'approved', 'declined'.
    price: Proposed price of the post. If the field is omitted, then the post is unpaid.
    send_date: Proposed send date of the post. If the field is omitted, then the post can be published at any time within 30 days at the sole discretion of the user or administrator who approves it."""
    price: Optional[object] = None
    send_date: Optional[int] = None
    is_approved: Optional[bool] = None
    is_declined: Optional[bool] = None
    decline_comment: Optional[str] = None
    refund_reason: Optional[str] = None

    @classmethod
    def from_dict(cls, data: Optional[dict]) -> Optional['SuggestedPostInfo']:
        """Provides the from dict operation for the Telegram integration.

Args:
    data: Value used by this operation.

Returns:
    Result produced by the operation."""
        "Executes the from_dict operation.\n        \n        Args:\n            data: Value of the declared parameter type.\n        \n        \n        Returns:\n            The operation result (``Optional['SuggestedPostInfo']``).\n        "
        if data is None:
            return None
        return cls(price=data.get('price'), send_date=data.get('send_date'), is_approved=data.get('is_approved'), is_declined=data.get('is_declined'), decline_comment=data.get('decline_comment'), refund_reason=data.get('refund_reason'))
