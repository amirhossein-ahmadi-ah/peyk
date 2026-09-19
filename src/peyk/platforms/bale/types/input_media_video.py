from __future__ import annotations
from dataclasses import dataclass
from typing import Optional
from .media_input import MediaInput

@dataclass(frozen=True)
class InputMediaVideo:
    """Represent an outgoing Bale ``InputMediaVideo`` item."""
    media: MediaInput
    caption: Optional[str] = None
    width: Optional[int] = None
    height: Optional[int] = None
    duration: Optional[int] = None
