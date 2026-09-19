from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Dict, List, Mapping, Optional, Sequence, Union

@dataclass
class MessageGenerationStopped:
    """MessageGenerationStopped Telegram Bot API type."""
    chat_id: int = 0
    message_id: Optional[int] = None
    message_thread_id: Optional[int] = None
    draft_id: Optional[int] = None

    @classmethod
    def from_dict(cls, data: Optional[dict]) -> Optional['MessageGenerationStopped']:
        """Provides the from dict operation for the Telegram integration.

Args:
    data: Value used by this operation.

Returns:
    Result produced by the operation."""
        "Executes the from_dict operation.\n        \n        Args:\n            data: Value of the declared parameter type.\n        \n        \n        Returns:\n            The operation result (``Optional['MessageGenerationStopped']``).\n        "
        if data is None:
            return None
        return cls(chat_id=data.get('chat_id', 0), message_id=data.get('message_id'), message_thread_id=data.get('message_thread_id'), draft_id=data.get('draft_id'))
