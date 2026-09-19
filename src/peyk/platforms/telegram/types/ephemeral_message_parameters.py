from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Dict, List, Mapping, Optional, Sequence, Union

@dataclass
class EphemeralMessageParameters:
    """Ephemeral message parameters."""
    receiver_user_id: Optional[int] = None
    callback_query_id: Optional[str] = None
    replace_callback_query_message: Optional[bool] = None

    @classmethod
    def from_dict(cls, data: Optional[dict]) -> Optional['EphemeralMessageParameters']:
        """Provides the from dict operation for the Telegram integration.

Args:
    data: Value used by this operation.

Returns:
    Result produced by the operation."""
        "Executes the from_dict operation.\n        \n        Args:\n            data: Value of the declared parameter type.\n        \n        \n        Returns:\n            The operation result (``Optional['EphemeralMessageParameters']``).\n        "
        if data is None:
            return None
        return cls(receiver_user_id=data.get('receiver_user_id'), callback_query_id=data.get('callback_query_id'), replace_callback_query_message=data.get('replace_callback_query_message'))
