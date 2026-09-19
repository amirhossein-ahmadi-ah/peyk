from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Dict, List, Mapping, Optional, Sequence, Union

@dataclass
class ChatBackground:
    """This object represents a chat background.

Attributes:
    type: Type of the background"""
    type: Optional[BackgroundType] = None

    @classmethod
    def from_dict(cls, data: Optional[dict]) -> Optional['ChatBackground']:
        """Provides the from dict operation for the Telegram integration.

Args:
    data: Value used by this operation.

Returns:
    Result produced by the operation."""
        "Executes the from_dict operation.\n        \n        Args:\n            data: Value of the declared parameter type.\n        \n        \n        Returns:\n            The operation result (``Optional['ChatBackground']``).\n        "
        if data is None:
            return None
        return cls(type=parse_background_type(data.get('type')))
