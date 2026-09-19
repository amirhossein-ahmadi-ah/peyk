from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Dict, List, Mapping, Optional, Sequence, Union

@dataclass
class SuggestedPostParameters:
    """Contains parameters of a post that is being suggested by the bot.

Attributes:
    price: Proposed price for the post. If the field is omitted, then the post is unpaid.
    send_date: Proposed send date of the post. If specified, then the date must be between 300 second and 2678400 seconds (30 days) in the future. If the field is omitted, then the post can be published at any time within 30 days at the sole discretion of the user who approves it."""
    price: Optional[object] = None
    send_date: Optional[int] = None

    def to_dict(self) -> Dict[str, object]:
        """Provides the to dict operation for the Telegram integration.

Returns:
    Result produced by the operation."""
        'Executes the to_dict operation.\n        \n        Returns:\n            The operation result (``Dict[str, object]``).\n        '
        body: Dict[str, object] = {}
        if self.price is not None:
            body['price'] = self.price
        if self.send_date is not None:
            body['send_date'] = self.send_date
        return body
