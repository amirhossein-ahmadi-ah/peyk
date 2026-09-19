from __future__ import annotations
from typing import Union
from .input_media_photo import InputMediaPhoto
from .input_media_video import InputMediaVideo
from .input_media_animation import InputMediaAnimation
from .input_media_audio import InputMediaAudio
from .input_media_document import InputMediaDocument

InputMediaItem = Union[InputMediaPhoto, InputMediaVideo, InputMediaAnimation, InputMediaAudio, InputMediaDocument]
_INPUT_MEDIA_TYPE_NAMES = {InputMediaPhoto:"photo",InputMediaVideo:"video",InputMediaAnimation:"animation",InputMediaAudio:"audio",InputMediaDocument:"document"}
