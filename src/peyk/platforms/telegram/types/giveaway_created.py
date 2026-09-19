from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Dict, List, Mapping, Optional, Sequence, Union

@dataclass
class GiveawayCreated:
    """This object represents a service message about the creation of a scheduled giveaway.

Attributes:
    prize_star_count: The number of Telegram Stars to be split between giveaway winners; for Telegram Star giveaways only"""
    prize_star_count: Optional[int] = None

    @classmethod
    def from_dict(cls, data: Optional[dict]) -> Optional['GiveawayCreated']:
        """Provides the from dict operation for the Telegram integration.

Args:
    data: Value used by this operation.

Returns:
    Result produced by the operation."""
        "Executes the from_dict operation.\n        \n        Args:\n            data: Value of the declared parameter type.\n        \n        \n        Returns:\n            The operation result (``Optional['GiveawayCreated']``).\n        "
        if data is None:
            return None
        return cls(prize_star_count=_parse_api_value('Integer', data.get('prize_star_count')))
