from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Dict, List, Mapping, Optional, Sequence, Union

@dataclass
class ChatOwnerLeft:
    """Describes a service message about the chat owner leaving the chat.

Attributes:
    new_owner: The user who will become the new owner of the chat if the previous owner does not return to the chat"""
    user: Optional[User] = None

    @classmethod
    def from_dict(cls, data: Optional[dict]) -> Optional['ChatOwnerLeft']:
        """Provides the from dict operation for the Telegram integration.

Args:
    data: Value used by this operation.

Returns:
    Result produced by the operation."""
        "Executes the from_dict operation.\n        \n        Args:\n            data: Value of the declared parameter type.\n        \n        \n        Returns:\n            The operation result (``Optional['ChatOwnerLeft']``).\n        "
        if data is None:
            return None
        return cls(user=User.from_dict(data.get('user')))
