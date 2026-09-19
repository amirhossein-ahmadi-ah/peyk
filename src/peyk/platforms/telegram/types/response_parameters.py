from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Dict, List, Mapping, Optional, Sequence, Union

@dataclass
class ResponseParameters:
    """Describes why a request was unsuccessful.

Attributes:
    migrate_to_chat_id: The group has been migrated to a supergroup with the specified identifier. This number may have more than 32 significant bits and some programming languages may have difficulty/silent defects in interpreting it. But it has at most 52 significant bits, so a signed 64-bit integer or double-precision float type are safe for storing this identifier.
    retry_after: In case of exceeding flood control, the number of seconds left to wait before the request can be repeated"""
    migrate_to_chat_id: Optional[int] = None
    retry_after: Optional[int] = None

    @classmethod
    def from_dict(cls, data: Optional[dict]) -> Optional['ResponseParameters']:
        """Provides the from dict operation for the Telegram integration.

Args:
    data: Value used by this operation.

Returns:
    Result produced by the operation."""
        "Executes the from_dict operation.\n        \n        Args:\n            data: Value of the declared parameter type.\n        \n        \n        Returns:\n            The operation result (``Optional['ResponseParameters']``).\n        "
        if data is None:
            return None
        return cls(migrate_to_chat_id=data.get('migrate_to_chat_id'), retry_after=data.get('retry_after'))
