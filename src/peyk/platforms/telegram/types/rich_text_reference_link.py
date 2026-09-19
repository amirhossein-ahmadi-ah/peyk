from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Dict, List, Mapping, Optional, Sequence, Union

@dataclass
class RichTextReferenceLink:
    """A link to a reference.

Attributes:
    type: Type of the rich text, always 'reference_link'
    text: The link text
    reference_name: The name of the reference"""
    text: str = ''
    reference_name: str = ''
    type: str = 'reference_link'

    @classmethod
    def from_dict(cls, data):
        """Provides the from dict operation for the Telegram integration.

Args:
    data: Value used by this operation."""
        'Executes the from_dict operation.\n        \n        Args:\n            data: Value of the declared parameter type.\n        \n        \n        Returns:\n            The operation result (``Any``).\n        '
        return cls(text=data.get('text', ''), reference_name=data.get('reference_name', '')) if data else None
