from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Dict, List, Mapping, Optional, Sequence, Union

@dataclass
class GiveawayCompleted:
    """This object represents a service message about the completion of a giveaway without public winners.

Attributes:
    winner_count: Number of winners in the giveaway
    unclaimed_prize_count: Number of undistributed prizes
    giveaway_message: Message with the giveaway that was completed, if it wasn't deleted
    is_star_giveaway: True, if the giveaway is a Telegram Star giveaway. Otherwise, currently, the giveaway is a Telegram Premium giveaway."""
    winner_count: int
    unclaimed_prize_count: Optional[int] = None
    giveaway_message: Optional[Message] = None
    is_star_giveaway: Optional[bool] = None

    @classmethod
    def from_dict(cls, data: Optional[dict]) -> Optional['GiveawayCompleted']:
        """Provides the from dict operation for the Telegram integration.

Args:
    data: Value used by this operation.

Returns:
    Result produced by the operation."""
        "Executes the from_dict operation.\n        \n        Args:\n            data: Value of the declared parameter type.\n        \n        \n        Returns:\n            The operation result (``Optional['GiveawayCompleted']``).\n        "
        if data is None:
            return None
        return cls(winner_count=_parse_api_value('Integer', data.get('winner_count')), unclaimed_prize_count=_parse_api_value('Integer', data.get('unclaimed_prize_count')), giveaway_message=_parse_api_value('Message', data.get('giveaway_message')), is_star_giveaway=_parse_api_value('True', data.get('is_star_giveaway')))
