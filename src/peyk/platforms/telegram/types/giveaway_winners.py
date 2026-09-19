from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Dict, List, Mapping, Optional, Sequence, Union

@dataclass
class GiveawayWinners:
    """This object represents a message about the completion of a giveaway with public winners.

Attributes:
    chat: The chat that created the giveaway
    giveaway_message_id: Identifier of the message with the giveaway in the chat
    winners_selection_date: Point in time (Unix timestamp) when winners of the giveaway were selected
    winner_count: Total number of winners in the giveaway
    winners: List of up to 100 winners of the giveaway
    additional_chat_count: The number of other chats the user had to join in order to be eligible for the giveaway
    prize_star_count: The number of Telegram Stars that were split between giveaway winners; for Telegram Star giveaways only
    premium_subscription_month_count: The number of months the Telegram Premium subscription won from the giveaway will be active for; for Telegram Premium giveaways only
    unclaimed_prize_count: Number of undistributed prizes
    only_new_members: True, if only users who had joined the chats after the giveaway started were eligible to win
    was_refunded: True, if the giveaway was canceled because the payment for it was refunded
    prize_description: Description of additional giveaway prize"""
    chat: Chat
    giveaway_message_id: int
    winners_selection_date: int
    winner_count: int
    winners: List[User]
    additional_chat_count: Optional[int] = None
    prize_star_count: Optional[int] = None
    premium_subscription_month_count: Optional[int] = None
    unclaimed_prize_count: Optional[int] = None
    only_new_members: Optional[bool] = None
    was_refunded: Optional[bool] = None
    prize_description: Optional[str] = None

    @classmethod
    def from_dict(cls, data: Optional[dict]) -> Optional['GiveawayWinners']:
        """Provides the from dict operation for the Telegram integration.

Args:
    data: Value used by this operation.

Returns:
    Result produced by the operation."""
        "Executes the from_dict operation.\n        \n        Args:\n            data: Value of the declared parameter type.\n        \n        \n        Returns:\n            The operation result (``Optional['GiveawayWinners']``).\n        "
        if data is None:
            return None
        return cls(chat=_parse_api_value('Chat', data.get('chat')), giveaway_message_id=_parse_api_value('Integer', data.get('giveaway_message_id')), winners_selection_date=_parse_api_value('Integer', data.get('winners_selection_date')), winner_count=_parse_api_value('Integer', data.get('winner_count')), winners=_parse_api_value('Array of User', data.get('winners')), additional_chat_count=_parse_api_value('Integer', data.get('additional_chat_count')), prize_star_count=_parse_api_value('Integer', data.get('prize_star_count')), premium_subscription_month_count=_parse_api_value('Integer', data.get('premium_subscription_month_count')), unclaimed_prize_count=_parse_api_value('Integer', data.get('unclaimed_prize_count')), only_new_members=_parse_api_value('True', data.get('only_new_members')), was_refunded=_parse_api_value('True', data.get('was_refunded')), prize_description=_parse_api_value('String', data.get('prize_description')))
