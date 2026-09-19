from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Dict, List, Mapping, Optional, Sequence, Union

@dataclass
class Giveaway:
    """This object represents a message about a scheduled giveaway.

Attributes:
    chats: The list of chats which the user must join to participate in the giveaway
    winners_selection_date: Point in time (Unix timestamp) when winners of the giveaway will be selected
    winner_count: The number of users which are supposed to be selected as winners of the giveaway
    only_new_members: True, if only users who join the chats after the giveaway started should be eligible to win
    has_public_winners: True, if the list of giveaway winners will be visible to everyone
    prize_description: Description of additional giveaway prize
    country_codes: A list of two-letter ISO 3166-1 alpha-2 country codes indicating the countries from which eligible users for the giveaway must come. If empty, then all users can participate in the giveaway. Users with a phone number that was bought on Fragment can always participate in giveaways.
    prize_star_count: The number of Telegram Stars to be split between giveaway winners; for Telegram Star giveaways only
    premium_subscription_month_count: The number of months the Telegram Premium subscription won from the giveaway will be active for; for Telegram Premium giveaways only"""
    chats: List[Chat]
    winners_selection_date: int
    winner_count: int
    only_new_members: Optional[bool] = None
    has_public_winners: Optional[bool] = None
    prize_description: Optional[str] = None
    country_codes: Optional[List[str]] = None
    prize_star_count: Optional[int] = None
    premium_subscription_month_count: Optional[int] = None

    @classmethod
    def from_dict(cls, data: Optional[dict]) -> Optional['Giveaway']:
        """Provides the from dict operation for the Telegram integration.

Args:
    data: Value used by this operation.

Returns:
    Result produced by the operation."""
        "Executes the from_dict operation.\n        \n        Args:\n            data: Value of the declared parameter type.\n        \n        \n        Returns:\n            The operation result (``Optional['Giveaway']``).\n        "
        if data is None:
            return None
        return cls(chats=_parse_api_value('Array of Chat', data.get('chats')), winners_selection_date=_parse_api_value('Integer', data.get('winners_selection_date')), winner_count=_parse_api_value('Integer', data.get('winner_count')), only_new_members=_parse_api_value('True', data.get('only_new_members')), has_public_winners=_parse_api_value('True', data.get('has_public_winners')), prize_description=_parse_api_value('String', data.get('prize_description')), country_codes=_parse_api_value('Array of String', data.get('country_codes')), prize_star_count=_parse_api_value('Integer', data.get('prize_star_count')), premium_subscription_month_count=_parse_api_value('Integer', data.get('premium_subscription_month_count')))
