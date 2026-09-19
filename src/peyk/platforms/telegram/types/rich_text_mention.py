from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Dict, List, Mapping, Optional, Sequence, Union

@dataclass
class RichTextMention:
    """A mention by a username.

Attributes:
    type: Type of the rich text, always 'mention'
    text: The text
    username: The username"""
    text: str = ''
    user_id: int = 0
    type: str = 'mention'

    @classmethod
    def from_dict(cls, data):
        """Provides the from dict operation for the Telegram integration.

Args:
    data: Value used by this operation."""
        'Executes the from_dict operation.\n        \n        Args:\n            data: Value of the declared parameter type.\n        \n        \n        Returns:\n            The operation result (``Any``).\n        '
        return cls(text=data.get('text', ''), user_id=data.get('user_id', 0)) if data else None
