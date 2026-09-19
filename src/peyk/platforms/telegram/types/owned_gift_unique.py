from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Dict, List, Mapping, Optional, Sequence, Union

@dataclass
class OwnedGiftUnique:
    """Describes a unique gift received and owned by a user or a chat.

Attributes:
    type: Type of the gift, always 'unique'
    gift: Information about the unique gift
    send_date: Date the gift was sent in Unix time
    owned_gift_id: Unique identifier of the received gift for the bot; for gifts received on behalf of business accounts only
    sender_user: Sender of the gift if it is a known user
    is_saved: True, if the gift is displayed on the account's profile page; for gifts received on behalf of business accounts only
    can_be_transferred: True, if the gift can be transferred to another owner; for gifts received on behalf of business accounts only
    transfer_star_count: Number of Telegram Stars that must be paid to transfer the gift; omitted if the bot cannot transfer the gift
    next_transfer_date: Point in time (Unix timestamp) when the gift can be transferred. If it is in the past, then the gift can be transferred now."""
    gift: UniqueGift
    send_date: int
    type: str = 'unique'
    owned_gift_id: Optional[str] = None
    sender_user: Optional[User] = None
    is_saved: Optional[bool] = None
    can_be_transferred: Optional[bool] = None
    transfer_star_count: Optional[int] = None
    next_transfer_date: Optional[int] = None

    @classmethod
    def from_dict(cls, data: Optional[dict]) -> Optional['OwnedGiftUnique']:
        """Provides the from dict operation for the Telegram integration.

Args:
    data: Value used by this operation.

Returns:
    Result produced by the operation."""
        "Executes the from_dict operation.\n        \n        Args:\n            data: Value of the declared parameter type.\n        \n        \n        Returns:\n            The operation result (``Optional['OwnedGiftUnique']``).\n        "
        if data is None:
            return None
        return cls(gift=_parse_api_value('UniqueGift', data.get('gift')), send_date=_parse_api_value('Integer', data.get('send_date')), type=_parse_api_value('String', data.get('type')), owned_gift_id=_parse_api_value('String', data.get('owned_gift_id')), sender_user=_parse_api_value('User', data.get('sender_user')), is_saved=_parse_api_value('True', data.get('is_saved')), can_be_transferred=_parse_api_value('True', data.get('can_be_transferred')), transfer_star_count=_parse_api_value('Integer', data.get('transfer_star_count')), next_transfer_date=_parse_api_value('Integer', data.get('next_transfer_date')))
