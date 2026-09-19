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

async def edit_chat_subscription_invite_link(self, chat_id: Union[int, str], invite_link: str, *, name: Optional[str]=None) -> object:
    """Use this method to edit a subscription invite link created by the bot. The bot must have the can_invite_users administrator rights. Returns the edited invite link as a ChatInviteLink object.

Args:
    chat_id: Unique identifier for the target chat or username of the target channel in the format @username
    invite_link: The invite link to edit
    name: Invite link name; 0-32 characters"""
    payload: Dict[str, object] = {}
    if chat_id is not None:
        payload['chat_id'] = _serialize_api_value(chat_id)
    if invite_link is not None:
        payload['invite_link'] = _serialize_api_value(invite_link)
    if name is not None:
        payload['name'] = _serialize_api_value(name)
    result = await self._call('editChatSubscriptionInviteLink', json_body=payload)
    return _parse_api_result('ChatInviteLink', result)
