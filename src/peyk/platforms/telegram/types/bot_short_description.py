from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Dict, List, Mapping, Optional, Sequence, Union

@dataclass
class BotShortDescription:
    """This object represents the bot's short description.

Attributes:
    short_description: The bot's short description"""
    short_description: str = ''

    @classmethod
    def from_dict(cls, data: Optional[dict]) -> Optional['BotShortDescription']:
        """Provides the from dict operation for the Telegram integration.

Args:
    data: Value used by this operation.

Returns:
    Result produced by the operation."""
        "Executes the from_dict operation.\n        \n        Args:\n            data: Value of the declared parameter type.\n        \n        \n        Returns:\n            The operation result (``Optional['BotShortDescription']``).\n        "
        if data is None:
            return None
        return cls(short_description=data.get('short_description', ''))
