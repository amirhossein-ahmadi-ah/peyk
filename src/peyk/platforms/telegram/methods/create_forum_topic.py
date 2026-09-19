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

async def create_forum_topic(self, chat_id: ChatId, name: str, *, icon_color: Optional[int]=None, icon_custom_emoji_id: Optional[str]=None) -> ForumTopic:
    """Use this method to create a topic in a forum supergroup chat or a private chat with a user. In the case of a supergroup chat the bot must be an administrator in the chat for this to work and must have the can_manage_topics administrator right. Returns information about the created topic as a ForumTopic object.

Args:
    chat_id: Unique identifier for the target chat or username of the target supergroup in the format @username
    name: Topic name, 1-128 characters
    icon_color: Color of the topic icon in RGB format. Currently, must be one of 7322096 (0x6FB9F0), 16766590 (0xFFD67E), 13338331 (0xCB86DB), 9367192 (0x8EEE98), 16749490 (0xFF93B2), or 16478047 (0xFB6F5F).
    icon_custom_emoji_id: Unique identifier of the custom emoji shown as the topic icon. Use getForumTopicIconStickers to get all allowed custom emoji identifiers."""
    payload: Dict[str, object] = {'chat_id': chat_id, 'name': name}
    if icon_color is not None:
        payload['icon_color'] = icon_color
    if icon_custom_emoji_id is not None:
        payload['icon_custom_emoji_id'] = icon_custom_emoji_id
    return ForumTopic.from_dict(await self._call('createForumTopic', json_body=payload))
