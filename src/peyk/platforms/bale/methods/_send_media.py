from __future__ import annotations

from ..errors import BaleAPIError
from peyk.transport import FilePayload
from typing import Any, Dict, Mapping, Optional, Union
from ..types.media_input import MediaInput

async def _send_media(self, method_name: str, field_name: str, chat_id: Union[int, str], media: MediaInput, caption: Optional[str], *, reply_to_message_id: Optional[int]=None, reply_markup: Optional[Mapping[str, object]]=None, default_filename: str) -> object:
    """Build Bale's media request through the shared transport path."""
    json_fields: Dict[str, object] = {}
    if caption is not None:
        json_fields['caption'] = caption
    if reply_to_message_id is not None:
        json_fields['reply_to_message_id'] = reply_to_message_id
    if reply_markup is not None:
        json_fields['reply_markup'] = reply_markup
    kwargs = self._build_media_request_kwargs(field_name, media, json_fields={'chat_id': chat_id, **json_fields}, default_filename=default_filename)
    return await self._call(method_name, **kwargs)
