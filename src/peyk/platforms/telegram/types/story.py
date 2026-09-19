from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Dict, List, Mapping, Optional, Sequence, Union

@dataclass
class Story:
    """This object represents a story.

Attributes:
    chat: Chat that posted the story
    id: Unique identifier for the story in the chat"""
    chat: Optional[Chat] = None
    id: Optional[int] = None

    @classmethod
    def from_dict(cls, data: Optional[dict]) -> Optional['Story']:
        """Provides the from dict operation for the Telegram integration.

Args:
    data: Value used by this operation.

Returns:
    Result produced by the operation."""
        "Executes the from_dict operation.\n        \n        Args:\n            data: Value of the declared parameter type.\n        \n        \n        Returns:\n            The operation result (``Optional['Story']``).\n        "
        if data is None:
            return None
        return cls(chat=Chat.from_dict(data.get('chat')), id=data.get('id'))
