from __future__ import annotations

from typing import Any, Dict, List, Mapping, Optional, Sequence, Union

from peyk.transport import FilePayload
from ..models import *

ChatId = Union[int, str]
EntitiesInput = Sequence[Union[MessageEntity, Mapping[str, object]]]
MediaInput = Union[str, bytes, FilePayload]


def _resolve_album_item(self, item: InputMediaItem, index: int, files: Dict[str, FilePayload]) -> Dict[str, object]:
    """Resolve one album item to its JSON entry, registering uploads."""

    def _ref(value: object, suffix: str) -> str:
        if isinstance(value, str):
            return value
        attach_name = f'file{index}_{suffix}'
        files[attach_name] = self._as_file_payload(value, default_filename=f'{suffix}_{index}')
        return f'attach://{attach_name}'
    if isinstance(item, InputMediaPhoto):
        return item.to_dict(_ref(item.media, 'media'))
    if isinstance(item, InputMediaVideo):
        return item.to_dict(_ref(item.media, 'media'), thumbnail=_ref(item.thumbnail, 'thumbnail') if item.thumbnail is not None else None, cover=_ref(item.cover, 'cover') if item.cover is not None else None)
    if isinstance(item, InputMediaAnimation):
        return item.to_dict(_ref(item.media, 'media'), thumbnail=_ref(item.thumbnail, 'thumbnail') if item.thumbnail is not None else None)
    if isinstance(item, InputMediaAudio):
        return item.to_dict(_ref(item.media, 'media'), thumbnail=_ref(item.thumbnail, 'thumbnail') if item.thumbnail is not None else None)
    if isinstance(item, InputMediaDocument):
        return item.to_dict(_ref(item.media, 'media'), thumbnail=_ref(item.thumbnail, 'thumbnail') if item.thumbnail is not None else None)
    if isinstance(item, InputMediaLivePhoto):
        return item.to_dict(_ref(item.media, 'media'), _ref(item.photo, 'photo'))
    raise TypeError(f'send_media_group: unsupported item type {type(item).__name__}')
