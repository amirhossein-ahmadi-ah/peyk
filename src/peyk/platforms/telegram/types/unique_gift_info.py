from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Dict, List, Mapping, Optional, Sequence, Union

@dataclass
class UniqueGiftInfo:
    """Describes a service message about a unique gift that was sent or received.

Attributes:
    gift: Information about the gift
    origin: Origin of the gift. Currently, either 'upgrade' for gifts upgraded from regular gifts, 'transfer' for gifts transferred from other users or channels, 'resale' for gifts bought from other users, 'gifted_upgrade' for upgrades purchased after the gift was sent, or 'offer' for gifts bought or sold through gift purchase offers.
    last_resale_currency: For gifts bought from other users, the currency in which the payment for the gift was done. Currently, one of 'XTR' for Telegram Stars or 'TON' for TON grams.
    last_resale_amount: For gifts bought from other users, the price paid for the gift in either Telegram Stars or nanograms
    owned_gift_id: Unique identifier of the received gift for the bot; only present for gifts received on behalf of business accounts
    transfer_star_count: Number of Telegram Stars that must be paid to transfer the gift; omitted if the bot cannot transfer the gift
    next_transfer_date: Point in time (Unix timestamp) when the gift can be transferred. If it is in the past, then the gift can be transferred now.
    last_resale_star_count: For gifts bought from other users, the price paid for the gift"""
    gift: UniqueGift
    origin: str
    text: Optional[str] = None
    entities: Optional[List[MessageEntity]] = None
    is_private: Optional[bool] = None
    last_resale_currency: Optional[str] = None
    last_resale_amount: Optional[int] = None
    owned_gift_id: Optional[str] = None
    transfer_star_count: Optional[int] = None
    next_transfer_date: Optional[int] = None

    @classmethod
    def from_dict(cls, data: Optional[dict]) -> Optional['UniqueGiftInfo']:
        """Provides the from dict operation for the Telegram integration.

Args:
    data: Value used by this operation.

Returns:
    Result produced by the operation."""
        "Executes the from_dict operation.\n        \n        Args:\n            data: Value of the declared parameter type.\n        \n        \n        Returns:\n            The operation result (``Optional['UniqueGiftInfo']``).\n        "
        if data is None:
            return None
        return cls(gift=_parse_api_value('UniqueGift', data.get('gift')), origin=_parse_api_value('String', data.get('origin')), text=_parse_api_value('String', data.get('text')), entities=_parse_api_value('Array of MessageEntity', data.get('entities')), is_private=_parse_api_value('True', data.get('is_private')), last_resale_currency=_parse_api_value('String', data.get('last_resale_currency')), last_resale_amount=_parse_api_value('Integer', data.get('last_resale_amount')), owned_gift_id=_parse_api_value('String', data.get('owned_gift_id')), transfer_star_count=_parse_api_value('Integer', data.get('transfer_star_count')), next_transfer_date=_parse_api_value('Integer', data.get('next_transfer_date')))
