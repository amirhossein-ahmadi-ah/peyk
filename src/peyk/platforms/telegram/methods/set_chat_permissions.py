from __future__ import annotations
from typing import Any, Dict, List, Mapping, Optional, Sequence, Union
from peyk.transport import FilePayload
from ..models import *
ChatId = Union[int, str]
EntitiesInput = Sequence[Union[MessageEntity, Mapping[str, object]]]
MediaInput = Union[str, bytes, FilePayload]

async def set_chat_permissions(self, chat_id: ChatId, permissions: Union[ChatPermissions, Mapping[str, object]], *, use_independent_chat_permissions: Optional[bool]=None) -> bool:
    """Use this method to set default chat permissions for all members. The bot must be an administrator in the group or a supergroup for this to work and must have the can_restrict_members administrator rights. Returns True on success.

Args:
    chat_id: Unique identifier for the target chat or username of the target supergroup in the format @username
    permissions: A JSON-serialized object for new default chat permissions
    use_independent_chat_permissions: Pass True if chat permissions are set independently. Otherwise, the can_send_other_messages and can_add_web_page_previews permissions will imply the can_send_messages, can_send_audios, can_send_documents, can_send_photos, can_send_videos, can_send_video_notes, and can_send_voice_notes permissions; the can_send_polls permission will imply the can_send_messages permission.

Returns:
    bool: Result returned by Telegram on successful execution."""
    payload: Dict[str, object] = {'chat_id': chat_id, 'permissions': self._serialize_permissions(permissions)}
    if use_independent_chat_permissions is not None:
        payload['use_independent_chat_permissions'] = use_independent_chat_permissions
    return bool(await self._call('setChatPermissions', json_body=payload))
