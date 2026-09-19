from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Dict, List, Mapping, Optional, Sequence, Union

@dataclass
class UserChatBoosts:
    """This object represents a list of boosts added to a chat by a user.

Attributes:
    boosts: The list of boosts added to the chat by the user"""
    boosts: List[ChatBoost]

    @classmethod
    def from_dict(cls, data: Optional[dict]) -> Optional['UserChatBoosts']:
        """Provides the from dict operation for the Telegram integration.

Args:
    data: Value used by this operation.

Returns:
    Result produced by the operation."""
        "Executes the from_dict operation.\n        \n        Args:\n            data: Value of the declared parameter type.\n        \n        \n        Returns:\n            The operation result (``Optional['UserChatBoosts']``).\n        "
        if data is None:
            return None
        return cls(boosts=_parse_api_value('Array of ChatBoost', data.get('boosts')))
