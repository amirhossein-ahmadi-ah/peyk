from __future__ import annotations
from typing import Any, Dict, List, Mapping, Optional, Sequence, Union
from peyk.transport import FilePayload
from ..models import *
ChatId = Union[int, str]
EntitiesInput = Sequence[Union[MessageEntity, Mapping[str, object]]]
MediaInput = Union[str, bytes, FilePayload]

async def pin_chat_message(self, chat_id: ChatId, message_id: int, *, disable_notification: Optional[bool]=None) -> bool:
    """Use this method to add a message to the list of pinned messages in a chat. In private chats and channel direct messages chats, all non-service messages can be pinned. Conversely, the bot must be an administrator with the 'can_pin_messages' right or the 'can_edit_messages' right to pin messages in groups and channels respectively. Returns True on success.

Args:
    chat_id: Unique identifier for the target chat or username of the target channel in the format @username
    message_id: Identifier of a message to pin
    disable_notification: Pass True if it is not necessary to send a notification to all chat members about the new pinned message. Notifications are always disabled in channels and private chats.

Returns:
    bool: Result returned by Telegram on successful execution."""
    payload: Dict[str, object] = {'chat_id': chat_id, 'message_id': message_id}
    if disable_notification is not None:
        payload['disable_notification'] = disable_notification
    return bool(await self._call('pinChatMessage', json_body=payload))
