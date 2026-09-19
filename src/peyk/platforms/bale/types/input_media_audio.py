from __future__ import annotations
from dataclasses import dataclass
from typing import Optional
from .media_input import MediaInput

@dataclass(frozen=True)
class InputMediaAudio:
    """Represent an outgoing Bale ``InputMediaAudio`` item."""
    media: MediaInput
    caption: Optional[str] = None
    duration: Optional[int] = None
    title: Optional[str] = None
