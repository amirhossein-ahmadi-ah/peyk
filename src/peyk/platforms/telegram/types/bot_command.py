from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Dict, List, Mapping, Optional, Sequence, Union

@dataclass
class BotCommand:
    """This object represents a bot command.

Attributes:
    command: Text of the command; 1-32 characters. Can contain only lowercase English letters, digits and underscores.
    description: Description of the command; 1-256 characters
    is_ephemeral: True, if the command sends an ephemeral message, which can be seen only by the sender of the message and the bot"""
    command: str = ''
    description: str = ''
    is_ephemeral: Optional[bool] = None

    @classmethod
    def from_dict(cls, data: Optional[dict]) -> Optional['BotCommand']:
        """Provides the from dict operation for the Telegram integration.

Args:
    data: Value used by this operation.

Returns:
    Result produced by the operation."""
        "Executes the from_dict operation.\n        \n        Args:\n            data: Value of the declared parameter type.\n        \n        \n        Returns:\n            The operation result (``Optional['BotCommand']``).\n        "
        if data is None:
            return None
        return cls(command=data.get('command', ''), description=data.get('description', ''), is_ephemeral=data.get('is_ephemeral'))

    def to_dict(self) -> Dict[str, object]:
        """Provides the to dict operation for the Telegram integration.

Returns:
    Result produced by the operation."""
        'Executes the to_dict operation.\n        \n        Returns:\n            The operation result (``Dict[str, object]``).\n        '
        body: Dict[str, object] = {'command': self.command, 'description': self.description}
        if self.is_ephemeral is not None:
            body['is_ephemeral'] = self.is_ephemeral
        return body
