from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Dict, List, Mapping, Optional, Sequence, Union

@dataclass
class ReactionTypeCustomEmoji:
    """The reaction is based on a custom emoji.

Attributes:
    type: Type of the reaction, always 'custom_emoji'
    custom_emoji_id: Custom emoji identifier"""
    type: str = 'custom_emoji'
    custom_emoji_id: str = ''

    @classmethod
    def from_dict(cls, data: Optional[dict]) -> Optional['ReactionTypeCustomEmoji']:
        """Provides the from dict operation for the Telegram integration.

Args:
    data: Value used by this operation.

Returns:
    Result produced by the operation."""
        "Executes the from_dict operation.\n        \n        Args:\n            data: Value of the declared parameter type.\n        \n        \n        Returns:\n            The operation result (``Optional['ReactionTypeCustomEmoji']``).\n        "
        if data is None:
            return None
        return cls(type=data.get('type', 'custom_emoji'), custom_emoji_id=data.get('custom_emoji_id', ''))
