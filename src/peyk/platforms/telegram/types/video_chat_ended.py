from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Dict, List, Mapping, Optional, Sequence, Union

@dataclass
class VideoChatEnded:
    """This object represents a service message about a video chat ended in the chat.

Attributes:
    duration: Video chat duration in seconds"""
    duration: int = 0

    @classmethod
    def from_dict(cls, data: Optional[dict]) -> Optional['VideoChatEnded']:
        """Provides the from dict operation for the Telegram integration.

Args:
    data: Value used by this operation.

Returns:
    Result produced by the operation."""
        "Executes the from_dict operation.\n        \n        Args:\n            data: Value of the declared parameter type.\n        \n        \n        Returns:\n            The operation result (``Optional['VideoChatEnded']``).\n        "
        if data is None:
            return None
        return cls(duration=data.get('duration', 0))
