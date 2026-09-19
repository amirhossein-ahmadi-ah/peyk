from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Dict, List, Mapping, Optional, Sequence, Union

@dataclass
class InputRichBlockDetails:
    """An expandable block for details disclosure, corresponding to the HTML tag .

Attributes:
    type: Type of the block, always 'details'
    summary: Always shown summary of the block
    blocks: Content of the block
    is_open: Pass True if the content of the block is visible by default"""
    title: str = ''
    text: str = ''

    def to_dict(self) -> Dict[str, object]:
        """Provides the to dict operation for the Telegram integration.

Returns:
    Result produced by the operation."""
        'Executes the to_dict operation.\n        \n        Returns:\n            The operation result (``Dict[str, object]``).\n        '
        return {'title': self.title, 'text': self.text}
