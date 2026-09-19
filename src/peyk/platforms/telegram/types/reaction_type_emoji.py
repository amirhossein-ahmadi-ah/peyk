from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Dict, List, Mapping, Optional, Sequence, Union

@dataclass
class ReactionTypeEmoji:
    """The reaction is based on an emoji.

Attributes:
    type: Type of the reaction, always 'emoji'
    emoji: Reaction emoji. Currently, it can be one of "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", ""."""
    type: str = 'emoji'
    emoji: str = ''

    @classmethod
    def from_dict(cls, data: Optional[dict]) -> Optional['ReactionTypeEmoji']:
        """Provides the from dict operation for the Telegram integration.

Args:
    data: Value used by this operation.

Returns:
    Result produced by the operation."""
        "Executes the from_dict operation.\n        \n        Args:\n            data: Value of the declared parameter type.\n        \n        \n        Returns:\n            The operation result (``Optional['ReactionTypeEmoji']``).\n        "
        if data is None:
            return None
        return cls(type=data.get('type', 'emoji'), emoji=data.get('emoji', ''))
