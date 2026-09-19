from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Dict, List, Mapping, Optional, Sequence, Union

@dataclass
class ChatBoostSourcePremium:
    """The boost was obtained by subscribing to Telegram Premium or by gifting a Telegram Premium subscription to another user.

Attributes:
    source: Source of the boost, always 'premium'
    user: User that boosted the chat"""
    source: str
    user: User

    @classmethod
    def from_dict(cls, data: Optional[dict]) -> Optional['ChatBoostSourcePremium']:
        """Provides the from dict operation for the Telegram integration.

Args:
    data: Value used by this operation.

Returns:
    Result produced by the operation."""
        "Executes the from_dict operation.\n        \n        Args:\n            data: Value of the declared parameter type.\n        \n        \n        Returns:\n            The operation result (``Optional['ChatBoostSourcePremium']``).\n        "
        if data is None:
            return None
        return cls(source=_parse_api_value('String', data.get('source')), user=_parse_api_value('User', data.get('user')))
