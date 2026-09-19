from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Dict, List, Mapping, Optional, Sequence, Union

@dataclass
class AcceptedGiftTypes:
    """This object describes the types of gifts that can be gifted to a user or a chat.

Attributes:
    unlimited_gifts: True, if unlimited regular gifts are accepted
    limited_gifts: True, if limited regular gifts are accepted
    unique_gifts: True, if unique gifts or gifts that can be upgraded to unique for free are accepted
    premium_subscription: True, if a Telegram Premium subscription is accepted
    gifts_from_channels: True, if transfers of unique gifts from channels are accepted"""
    unlimited_gifts: bool
    limited_gifts: bool
    unique_gifts: bool
    premium_subscription: bool
    gifts_from_channels: bool

    @classmethod
    def from_dict(cls, data: Optional[dict]) -> Optional['AcceptedGiftTypes']:
        """Provides the from dict operation for the Telegram integration.

Args:
    data: Value used by this operation.

Returns:
    Result produced by the operation."""
        "Executes the from_dict operation.\n        \n        Args:\n            data: Value of the declared parameter type.\n        \n        \n        Returns:\n            The operation result (``Optional['AcceptedGiftTypes']``).\n        "
        if data is None:
            return None
        return cls(unlimited_gifts=_parse_api_value('Boolean', data.get('unlimited_gifts')), limited_gifts=_parse_api_value('Boolean', data.get('limited_gifts')), unique_gifts=_parse_api_value('Boolean', data.get('unique_gifts')), premium_subscription=_parse_api_value('Boolean', data.get('premium_subscription')), gifts_from_channels=_parse_api_value('Boolean', data.get('gifts_from_channels')))
