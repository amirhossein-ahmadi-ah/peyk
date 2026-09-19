from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Dict, List, Mapping, Optional, Sequence, Union

@dataclass
class ChatBoostRemoved:
    """This object represents a boost removed from a chat.

Attributes:
    chat: Chat which was boosted
    boost_id: Unique identifier of the boost
    remove_date: Point in time (Unix timestamp) when the boost was removed
    source: Source of the removed boost"""
    chat: Chat
    boost_id: str
    remove_date: int
    source: ChatBoostSource

    @classmethod
    def from_dict(cls, data: Optional[dict]) -> Optional['ChatBoostRemoved']:
        """Provides the from dict operation for the Telegram integration.

Args:
    data: Value used by this operation.

Returns:
    Result produced by the operation."""
        "Executes the from_dict operation.\n        \n        Args:\n            data: Value of the declared parameter type.\n        \n        \n        Returns:\n            The operation result (``Optional['ChatBoostRemoved']``).\n        "
        if data is None:
            return None
        return cls(chat=_parse_api_value('Chat', data.get('chat')), boost_id=_parse_api_value('String', data.get('boost_id')), remove_date=_parse_api_value('Integer', data.get('remove_date')), source=_parse_api_value('ChatBoostSource', data.get('source')))
