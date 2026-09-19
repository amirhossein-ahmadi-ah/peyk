from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Dict, List, Mapping, Optional, Sequence, Union

@dataclass
class RichTextEmailAddress:
    """A text with an email address.

Attributes:
    type: Type of the rich text, always 'email_address'
    text: The text
    email_address: The email address"""
    text: str = ''
    email: str = ''
    type: str = 'email_address'

    @classmethod
    def from_dict(cls, data):
        """Provides the from dict operation for the Telegram integration.

Args:
    data: Value used by this operation."""
        'Executes the from_dict operation.\n        \n        Args:\n            data: Value of the declared parameter type.\n        \n        \n        Returns:\n            The operation result (``Any``).\n        '
        return cls(text=data.get('text', ''), email=data.get('email', '')) if data else None
