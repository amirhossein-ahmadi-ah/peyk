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

async def repost_story(self, business_connection_id: str, from_chat_id: int, from_story_id: int, active_period: int, *, post_to_chat_page: Optional[bool]=None, protect_content: Optional[bool]=None) -> Story:
    """Reposts a story on behalf of a business account from another business account. Both business accounts must be managed by the same bot, and the story on the source account must have been posted (or reposted) by the bot. Requires the can_manage_stories business bot right for both business accounts. Returns Story on success.

Args:
    business_connection_id: Unique identifier of the business connection
    from_chat_id: Unique identifier of the chat which posted the story that should be reposted
    from_story_id: Unique identifier of the story that should be reposted
    active_period: Period after which the story is moved to the archive, in seconds; must be one of 6  3600, 12  3600, 86400, or 2 * 86400
    post_to_chat_page: Pass True to keep the story accessible after it expires
    protect_content: Pass True if the content of the story must be protected from forwarding and screenshotting"""
    payload: Dict[str, object] = {}
    if business_connection_id is not None:
        payload['business_connection_id'] = _serialize_api_value(business_connection_id)
    if from_chat_id is not None:
        payload['from_chat_id'] = _serialize_api_value(from_chat_id)
    if from_story_id is not None:
        payload['from_story_id'] = _serialize_api_value(from_story_id)
    if active_period is not None:
        payload['active_period'] = _serialize_api_value(active_period)
    if post_to_chat_page is not None:
        payload['post_to_chat_page'] = _serialize_api_value(post_to_chat_page)
    if protect_content is not None:
        payload['protect_content'] = _serialize_api_value(protect_content)
    result = await self._call('repostStory', json_body=payload)
    return _parse_api_result('Story', result)
