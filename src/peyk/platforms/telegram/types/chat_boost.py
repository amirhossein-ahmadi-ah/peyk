from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Dict, List, Mapping, Optional, Sequence, Union

@dataclass
class ChatBoost:
    """This object contains information about a chat boost.

Attributes:
    boost_id: Unique identifier of the boost
    add_date: Point in time (Unix timestamp) when the chat was boosted
    expiration_date: Point in time (Unix timestamp) when the boost will automatically expire, unless the booster's Telegram Premium subscription is prolonged
    source: Source of the added boost"""
    boost_id: str
    add_date: int
    expiration_date: int
    source: ChatBoostSource

    @classmethod
    def from_dict(cls, data: Optional[dict]) -> Optional['ChatBoost']:
        """Provides the from dict operation for the Telegram integration.

Args:
    data: Value used by this operation.

Returns:
    Result produced by the operation."""
        "Executes the from_dict operation.\n        \n        Args:\n            data: Value of the declared parameter type.\n        \n        \n        Returns:\n            The operation result (``Optional['ChatBoost']``).\n        "
        if data is None:
            return None
        return cls(boost_id=_parse_api_value('String', data.get('boost_id')), add_date=_parse_api_value('Integer', data.get('add_date')), expiration_date=_parse_api_value('Integer', data.get('expiration_date')), source=_parse_api_value('ChatBoostSource', data.get('source')))
