from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Dict, List, Mapping, Optional, Sequence, Union

@dataclass
class BotDescription:
    """This object represents the bot's description.

Attributes:
    description: The bot's description"""
    description: str = ''

    @classmethod
    def from_dict(cls, data: Optional[dict]) -> Optional['BotDescription']:
        """Provides the from dict operation for the Telegram integration.

Args:
    data: Value used by this operation.

Returns:
    Result produced by the operation."""
        "Executes the from_dict operation.\n        \n        Args:\n            data: Value of the declared parameter type.\n        \n        \n        Returns:\n            The operation result (``Optional['BotDescription']``).\n        "
        if data is None:
            return None
        return cls(description=data.get('description', ''))
