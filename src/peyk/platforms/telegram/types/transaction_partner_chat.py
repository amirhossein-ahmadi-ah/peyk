from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Dict, List, Mapping, Optional, Sequence, Union

@dataclass
class TransactionPartnerChat:
    """Describes a transaction with a chat.

Attributes:
    type: Type of the transaction partner, always 'chat'
    chat: Information about the chat
    gift: The gift sent to the chat by the bot"""
    type: str = 'chat'
    chat: Optional[Chat] = None

    @classmethod
    def from_dict(cls, data: Optional[dict]) -> Optional['TransactionPartnerChat']:
        """Provides the from dict operation for the Telegram integration.

Args:
    data: Value used by this operation.

Returns:
    Result produced by the operation."""
        "Executes the from_dict operation.\n        \n        Args:\n            data: Value of the declared parameter type.\n        \n        \n        Returns:\n            The operation result (``Optional['TransactionPartnerChat']``).\n        "
        if data is None:
            return None
        return cls(type=data.get('type', 'chat'), chat=Chat.from_dict(data.get('chat', {})))
