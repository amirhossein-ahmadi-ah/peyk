from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Dict, List, Mapping, Optional, Sequence, Union

@dataclass
class RichTextPhoneNumber:
    """A text with a phone number.

Attributes:
    type: Type of the rich text, always 'phone_number'
    text: The text
    phone_number: The phone number"""
    text: str = ''
    phone_number: str = ''
    type: str = 'phone_number'

    @classmethod
    def from_dict(cls, data):
        """Provides the from dict operation for the Telegram integration.

Args:
    data: Value used by this operation."""
        'Executes the from_dict operation.\n        \n        Args:\n            data: Value of the declared parameter type.\n        \n        \n        Returns:\n            The operation result (``Any``).\n        '
        return cls(text=data.get('text', ''), phone_number=data.get('phone_number', '')) if data else None
