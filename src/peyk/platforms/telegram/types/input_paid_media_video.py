from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Dict, List, Mapping, Optional, Sequence, Union

@dataclass
class InputPaidMediaVideo:
    """The paid media to send is a video.

Attributes:
    type: Type of the media, must be video
    media: File to send. Pass a file_id to send a file that exists on the Telegram servers (recommended), pass an HTTP URL for Telegram to get a file from the Internet, or pass 'attach://' to upload a new one using multipart/form-data under  name. More information on Sending Files
    thumbnail: Thumbnail of the file sent; can be ignored if thumbnail generation for the file is supported server-side. The thumbnail should be in JPEG format and less than 200 kB in size. A thumbnail's width and height should not exceed 320. Ignored if the file is not uploaded using multipart/form-data. Thumbnails can't be reused and can be only uploaded as a new file, so you can pass 'attach://' if the thumbnail was uploaded using multipart/form-data under . More information on Sending Files
    cover: Cover for the video in the message. Pass a file_id to send a file that exists on the Telegram servers (recommended), pass an HTTP URL for Telegram to get a file from the Internet, or pass 'attach://' to upload a new one using multipart/form-data under  name. More information on Sending Files
    start_timestamp: Start timestamp for the video in the message
    width: Video width
    height: Video height
    duration: Video duration in seconds
    supports_streaming: Pass True if the uploaded video is suitable for streaming"""
    media: str
    type: str = 'video'
    thumbnail: Optional[str] = None
    cover: Optional[str] = None
    start_timestamp: Optional[int] = None
    width: Optional[int] = None
    height: Optional[int] = None
    duration: Optional[int] = None
    supports_streaming: Optional[bool] = None

    @classmethod
    def from_dict(cls, data: Optional[dict]) -> Optional['InputPaidMediaVideo']:
        """Provides the from dict operation for the Telegram integration.

Args:
    data: Value used by this operation.

Returns:
    Result produced by the operation."""
        "Executes the from_dict operation.\n        \n        Args:\n            data: Value of the declared parameter type.\n        \n        \n        Returns:\n            The operation result (``Optional['InputPaidMediaVideo']``).\n        "
        if data is None:
            return None
        return cls(media=_parse_api_value('String', data.get('media')), type=_parse_api_value('String', data.get('type')), thumbnail=_parse_api_value('String', data.get('thumbnail')), cover=_parse_api_value('String', data.get('cover')), start_timestamp=_parse_api_value('Integer', data.get('start_timestamp')), width=_parse_api_value('Integer', data.get('width')), height=_parse_api_value('Integer', data.get('height')), duration=_parse_api_value('Integer', data.get('duration')), supports_streaming=_parse_api_value('Boolean', data.get('supports_streaming')))
