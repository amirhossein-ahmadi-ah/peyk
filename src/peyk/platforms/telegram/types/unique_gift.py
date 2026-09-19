from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Dict, List, Mapping, Optional, Sequence, Union

@dataclass
class UniqueGift:
    """This object describes a unique gift that was upgraded from a regular gift.

Attributes:
    gift_id: Identifier of the regular gift from which the gift was upgraded
    base_name: Human-readable name of the regular gift from which this unique gift was upgraded
    name: Unique name of the gift. This name can be used in https://t.me/nft/... links and story areas.
    number: Unique number of the upgraded gift among gifts upgraded from the same regular gift
    model: Model of the gift
    symbol: Symbol of the gift
    backdrop: Backdrop of the gift
    is_premium: True, if the original regular gift was exclusively purchaseable by Telegram Premium subscribers
    is_burned: True, if the gift was used to craft another gift and isn't available anymore
    is_from_blockchain: True, if the gift is assigned from the TON blockchain and can't be resold or transferred in Telegram
    colors: The color scheme that can be used by the gift's owner for the chat's name, replies to messages and link previews; for business account gifts and gifts that are currently on sale only
    publisher_chat: Information about the chat that published the gift"""
    gift_id: str
    base_name: str
    name: str
    number: int
    model: UniqueGiftModel
    symbol: UniqueGiftSymbol
    backdrop: UniqueGiftBackdrop
    is_premium: Optional[bool] = None
    is_burned: Optional[bool] = None
    is_from_blockchain: Optional[bool] = None
    colors: Optional[UniqueGiftColors] = None
    publisher_chat: Optional[Chat] = None

    @classmethod
    def from_dict(cls, data: Optional[dict]) -> Optional['UniqueGift']:
        """Provides the from dict operation for the Telegram integration.

Args:
    data: Value used by this operation.

Returns:
    Result produced by the operation."""
        "Executes the from_dict operation.\n        \n        Args:\n            data: Value of the declared parameter type.\n        \n        \n        Returns:\n            The operation result (``Optional['UniqueGift']``).\n        "
        if data is None:
            return None
        return cls(gift_id=_parse_api_value('String', data.get('gift_id')), base_name=_parse_api_value('String', data.get('base_name')), name=_parse_api_value('String', data.get('name')), number=_parse_api_value('Integer', data.get('number')), model=_parse_api_value('UniqueGiftModel', data.get('model')), symbol=_parse_api_value('UniqueGiftSymbol', data.get('symbol')), backdrop=_parse_api_value('UniqueGiftBackdrop', data.get('backdrop')), is_premium=_parse_api_value('True', data.get('is_premium')), is_burned=_parse_api_value('True', data.get('is_burned')), is_from_blockchain=_parse_api_value('True', data.get('is_from_blockchain')), colors=_parse_api_value('UniqueGiftColors', data.get('colors')), publisher_chat=_parse_api_value('Chat', data.get('publisher_chat')))
