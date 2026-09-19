from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Dict, List, Mapping, Optional, Sequence, Union

@dataclass
class RichBlockAudio:
    """A block with a music file, corresponding to the HTML tag .

Attributes:
    type: Type of the block, always 'audio'
    audio: The audio
    caption: Caption of the block"""
    audio: Optional[Audio] = None

    @classmethod
    def from_dict(cls, data):
        """Provides the from dict operation for the Telegram integration.

Args:
    data: Value used by this operation."""
        'Executes the from_dict operation.\n        \n        Args:\n            data: Value of the declared parameter type.\n        \n        \n        Returns:\n            The operation result (``Any``).\n        '
        return cls(audio=Audio.from_dict(data.get('audio'))) if data else None
