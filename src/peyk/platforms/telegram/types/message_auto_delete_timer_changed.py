from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Dict, List, Mapping, Optional, Sequence, Union

@dataclass
class MessageAutoDeleteTimerChanged:
    """This object represents a service message about a change in auto-delete timer settings.

Attributes:
    message_auto_delete_time: New auto-delete time for messages in the chat; in seconds"""
    message_auto_delete_time: int = 0

    @classmethod
    def from_dict(cls, data: Optional[dict]) -> Optional['MessageAutoDeleteTimerChanged']:
        """Provides the from dict operation for the Telegram integration.

Args:
    data: Value used by this operation.

Returns:
    Result produced by the operation."""
        "Executes the from_dict operation.\n        \n        Args:\n            data: Value of the declared parameter type.\n        \n        \n        Returns:\n            The operation result (``Optional['MessageAutoDeleteTimerChanged']``).\n        "
        if data is None:
            return None
        return cls(message_auto_delete_time=data.get('message_auto_delete_time', 0))
