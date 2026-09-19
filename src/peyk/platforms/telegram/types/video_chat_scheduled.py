from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Dict, List, Mapping, Optional, Sequence, Union

@dataclass
class VideoChatScheduled:
    """This object represents a service message about a video chat scheduled in the chat.

Attributes:
    start_date: Point in time (Unix timestamp) when the video chat is supposed to be started by a chat administrator"""
    start_date: int = 0

    @classmethod
    def from_dict(cls, data: Optional[dict]) -> Optional['VideoChatScheduled']:
        """Provides the from dict operation for the Telegram integration.

Args:
    data: Value used by this operation.

Returns:
    Result produced by the operation."""
        "Executes the from_dict operation.\n        \n        Args:\n            data: Value of the declared parameter type.\n        \n        \n        Returns:\n            The operation result (``Optional['VideoChatScheduled']``).\n        "
        if data is None:
            return None
        return cls(start_date=data.get('start_date', 0))
