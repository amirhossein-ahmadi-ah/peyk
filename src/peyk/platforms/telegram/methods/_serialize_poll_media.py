from __future__ import annotations

from typing import Any, Dict, List, Mapping, Optional, Sequence, Union

from peyk.transport import FilePayload
from ..models import *

ChatId = Union[int, str]
EntitiesInput = Sequence[Union[MessageEntity, Mapping[str, object]]]
MediaInput = Union[str, bytes, FilePayload]


def _serialize_poll_media(value: Optional[Union[InputPollMedia, Mapping[str, object]]]) -> Optional[Dict[str, object]]:
    """Telegram Bot API method ``_serialize_poll_media`` (T1-T5).

The implementation is preserves the existing implementation ``TelegramClient``
without changing request construction, return parsing, or error behavior."""
    if value is None:
        return None
    if isinstance(value, Mapping):
        return dict(value)
    if isinstance(value, (InputMediaLocation, InputMediaVenue)):
        return value.to_dict()

    def _ref(field: object, *, what: str) -> str:
        if not isinstance(field, str):
            raise ValueError(f'poll media {what} must be a file_id/URL string (sendPoll has no multipart upload path)')
        return field
    if isinstance(value, InputMediaVideo):
        return value.to_dict(_ref(value.media, what='video'), thumbnail=_ref(value.thumbnail, what='thumbnail') if value.thumbnail is not None else None, cover=_ref(value.cover, what='cover') if value.cover is not None else None)
    if isinstance(value, (InputMediaAnimation, InputMediaAudio, InputMediaDocument)):
        return value.to_dict(_ref(value.media, what='media'), thumbnail=_ref(value.thumbnail, what='thumbnail') if value.thumbnail is not None else None)
    if isinstance(value, InputMediaLivePhoto):
        return value.to_dict(_ref(value.media, what='live video'), _ref(value.photo, what='static photo'))
    return value.to_dict(_ref(value.media, what='photo'))
