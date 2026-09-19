from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Dict, List, Mapping, Optional, Sequence, Union

@dataclass
class OwnedGiftRegular:
    """Describes a regular gift owned by a user or a chat.

Attributes:
    type: Type of the gift, always 'regular'
    gift: Information about the regular gift
    send_date: Date the gift was sent in Unix time
    owned_gift_id: Unique identifier of the gift for the bot; for gifts received on behalf of business accounts only
    sender_user: Sender of the gift if it is a known user
    text: Text of the message that was added to the gift
    entities: Special entities that appear in the text
    is_private: True, if the sender and gift text are shown only to the gift receiver; otherwise, everyone will be able to see them
    is_saved: True, if the gift is displayed on the account's profile page; for gifts received on behalf of business accounts only
    can_be_upgraded: True, if the gift can be upgraded to a unique gift; for gifts received on behalf of business accounts only
    was_refunded: True, if the gift was refunded and isn't available anymore
    convert_star_count: Number of Telegram Stars that can be claimed by the receiver instead of the gift; omitted if the gift cannot be converted to Telegram Stars; for gifts received on behalf of business accounts only
    prepaid_upgrade_star_count: Number of Telegram Stars that were paid for the ability to upgrade the gift
    is_upgrade_separate: True, if the gift's upgrade was purchased after the gift was sent; for gifts received on behalf of business accounts only
    unique_gift_number: Unique number reserved for this gift when upgraded. See the number field in UniqueGift."""
    gift: Gift
    send_date: int
    type: str = 'regular'
    owned_gift_id: Optional[str] = None
    sender_user: Optional[User] = None
    text: Optional[str] = None
    entities: Optional[List[MessageEntity]] = None
    is_private: Optional[bool] = None
    is_saved: Optional[bool] = None
    can_be_upgraded: Optional[bool] = None
    was_refunded: Optional[bool] = None
    convert_star_count: Optional[int] = None
    prepaid_upgrade_star_count: Optional[int] = None
    is_upgrade_separate: Optional[bool] = None
    unique_gift_number: Optional[int] = None

    @classmethod
    def from_dict(cls, data: Optional[dict]) -> Optional['OwnedGiftRegular']:
        """Provides the from dict operation for the Telegram integration.

Args:
    data: Value used by this operation.

Returns:
    Result produced by the operation."""
        "Executes the from_dict operation.\n        \n        Args:\n            data: Value of the declared parameter type.\n        \n        \n        Returns:\n            The operation result (``Optional['OwnedGiftRegular']``).\n        "
        if data is None:
            return None
        return cls(gift=_parse_api_value('Gift', data.get('gift')), send_date=_parse_api_value('Integer', data.get('send_date')), type=_parse_api_value('String', data.get('type')), owned_gift_id=_parse_api_value('String', data.get('owned_gift_id')), sender_user=_parse_api_value('User', data.get('sender_user')), text=_parse_api_value('String', data.get('text')), entities=_parse_api_value('Array of MessageEntity', data.get('entities')), is_private=_parse_api_value('True', data.get('is_private')), is_saved=_parse_api_value('True', data.get('is_saved')), can_be_upgraded=_parse_api_value('True', data.get('can_be_upgraded')), was_refunded=_parse_api_value('True', data.get('was_refunded')), convert_star_count=_parse_api_value('Integer', data.get('convert_star_count')), prepaid_upgrade_star_count=_parse_api_value('Integer', data.get('prepaid_upgrade_star_count')), is_upgrade_separate=_parse_api_value('True', data.get('is_upgrade_separate')), unique_gift_number=_parse_api_value('Integer', data.get('unique_gift_number')))
