from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Dict, List, Mapping, Optional, Sequence, Union

@dataclass
class KeyboardButtonRequestManagedBot:
    """This object defines the parameters for the creation of a managed bot. Information about the created bot will be shared with the bot using the update managed_bot and a Message with the field managed_bot_created.

Attributes:
    request_id: Signed 32-bit identifier of the request. Must be unique within the message.
    suggested_name: Suggested name for the bot
    suggested_username: Suggested username for the bot"""
    request_id: int = 0
    suggested_name: Optional[str] = None
    suggested_username: Optional[str] = None

    @classmethod
    def from_dict(cls, data: Optional[dict]) -> Optional['KeyboardButtonRequestManagedBot']:
        """Provides the from dict operation for the Telegram integration.

Args:
    data: Value used by this operation.

Returns:
    Result produced by the operation."""
        "Executes the from_dict operation.\n        \n        Args:\n            data: Value of the declared parameter type.\n        \n        \n        Returns:\n            The operation result (``Optional['KeyboardButtonRequestManagedBot']``).\n        "
        if data is None:
            return None
        return cls(request_id=data.get('request_id', 0), suggested_name=data.get('suggested_name'), suggested_username=data.get('suggested_username'))

    def to_dict(self) -> Dict[str, object]:
        """Provides the to dict operation for the Telegram integration.

Returns:
    Result produced by the operation."""
        'Executes the to_dict operation.\n        \n        Returns:\n            The operation result (``Dict[str, object]``).\n        '
        body: Dict[str, object] = {'request_id': self.request_id}
        if self.suggested_name is not None:
            body['suggested_name'] = self.suggested_name
        if self.suggested_username is not None:
            body['suggested_username'] = self.suggested_username
        return body
