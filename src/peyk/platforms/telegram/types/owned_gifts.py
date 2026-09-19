from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Dict, List, Mapping, Optional, Sequence, Union

@dataclass
class OwnedGifts:
    """Contains the list of gifts received and owned by a user or a chat.

Attributes:
    total_count: The total number of gifts owned by the user or the chat
    gifts: The list of gifts
    next_offset: Offset for the next request. If empty, then there are no more results."""
    total_count: int
    gifts: List[OwnedGift]
    next_offset: Optional[str] = None

    @classmethod
    def from_dict(cls, data: Optional[dict]) -> Optional['OwnedGifts']:
        """Provides the from dict operation for the Telegram integration.

Args:
    data: Value used by this operation.

Returns:
    Result produced by the operation."""
        "Executes the from_dict operation.\n        \n        Args:\n            data: Value of the declared parameter type.\n        \n        \n        Returns:\n            The operation result (``Optional['OwnedGifts']``).\n        "
        if data is None:
            return None
        return cls(total_count=_parse_api_value('Integer', data.get('total_count')), gifts=_parse_api_value('Array of OwnedGift', data.get('gifts')), next_offset=_parse_api_value('String', data.get('next_offset')))
