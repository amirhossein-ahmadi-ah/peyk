from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Dict, List, Mapping, Optional, Sequence, Union

@dataclass
class RichTextBankCardNumber:
    """A text with a bank card number.

Attributes:
    type: Type of the rich text, always 'bank_card_number'
    text: The text
    bank_card_number: The bank card number"""
    text: str = ''
    bank_card_number: str = ''
    type: str = 'bank_card_number'

    @classmethod
    def from_dict(cls, data):
        """Provides the from dict operation for the Telegram integration.

Args:
    data: Value used by this operation."""
        'Executes the from_dict operation.\n        \n        Args:\n            data: Value of the declared parameter type.\n        \n        \n        Returns:\n            The operation result (``Any``).\n        '
        return cls(text=data.get('text', ''), bank_card_number=data.get('bank_card_number', '')) if data else None
