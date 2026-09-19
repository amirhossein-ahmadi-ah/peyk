from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Dict, List, Mapping, Optional, Sequence, Union

@dataclass
class RichTextUrl:
    """A text with a link.

Attributes:
    type: Type of the rich text, always 'url'
    text: The text
    url: URL of the link"""
    text: str = ''
    url: str = ''
    type: str = 'url'

    @classmethod
    def from_dict(cls, data):
        """Provides the from dict operation for the Telegram integration.

Args:
    data: Value used by this operation."""
        'Executes the from_dict operation.\n        \n        Args:\n            data: Value of the declared parameter type.\n        \n        \n        Returns:\n            The operation result (``Any``).\n        '
        return cls(text=data.get('text', ''), url=data.get('url', '')) if data else None
