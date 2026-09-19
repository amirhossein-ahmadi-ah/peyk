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

async def set_message_reaction(self, chat_id: Union[int, str], message_id: int, *, reaction: Optional[List[ReactionType]]=None, is_big: Optional[bool]=None) -> bool:
    """Use this method to change the chosen reactions on a message. Service messages of some types can't be reacted to. Automatically forwarded messages from a channel to its discussion group have the same available reactions as messages in the channel. Bots can't use paid reactions. Returns True on success.

Args:
    chat_id: Unique identifier for the target chat or username of the target bot, supergroup or channel in the format @username
    message_id: Identifier of the target message. If the message belongs to a media group, the reaction is set to the first non-deleted message in the group instead.
    reaction: A JSON-serialized list of reaction types to set on the message. Currently, as non-premium users, bots can set up to one reaction per message. A custom emoji reaction can be used if it is either already present on the message or explicitly allowed by chat administrators. Paid reactions can't be used by bots.
    is_big: Pass True to set the reaction with a big animation

Returns:
    bool: Result returned by Telegram on successful execution."""
    payload: Dict[str, object] = {}
    if chat_id is not None:
        payload['chat_id'] = _serialize_api_value(chat_id)
    if message_id is not None:
        payload['message_id'] = _serialize_api_value(message_id)
    if reaction is not None:
        payload['reaction'] = _serialize_api_value(reaction)
    if is_big is not None:
        payload['is_big'] = _serialize_api_value(is_big)
    result = await self._call('setMessageReaction', json_body=payload)
    return _parse_api_result('bool', result)
