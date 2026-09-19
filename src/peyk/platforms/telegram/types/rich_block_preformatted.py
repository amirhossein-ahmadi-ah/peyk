from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Dict, List, Mapping, Optional, Sequence, Union

@dataclass
class RichBlockPreformatted:
    """A preformatted text block, corresponding to the nested HTML tags  and .

Attributes:
    type: Type of the block, always 'pre'
    text: Text of the block
    language: The programming language of the text"""
    text: str = ''
    language: str = ''

    @classmethod
    def from_dict(cls, data):
        """Provides the from dict operation for the Telegram integration.

Args:
    data: Value used by this operation."""
        'Executes the from_dict operation.\n        \n        Args:\n            data: Value of the declared parameter type.\n        \n        \n        Returns:\n            The operation result (``Any``).\n        '
        return cls(text=data.get('text', ''), language=data.get('language', '')) if data else None
