from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Dict, List, Mapping, Optional, Sequence, Union

@dataclass
class RichTextTextMention:
    """A mention of a Telegram user by their identifier.

Attributes:
    type: Type of the rich text, always 'text_mention'
    text: The text
    user: The mentioned user"""
    text: str = ''
    user: Optional[User] = None
    type: str = 'text_mention'

    @classmethod
    def from_dict(cls, data):
        """Provides the from dict operation for the Telegram integration.

Args:
    data: Value used by this operation."""
        'Executes the from_dict operation.\n        \n        Args:\n            data: Value of the declared parameter type.\n        \n        \n        Returns:\n            The operation result (``Any``).\n        '
        return cls(text=data.get('text', ''), user=User.from_dict(data.get('user'))) if data else None
