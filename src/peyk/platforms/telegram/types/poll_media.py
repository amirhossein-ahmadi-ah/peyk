from __future__ import annotations
from dataclasses import dataclass, field
import re
from typing import Any, Dict, List, Mapping, Optional, Sequence, Union
from .animation import Animation
from .audio import Audio
from .document import Document
from .link import Link
from .live_photo import LivePhoto
from .location import Location
from .photo_size import PhotoSize
from .venue import Venue
from .video import Video

@dataclass
class PollMedia:
    """At most one of the optional fields can be present in any given object.

Attributes:
    animation: Media is an animation, information about the animation
    audio: Media is an audio file, information about the file; currently, can't be received in a poll option
    document: Media is a general file, information about the file; currently, can't be received in a poll option
    live_photo: Media is a live photo, information about the live photo
    location: Media is a shared location, information about the location
    photo: Media is a photo, available sizes of the photo
    sticker: Media is a sticker, information about the sticker; currently, for poll options only
    venue: Media is a venue, information about the venue
    video: Media is a video, information about the video
    link: The HTTP link attached to the poll option"""
    animation: Optional[Animation] = None
    audio: Optional[Audio] = None
    document: Optional[Document] = None
    link: Optional[Link] = None
    live_photo: Optional[LivePhoto] = None
    location: Optional[Location] = None
    photo: Optional[List[PhotoSize]] = None
    sticker: Optional[object] = None
    venue: Optional[Venue] = None
    video: Optional[Video] = None

    @classmethod
    def from_dict(cls, data: Optional[dict]) -> Optional['PollMedia']:
        """Parse a Telegram API mapping into this type.

Args:
    data: Raw Telegram API mapping, or ``None``.

Returns:
    Parsed type instance, or ``None`` when ``data`` is ``None``."""
        if data is None:
            return None
        return cls(animation=Animation.from_dict(data.get('animation')), audio=Audio.from_dict(data.get('audio')), document=Document.from_dict(data.get('document')), link=Link.from_dict(data.get('link')), live_photo=LivePhoto.from_dict(data.get('live_photo')), location=Location.from_dict(data.get('location')), photo=PhotoSize.list_from(data.get('photo')), sticker=data.get('sticker'), venue=Venue.from_dict(data.get('venue')), video=Video.from_dict(data.get('video')))
