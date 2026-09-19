from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Dict, List, Mapping, Optional, Sequence, Union

@dataclass
class ChatBoostUpdated:
    """This object represents a boost added to a chat or changed.

Attributes:
    chat: Chat which was boosted
    boost: Information about the chat boost"""
    chat: Chat
    boost: ChatBoost

    @classmethod
    def from_dict(cls, data: Optional[dict]) -> Optional['ChatBoostUpdated']:
        """Provides the from dict operation for the Telegram integration.

Args:
    data: Value used by this operation.

Returns:
    Result produced by the operation."""
        "Executes the from_dict operation.\n        \n        Args:\n            data: Value of the declared parameter type.\n        \n        \n        Returns:\n            The operation result (``Optional['ChatBoostUpdated']``).\n        "
        if data is None:
            return None
        return cls(chat=_parse_api_value('Chat', data.get('chat')), boost=_parse_api_value('ChatBoost', data.get('boost')))
