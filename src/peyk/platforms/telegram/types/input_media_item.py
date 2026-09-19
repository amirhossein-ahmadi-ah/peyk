"""T3 input-media union alias retained for compatibility."""

from typing import Union

from .input_media_animation import InputMediaAnimation
from .input_media_audio import InputMediaAudio
from .input_media_document import InputMediaDocument
from .input_media_live_photo import InputMediaLivePhoto
from .input_media_photo import InputMediaPhoto
from .input_media_video import InputMediaVideo

InputMediaItem = Union[
    InputMediaPhoto,
    InputMediaVideo,
    InputMediaAnimation,
    InputMediaAudio,
    InputMediaDocument,
    InputMediaLivePhoto,
]
