from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Dict, List, Mapping, Optional, Sequence, Union

@dataclass
class RichTextAnchor:
    """An anchor.

Attributes:
    type: Type of the rich text, always 'anchor'
    name: The name of the anchor"""
    text: str = ''
    name: str = ''
    type: str = 'anchor'

    @classmethod
    def from_dict(cls, data):
        """Provides the from dict operation for the Telegram integration.

Args:
    data: Value used by this operation."""
        'Executes the from_dict operation.\n        \n        Args:\n            data: Value of the declared parameter type.\n        \n        \n        Returns:\n            The operation result (``Any``).\n        '
        return cls(text=data.get('text', ''), name=data.get('name', '')) if data else None
