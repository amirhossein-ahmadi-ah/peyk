"""T4 union alias for poll-option media."""

from typing import Union

from .input_media_animation import InputMediaAnimation
from .input_media_link import InputMediaLink
from .input_media_live_photo import InputMediaLivePhoto
from .input_media_location import InputMediaLocation
from .input_media_photo import InputMediaPhoto
from .input_media_venue import InputMediaVenue
from .input_media_video import InputMediaVideo

InputPollOptionMedia = Union[
    InputMediaPhoto, InputMediaVideo, InputMediaAnimation, InputMediaLink,
    InputMediaLivePhoto, InputMediaLocation, InputMediaVenue,
]
