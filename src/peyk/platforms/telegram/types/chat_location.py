from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Dict, List, Mapping, Optional, Sequence, Union

@dataclass
class ChatLocation:
    """Represents a location to which a chat is connected.

Attributes:
    location: The location to which the supergroup is connected. Can't be a live location.
    address: Location address; 1-64 characters, as defined by the chat owner"""
    location: Optional[Location] = None
    address: str = ''

    @classmethod
    def from_dict(cls, data: Optional[dict]) -> Optional['ChatLocation']:
        """Provides the from dict operation for the Telegram integration.

Args:
    data: Value used by this operation.

Returns:
    Result produced by the operation."""
        "Executes the from_dict operation.\n        \n        Args:\n            data: Value of the declared parameter type.\n        \n        \n        Returns:\n            The operation result (``Optional['ChatLocation']``).\n        "
        if data is None:
            return None
        return cls(location=Location.from_dict(data.get('location')), address=data.get('address', ''))
