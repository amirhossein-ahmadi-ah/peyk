from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Dict, List, Mapping, Optional, Sequence, Union

@dataclass
class Gift:
    """This object represents a gift that can be sent by the bot.

Attributes:
    id: Unique identifier of the gift
    sticker: The sticker that represents the gift
    star_count: The number of Telegram Stars that must be paid to send the sticker
    upgrade_star_count: The number of Telegram Stars that must be paid to upgrade the gift to a unique one
    is_premium: True, if the gift can only be purchased by Telegram Premium subscribers
    has_colors: True, if the gift can be used (after being upgraded) to customize a user's appearance
    total_count: The total number of gifts of this type that can be sent by all users; for limited gifts only
    remaining_count: The number of remaining gifts of this type that can be sent by all users; for limited gifts only
    personal_total_count: The total number of gifts of this type that can be sent by the bot; for limited gifts only
    personal_remaining_count: The number of remaining gifts of this type that can be sent by the bot; for limited gifts only
    background: Background of the gift
    unique_gift_variant_count: The total number of different unique gifts that can be obtained by upgrading the gift
    publisher_chat: Information about the chat that published the gift"""
    id: str
    sticker: Sticker
    star_count: int
    upgrade_star_count: Optional[int] = None
    is_premium: Optional[bool] = None
    has_colors: Optional[bool] = None
    total_count: Optional[int] = None
    remaining_count: Optional[int] = None
    personal_total_count: Optional[int] = None
    personal_remaining_count: Optional[int] = None
    background: Optional[GiftBackground] = None
    unique_gift_variant_count: Optional[int] = None
    publisher_chat: Optional[Chat] = None

    @classmethod
    def from_dict(cls, data: Optional[dict]) -> Optional['Gift']:
        """Provides the from dict operation for the Telegram integration.

Args:
    data: Value used by this operation.

Returns:
    Result produced by the operation."""
        "Executes the from_dict operation.\n        \n        Args:\n            data: Value of the declared parameter type.\n        \n        \n        Returns:\n            The operation result (``Optional['Gift']``).\n        "
        if data is None:
            return None
        return cls(id=_parse_api_value('String', data.get('id')), sticker=_parse_api_value('Sticker', data.get('sticker')), star_count=_parse_api_value('Integer', data.get('star_count')), upgrade_star_count=_parse_api_value('Integer', data.get('upgrade_star_count')), is_premium=_parse_api_value('True', data.get('is_premium')), has_colors=_parse_api_value('True', data.get('has_colors')), total_count=_parse_api_value('Integer', data.get('total_count')), remaining_count=_parse_api_value('Integer', data.get('remaining_count')), personal_total_count=_parse_api_value('Integer', data.get('personal_total_count')), personal_remaining_count=_parse_api_value('Integer', data.get('personal_remaining_count')), background=_parse_api_value('GiftBackground', data.get('background')), unique_gift_variant_count=_parse_api_value('Integer', data.get('unique_gift_variant_count')), publisher_chat=_parse_api_value('Chat', data.get('publisher_chat')))
