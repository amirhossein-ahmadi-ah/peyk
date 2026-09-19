from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Dict, List, Mapping, Optional, Sequence, Union

@dataclass
class RichBlockAnimation:
    """A block with an animation, corresponding to the HTML tag .

Attributes:
    type: Type of the block, always 'animation'
    animation: The animation
    has_spoiler: True, if the media preview is covered by a spoiler animation
    caption: Caption of the block"""
    animation: Optional[Animation] = None

    @classmethod
    def from_dict(cls, data):
        """Provides the from dict operation for the Telegram integration.

Args:
    data: Value used by this operation."""
        'Executes the from_dict operation.\n        \n        Args:\n            data: Value of the declared parameter type.\n        \n        \n        Returns:\n            The operation result (``Any``).\n        '
        return cls(animation=Animation.from_dict(data.get('animation'))) if data else None
