from __future__ import annotations
from typing import Any, Dict, List, Mapping, Optional, Sequence, Union
import orjson
from peyk.transport import FilePayload
from ..errors import TelegramAPIError, ResponseParameters
from ..models import *
from .. import models as _models
globals().update({k: v for k, v in vars(_models).items() if k.startswith('_')})
ChatId = Union[int, str]
EntitiesInput = Sequence[Union[MessageEntity, Mapping[str, object]]]
MediaInput = Union[str, bytes, FilePayload]

async def edit_forum_topic(self, chat_id: ChatId, message_thread_id: int, *, name: Optional[str]=None, icon_color: Optional[int]=None, icon_custom_emoji_id: Optional[str]=None) -> bool:
    """Use this method to edit name and icon of a topic in a forum supergroup chat or a private chat with a user. In the case of a supergroup chat the bot must be an administrator in the chat for this to work and must have the can_manage_topics administrator rights, unless it is the creator of the topic. Returns True on success.

Args:
    chat_id: Unique identifier for the target chat or username of the target supergroup in the format @username
    message_thread_id: Unique identifier for the target message thread of the forum topic
    name: New topic name, 0-128 characters. If not specified or empty, the current name of the topic will be kept.
    icon_color: Value accepted by this operation.
    icon_custom_emoji_id: New unique identifier of the custom emoji shown as the topic icon. Use getForumTopicIconStickers to get all allowed custom emoji identifiers. Pass an empty string to remove the icon. If not specified, the current icon will be kept.

Returns:
    bool: Result returned by Telegram on successful execution."""
    payload: Dict[str, object] = {'chat_id': chat_id, 'message_thread_id': message_thread_id}
    if name is not None:
        payload['name'] = name
    if icon_color is not None:
        payload['icon_color'] = icon_color
    if icon_custom_emoji_id is not None:
        payload['icon_custom_emoji_id'] = icon_custom_emoji_id
    return ForumTopic.from_dict(await self._call('editForumTopic', json_body=payload))
