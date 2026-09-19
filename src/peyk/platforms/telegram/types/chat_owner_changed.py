from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Dict, List, Mapping, Optional, Sequence, Union

@dataclass
class ChatOwnerChanged:
    """Describes a service message about an ownership change in the chat.

Attributes:
    new_owner: The new owner of the chat"""
    from_user: Optional[User] = None
    to_user: Optional[User] = None

    @classmethod
    def from_dict(cls, data: Optional[dict]) -> Optional['ChatOwnerChanged']:
        """Provides the from dict operation for the Telegram integration.

Args:
    data: Value used by this operation.

Returns:
    Result produced by the operation."""
        "Executes the from_dict operation.\n        \n        Args:\n            data: Value of the declared parameter type.\n        \n        \n        Returns:\n            The operation result (``Optional['ChatOwnerChanged']``).\n        "
        if data is None:
            return None
        return cls(from_user=User.from_dict(data.get('from')), to_user=User.from_dict(data.get('to')))
