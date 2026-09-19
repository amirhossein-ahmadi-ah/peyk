from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Dict, List, Mapping, Optional, Sequence, Union

@dataclass
class BotName:
    """This object represents the bot's name.

Attributes:
    name: The bot's name"""
    name: str = ''

    @classmethod
    def from_dict(cls, data: Optional[dict]) -> Optional['BotName']:
        """Provides the from dict operation for the Telegram integration.

Args:
    data: Value used by this operation.

Returns:
    Result produced by the operation."""
        "Executes the from_dict operation.\n        \n        Args:\n            data: Value of the declared parameter type.\n        \n        \n        Returns:\n            The operation result (``Optional['BotName']``).\n        "
        if data is None:
            return None
        return cls(name=data.get('name', ''))
