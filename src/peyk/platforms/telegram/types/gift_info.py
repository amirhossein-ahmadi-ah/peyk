from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Dict, List, Mapping, Optional, Sequence, Union

@dataclass
class GiftInfo:
    """Describes a service message about a regular gift that was sent or received.

Attributes:
    gift: Information about the gift
    owned_gift_id: Unique identifier of the received gift for the bot; only present for gifts received on behalf of business accounts
    convert_star_count: Number of Telegram Stars that can be claimed by the receiver by converting the gift; omitted if conversion to Telegram Stars is impossible
    prepaid_upgrade_star_count: Number of Telegram Stars that were prepaid for the ability to upgrade the gift
    is_upgrade_separate: True, if the gift's upgrade was purchased after the gift was sent
    can_be_upgraded: True, if the gift can be upgraded to a unique gift
    text: Text of the message that was added to the gift
    entities: Special entities that appear in the text
    is_private: True, if the sender and gift text are shown only to the gift receiver; otherwise, everyone will be able to see them
    unique_gift_number: Unique number reserved for this gift when upgraded. See the number field in UniqueGift."""
    gift: Optional[Gift] = None
    owned_gift_id: Optional[str] = None
    convert_star_count: Optional[int] = None
    upgrade_star_count: Optional[int] = None
    can_be_upgraded: Optional[bool] = None
    is_saved: Optional[bool] = None
    is_pinned: Optional[bool] = None
    is_private: Optional[bool] = None
    is_saved_in_chat: Optional[bool] = None
    can_be_refunded: Optional[bool] = None
    upgraded_gift: Optional[object] = None
    date: Optional[int] = None
    send_date: Optional[int] = None
    last_reservation_date: Optional[int] = None

    @classmethod
    def from_dict(cls, data: Optional[dict]) -> Optional['GiftInfo']:
        """Provides the from dict operation for the Telegram integration.

Args:
    data: Value used by this operation.

Returns:
    Result produced by the operation."""
        "Executes the from_dict operation.\n        \n        Args:\n            data: Value of the declared parameter type.\n        \n        \n        Returns:\n            The operation result (``Optional['GiftInfo']``).\n        "
        if data is None:
            return None
        return cls(gift=Gift.from_dict(data.get('gift')), owned_gift_id=data.get('owned_gift_id'), convert_star_count=data.get('convert_star_count'), upgrade_star_count=data.get('upgrade_star_count'), can_be_upgraded=data.get('can_be_upgraded'), is_saved=data.get('is_saved'), is_pinned=data.get('is_pinned'), is_private=data.get('is_private'), is_saved_in_chat=data.get('is_saved_in_chat'), can_be_refunded=data.get('can_be_refunded'), upgraded_gift=data.get('upgraded_gift'), date=data.get('date'), send_date=data.get('send_date'), last_reservation_date=data.get('last_reservation_date'))
