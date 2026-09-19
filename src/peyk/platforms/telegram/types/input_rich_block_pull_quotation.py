from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Dict, List, Mapping, Optional, Sequence, Union

@dataclass
class InputRichBlockPullQuotation:
    """A quotation with centered text, loosely corresponding to the HTML tag .

Attributes:
    type: Type of the block, always 'pullquote'
    text: Text of the block
    credit: Credit of the block"""
    text: str = ''

    def to_dict(self) -> Dict[str, object]:
        """Provides the to dict operation for the Telegram integration.

Returns:
    Result produced by the operation."""
        'Executes the to_dict operation.\n        \n        Returns:\n            The operation result (``Dict[str, object]``).\n        '
        return {'text': self.text}
