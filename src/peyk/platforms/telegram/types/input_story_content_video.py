from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Dict, List, Mapping, Optional, Sequence, Union

@dataclass
class InputStoryContentVideo:
    """Describes a video to post as a story.

Attributes:
    type: Type of the content, must be video
    video: The video to post as a story. The video must be of the size 720x1280, streamable, encoded with H.265 codec, with key frames added each second in the MPEG4 format, and must not exceed 30 MB. The video can't be reused and can only be uploaded as a new file, so you can pass 'attach://' if the video was uploaded using multipart/form-data under . More information on Sending Files
    duration: Precise duration of the video in seconds; 0-60
    cover_frame_timestamp: Timestamp in seconds of the frame that will be used as the static cover for the story. Defaults to 0.0.
    is_animation: Pass True if the video has no sound"""
    video: str
    type: str = 'video'
    duration: Optional[float] = None
    cover_frame_timestamp: Optional[float] = None
    is_animation: Optional[bool] = None

    @classmethod
    def from_dict(cls, data: Optional[dict]) -> Optional['InputStoryContentVideo']:
        """Provides the from dict operation for the Telegram integration.

Args:
    data: Value used by this operation.

Returns:
    Result produced by the operation."""
        "Executes the from_dict operation.\n        \n        Args:\n            data: Value of the declared parameter type.\n        \n        \n        Returns:\n            The operation result (``Optional['InputStoryContentVideo']``).\n        "
        if data is None:
            return None
        return cls(video=_parse_api_value('String', data.get('video')), type=_parse_api_value('String', data.get('type')), duration=_parse_api_value('Float', data.get('duration')), cover_frame_timestamp=_parse_api_value('Float', data.get('cover_frame_timestamp')), is_animation=_parse_api_value('Boolean', data.get('is_animation')))
