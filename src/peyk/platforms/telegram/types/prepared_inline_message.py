from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Dict, List, Mapping, Optional, Sequence, Union

@dataclass
class PreparedInlineMessage:
    """Describes an inline message to be sent by a user of a Mini App.

Attributes:
    id: Unique identifier of the prepared message
    expiration_date: Expiration date of the prepared message, in Unix time. Expired prepared messages can no longer be used."""
    id: str = ''
    expiration_date: int = 0

    @classmethod
    def from_dict(cls, data: Optional[dict]) -> Optional['PreparedInlineMessage']:
        """Provides the from dict operation for the Telegram integration.

Args:
    data: Value used by this operation.

Returns:
    Result produced by the operation."""
        "Executes the from_dict operation.\n        \n        Args:\n            data: Value of the declared parameter type.\n        \n        \n        Returns:\n            The operation result (``Optional['PreparedInlineMessage']``).\n        "
        if data is None:
            return None
        return cls(id=data.get('id', ''), expiration_date=data.get('expiration_date', 0))
