from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Dict, List, Mapping, Optional, Sequence, Union

@dataclass
class InputRichBlockPhoto:
    """A block with a photo, corresponding to the HTML tag .

Attributes:
    type: Type of the block, always 'photo'
    photo: The photo. Caption is ignored.
    caption: Caption of the block"""
    photo: object = None
    caption: Optional[str] = None

    def to_dict(self, media_ref: str) -> Dict[str, object]:
        """Provides the to dict operation for the Telegram integration.

Args:
    media_ref: Value used by this operation.

Returns:
    Result produced by the operation."""
        'Executes the to_dict operation.\n        \n        Args:\n            media_ref: Value of the declared parameter type.\n        \n        \n        Returns:\n            The operation result (``Dict[str, object]``).\n        '
        body: Dict[str, object] = {'type': 'photo', 'photo': media_ref}
        if self.caption is not None:
            body['caption'] = self.caption
        return body
