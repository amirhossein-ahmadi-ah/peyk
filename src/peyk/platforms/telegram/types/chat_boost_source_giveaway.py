from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Dict, List, Mapping, Optional, Sequence, Union

@dataclass
class ChatBoostSourceGiveaway:
    """The boost was obtained by the creation of a Telegram Premium or a Telegram Star giveaway. This boosts the chat 4 times for the duration of the corresponding Telegram Premium subscription for Telegram Premium giveaways and prize_star_count / 500 times for one year for Telegram Star giveaways.

Attributes:
    source: Source of the boost, always 'giveaway'
    giveaway_message_id: Identifier of a message in the chat with the giveaway; the message could have been deleted already. May be 0 if the message isn't sent yet.
    user: User that won the prize in the giveaway if any; for Telegram Premium giveaways only
    prize_star_count: The number of Telegram Stars to be split between giveaway winners; for Telegram Star giveaways only
    is_unclaimed: True, if the giveaway was completed, but there was no user to win the prize"""
    source: str
    giveaway_message_id: int
    user: Optional[User] = None
    prize_star_count: Optional[int] = None
    is_unclaimed: Optional[bool] = None

    @classmethod
    def from_dict(cls, data: Optional[dict]) -> Optional['ChatBoostSourceGiveaway']:
        """Provides the from dict operation for the Telegram integration.

Args:
    data: Value used by this operation.

Returns:
    Result produced by the operation."""
        "Executes the from_dict operation.\n        \n        Args:\n            data: Value of the declared parameter type.\n        \n        \n        Returns:\n            The operation result (``Optional['ChatBoostSourceGiveaway']``).\n        "
        if data is None:
            return None
        return cls(source=_parse_api_value('String', data.get('source')), giveaway_message_id=_parse_api_value('Integer', data.get('giveaway_message_id')), user=_parse_api_value('User', data.get('user')), prize_star_count=_parse_api_value('Integer', data.get('prize_star_count')), is_unclaimed=_parse_api_value('True', data.get('is_unclaimed')))
