from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Dict, List, Mapping, Optional, Sequence, Union

@dataclass
class RichBlockPhoto:
    """A block with a photo, corresponding to the HTML tag .

Attributes:
    type: Type of the block, always 'photo'
    photo: Available sizes of the photo
    has_spoiler: True, if the media preview is covered by a spoiler animation
    caption: Caption of the block"""
    photo: Optional[List[PhotoSize]] = None

    @classmethod
    def from_dict(cls, data):
        """Provides the from dict operation for the Telegram integration.

Args:
    data: Value used by this operation."""
        'Executes the from_dict operation.\n        \n        Args:\n            data: Value of the declared parameter type.\n        \n        \n        Returns:\n            The operation result (``Any``).\n        '
        return cls(photo=PhotoSize.list_from(data.get('photo'))) if data else None
