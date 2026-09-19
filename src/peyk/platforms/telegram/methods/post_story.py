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

async def post_story(self, business_connection_id: str, content: InputStoryContent, active_period: int, *, caption: Optional[str]=None, parse_mode: Optional[str]=None, caption_entities: Optional[List[MessageEntity]]=None, areas: Optional[List[StoryArea]]=None, post_to_chat_page: Optional[bool]=None, protect_content: Optional[bool]=None) -> Story:
    """Posts a story on behalf of a managed business account. Requires the can_manage_stories business bot right. Returns Story on success.

Args:
    business_connection_id: Unique identifier of the business connection
    content: Content of the story
    active_period: Period after which the story is moved to the archive, in seconds; must be one of 6  3600, 12  3600, 86400, or 2 * 86400
    caption: Caption of the story, 0-2048 characters after entities parsing
    parse_mode: Mode for parsing entities in the story caption. See formatting options for more details.
    caption_entities: A JSON-serialized list of special entities that appear in the caption, which can be specified instead of parse_mode
    areas: A JSON-serialized list of clickable areas to be shown on the story
    post_to_chat_page: Pass True to keep the story accessible after it expires
    protect_content: Pass True if the content of the story must be protected from forwarding and screenshotting"""
    payload: Dict[str, object] = {}
    if business_connection_id is not None:
        payload['business_connection_id'] = _serialize_api_value(business_connection_id)
    if content is not None:
        payload['content'] = _serialize_api_value(content)
    if active_period is not None:
        payload['active_period'] = _serialize_api_value(active_period)
    if caption is not None:
        payload['caption'] = _serialize_api_value(caption)
    if parse_mode is not None:
        payload['parse_mode'] = _serialize_api_value(parse_mode)
    if caption_entities is not None:
        payload['caption_entities'] = _serialize_api_value(caption_entities)
    if areas is not None:
        payload['areas'] = _serialize_api_value(areas)
    if post_to_chat_page is not None:
        payload['post_to_chat_page'] = _serialize_api_value(post_to_chat_page)
    if protect_content is not None:
        payload['protect_content'] = _serialize_api_value(protect_content)
    result = await self._call('postStory', json_body=payload)
    return _parse_api_result('Story', result)
