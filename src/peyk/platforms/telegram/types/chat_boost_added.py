from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Dict, List, Mapping, Optional, Sequence, Union

@dataclass
class ChatBoostAdded:
    """This object represents a service message about a user boosting a chat.

Attributes:
    boost_count: Number of boosts added by the user"""
    boost_count: int

    @classmethod
    def from_dict(cls, data: Optional[dict]) -> Optional['ChatBoostAdded']:
        """Provides the from dict operation for the Telegram integration.

Args:
    data: Value used by this operation.

Returns:
    Result produced by the operation."""
        "Executes the from_dict operation.\n        \n        Args:\n            data: Value of the declared parameter type.\n        \n        \n        Returns:\n            The operation result (``Optional['ChatBoostAdded']``).\n        "
        if data is None:
            return None
        return cls(boost_count=data.get('boost_count', 0))
