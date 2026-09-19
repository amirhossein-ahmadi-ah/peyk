from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Dict, List, Mapping, Optional, Sequence, Union

@dataclass
class RichTextAnchorLink:
    """A link to an anchor.

Attributes:
    type: Type of the rich text, always 'anchor_link'
    text: The link text
    anchor_name: The name of the anchor. If the name is empty, then the link brings back to the top of the message."""
    text: str = ''
    anchor_name: str = ''
    type: str = 'anchor_link'

    @classmethod
    def from_dict(cls, data):
        """Provides the from dict operation for the Telegram integration.

Args:
    data: Value used by this operation."""
        'Executes the from_dict operation.\n        \n        Args:\n            data: Value of the declared parameter type.\n        \n        \n        Returns:\n            The operation result (``Any``).\n        '
        return cls(text=data.get('text', ''), anchor_name=data.get('anchor_name', '')) if data else None
