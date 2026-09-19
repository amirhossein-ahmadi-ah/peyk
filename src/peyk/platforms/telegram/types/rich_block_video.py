from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Dict, List, Mapping, Optional, Sequence, Union

@dataclass
class RichBlockVideo:
    """A block with a video, corresponding to the HTML tag .

Attributes:
    type: Type of the block, always 'video'
    video: The video
    has_spoiler: True, if the media preview is covered by a spoiler animation
    caption: Caption of the block"""
    video: Optional[Video] = None

    @classmethod
    def from_dict(cls, data):
        """Provides the from dict operation for the Telegram integration.

Args:
    data: Value used by this operation."""
        'Executes the from_dict operation.\n        \n        Args:\n            data: Value of the declared parameter type.\n        \n        \n        Returns:\n            The operation result (``Any``).\n        '
        return cls(video=Video.from_dict(data.get('video'))) if data else None
