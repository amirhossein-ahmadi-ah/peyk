from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Dict, List, Mapping, Optional, Sequence, Union

@dataclass
class ChatBoostSourceGiftCode:
    """The boost was obtained by the creation of Telegram Premium gift codes to boost a chat. Each such code boosts the chat 4 times for the duration of the corresponding Telegram Premium subscription.

Attributes:
    source: Source of the boost, always 'gift_code'
    user: User for which the gift code was created"""
    source: str
    user: User

    @classmethod
    def from_dict(cls, data: Optional[dict]) -> Optional['ChatBoostSourceGiftCode']:
        """Provides the from dict operation for the Telegram integration.

Args:
    data: Value used by this operation.

Returns:
    Result produced by the operation."""
        "Executes the from_dict operation.\n        \n        Args:\n            data: Value of the declared parameter type.\n        \n        \n        Returns:\n            The operation result (``Optional['ChatBoostSourceGiftCode']``).\n        "
        if data is None:
            return None
        return cls(source=_parse_api_value('String', data.get('source')), user=_parse_api_value('User', data.get('user')))
