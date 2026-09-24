from __future__ import annotations

from typing import Any, Dict, List, Mapping, Optional, Sequence, Union

from peyk.transport import FilePayload
from ..models import *

ChatId = Union[int, str]
EntitiesInput = Sequence[Union[MessageEntity, Mapping[str, object]]]
MediaInput = Union[str, bytes, FilePayload]

from ._serialization import _serialize_entities, _serialize_reply_parameters, _serialize_link_preview

async def _send_file_message(self, method_name: str, field_name: str, chat_id: ChatId, media: MediaInput, *, caption: Optional[str]=None, parse_mode: Optional[str]=None, caption_entities: Optional[EntitiesInput]=None, message_thread_id: Optional[int]=None, disable_notification: Optional[bool]=None, protect_content: Optional[bool]=None, reply_parameters: Optional[Union[ReplyParameters, Mapping[str, object]]]=None, reply_markup: Optional[ReplyMarkup]=None, extra_json: Optional[Mapping[str, object]]=None, extra_files: Optional[Mapping[str, MediaInput]]=None, default_filename: str='file') -> Message:
    """Telegram's public media signatures feed the shared request builder."""
    json_fields: Dict[str, object] = dict(extra_json or {})
    if caption is not None:
        json_fields['caption'] = caption
    if parse_mode is not None:
        json_fields['parse_mode'] = parse_mode
    serialized = _serialize_entities(caption_entities)
    if serialized is not None:
        json_fields['caption_entities'] = serialized
    form_fields: Dict[str, str] = {}
    json_payload: Dict[str, object] = {'chat_id': chat_id, field_name: media, **json_fields}
    self._apply_send_options_json(json_payload, message_thread_id=message_thread_id, disable_notification=disable_notification, protect_content=protect_content, reply_parameters=reply_parameters, reply_markup=reply_markup)
    if not (self._is_upload(media) or any((self._is_upload(v) for v in (extra_files or {}).values()))):
        result = await self._call(method_name, json_body={**json_payload, **{k: v for k, v in (extra_files or {}).items()}})
        return Message.from_dict(result)
    form_fields = {key: self._form_field_value(value) for key, value in json_payload.items() if key != field_name}
    self._apply_send_options_form(form_fields, message_thread_id=message_thread_id, disable_notification=disable_notification, protect_content=protect_content, reply_parameters=reply_parameters, reply_markup=reply_markup)
    kwargs = self._build_media_request_kwargs(field_name, media, form_fields=form_fields, extra_files=extra_files, default_filename=default_filename)
    result = await self._call(method_name, **kwargs)
    return Message.from_dict(result)
