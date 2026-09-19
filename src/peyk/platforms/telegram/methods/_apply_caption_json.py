from __future__ import annotations

from typing import Any, Dict, List, Mapping, Optional, Sequence, Union

from peyk.transport import FilePayload
from ..models import *

ChatId = Union[int, str]
EntitiesInput = Sequence[Union[MessageEntity, Mapping[str, object]]]
MediaInput = Union[str, bytes, FilePayload]

from ._serialization import _serialize_entities, _serialize_reply_parameters, _serialize_link_preview

def _apply_caption_json(payload: Dict[str, object], *, caption: Optional[str]=None, parse_mode: Optional[str]=None, caption_entities: Optional[EntitiesInput]=None) -> None:
    """Telegram Bot API method ``_apply_caption_json`` (T1-T5).

The implementation is preserves the existing implementation ``TelegramClient``
without changing request construction, return parsing, or error behavior."""
    if caption is not None:
        payload['caption'] = caption
    if parse_mode is not None:
        payload['parse_mode'] = parse_mode
    serialized = _serialize_entities(caption_entities)
    if serialized is not None:
        payload['caption_entities'] = serialized
