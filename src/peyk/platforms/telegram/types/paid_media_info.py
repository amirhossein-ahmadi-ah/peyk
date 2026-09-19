from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Dict, List, Mapping, Optional, Sequence, Union

@dataclass
class PaidMediaInfo:
    """Describes the paid media added to a message.

Attributes:
    star_count: The number of Telegram Stars that must be paid to buy access to the media
    paid_media: Information about the paid media"""
    star_count: int
    paid_media: List[PaidMedia]

    @classmethod
    def from_dict(cls, data: Optional[dict]) -> Optional['PaidMediaInfo']:
        """Provides the from dict operation for the Telegram integration.

Args:
    data: Value used by this operation.

Returns:
    Result produced by the operation."""
        "Executes the from_dict operation.\n        \n        Args:\n            data: Value of the declared parameter type.\n        \n        \n        Returns:\n            The operation result (``Optional['PaidMediaInfo']``).\n        "
        if data is None:
            return None
        return cls(star_count=_parse_api_value('Integer', data.get('star_count')), paid_media=_parse_api_value('Array of PaidMedia', data.get('paid_media')))
