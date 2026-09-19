from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Dict, List, Mapping, Optional, Sequence, Union

@dataclass
class DirectMessagesTopic:
    """Describes a topic of a direct messages chat.

Attributes:
    topic_id: Unique identifier of the topic. This number may have more than 32 significant bits and some programming languages may have difficulty/silent defects in interpreting it. But it has at most 52 significant bits, so a 64-bit integer or double-precision float type are safe for storing this identifier.
    user: Information about the user that created the topic. Currently, it is always present."""
    topic_id: Optional[int] = None
    user: Optional[User] = None

    @classmethod
    def from_dict(cls, data: Optional[dict]) -> Optional['DirectMessagesTopic']:
        """Provides the from dict operation for the Telegram integration.

Args:
    data: Value used by this operation.

Returns:
    Result produced by the operation."""
        "Executes the from_dict operation.\n        \n        Args:\n            data: Value of the declared parameter type.\n        \n        \n        Returns:\n            The operation result (``Optional['DirectMessagesTopic']``).\n        "
        if data is None:
            return None
        return cls(topic_id=data.get('topic_id'), user=User.from_dict(data.get('user')))
