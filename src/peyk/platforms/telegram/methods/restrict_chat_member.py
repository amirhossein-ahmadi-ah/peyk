from __future__ import annotations
from typing import Any, Dict, List, Mapping, Optional, Sequence, Union
from peyk.transport import FilePayload
from ..models import *
ChatId = Union[int, str]
EntitiesInput = Sequence[Union[MessageEntity, Mapping[str, object]]]
MediaInput = Union[str, bytes, FilePayload]

async def restrict_chat_member(self, chat_id: ChatId, user_id: int, permissions: Union[ChatPermissions, Mapping[str, object]], *, use_independent_chat_permissions: Optional[bool]=None, until_date: Optional[int]=None) -> bool:
    """Use this method to restrict a user in a supergroup. The bot must be an administrator in the supergroup for this to work and must have the appropriate administrator rights. Pass True for all permissions to lift restrictions from a user. Returns True on success.

Args:
    chat_id: Unique identifier for the target chat or username of the target supergroup in the format @username
    user_id: Unique identifier of the target user
    permissions: A JSON-serialized object for new user permissions
    use_independent_chat_permissions: Pass True if chat permissions are set independently. Otherwise, the can_send_other_messages and can_add_web_page_previews permissions will imply the can_send_messages, can_send_audios, can_send_documents, can_send_photos, can_send_videos, can_send_video_notes, and can_send_voice_notes permissions; the can_send_polls permission will imply the can_send_messages permission.
    until_date: Date when restrictions will be lifted for the user; Unix time. If user is restricted for more than 366 days or less than 30 seconds from the current time, they are considered to be restricted forever.

Returns:
    bool: Result returned by Telegram on successful execution."""
    payload: Dict[str, object] = {'chat_id': chat_id, 'user_id': user_id, 'permissions': self._serialize_permissions(permissions)}
    if use_independent_chat_permissions is not None:
        payload['use_independent_chat_permissions'] = use_independent_chat_permissions
    if until_date is not None:
        payload['until_date'] = until_date
    return bool(await self._call('restrictChatMember', json_body=payload))
