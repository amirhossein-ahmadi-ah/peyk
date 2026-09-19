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

async def create_chat_subscription_invite_link(self, chat_id: Union[int, str], subscription_period: int, subscription_price: int, *, name: Optional[str]=None) -> object:
    """Use this method to create a subscription invite link for a channel chat. The bot must have the can_invite_users administrator rights. The link can be edited using the method editChatSubscriptionInviteLink or revoked using the method revokeChatInviteLink. Returns the new invite link as a ChatInviteLink object.

Args:
    chat_id: Unique identifier for the target channel chat or username of the target channel in the format @username
    subscription_period: The number of seconds the subscription will be active for before the next payment. Currently, it must always be 2592000 (30 days).
    subscription_price: The amount of Telegram Stars a user must pay initially and after each subsequent subscription period to be a member of the chat; 1-10000
    name: Invite link name; 0-32 characters"""
    payload: Dict[str, object] = {}
    if chat_id is not None:
        payload['chat_id'] = _serialize_api_value(chat_id)
    if name is not None:
        payload['name'] = _serialize_api_value(name)
    if subscription_period is not None:
        payload['subscription_period'] = _serialize_api_value(subscription_period)
    if subscription_price is not None:
        payload['subscription_price'] = _serialize_api_value(subscription_price)
    result = await self._call('createChatSubscriptionInviteLink', json_body=payload)
    return _parse_api_result('ChatInviteLink', result)
