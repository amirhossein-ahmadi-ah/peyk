from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Dict, List, Mapping, Optional, Sequence, Union

@dataclass
class RichBlockDetails:
    """An expandable block for details disclosure, corresponding to the HTML tag .

Attributes:
    type: Type of the block, always 'details'
    summary: Always shown summary of the block
    blocks: Content of the block
    is_open: True, if the content of the block is visible by default"""
    title: str = ''
    text: str = ''

    @classmethod
    def from_dict(cls, data):
        """Provides the from dict operation for the Telegram integration.

Args:
    data: Value used by this operation."""
        'Executes the from_dict operation.\n        \n        Args:\n            data: Value of the declared parameter type.\n        \n        \n        Returns:\n            The operation result (``Any``).\n        '
        return cls(title=data.get('title', ''), text=data.get('text', '')) if data else None
