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

async def get_my_commands(self, *, scope: Optional[Union[BotCommandScope, Mapping[str, object]]]=None, language_code: Optional[str]=None) -> List[BotCommand]:
    """Use this method to get the current list of the bot's commands for the given scope and user language. Returns an Array of BotCommand objects. If commands aren't set, an empty list is returned.

Args:
    scope: A JSON-serialized object, describing scope of users. Defaults to BotCommandScopeDefault.
    language_code: A two-letter ISO 639-1 language code or an empty string

Returns:
    List[BotCommand]: Result returned by Telegram on successful execution."""
    payload: Dict[str, object] = {}
    if scope is not None:
        payload['scope'] = serialize_bot_command_scope(scope)
    if language_code is not None:
        payload['language_code'] = language_code
    result = await self._call('getMyCommands', json_body=payload)
    return [cmd for cmd in (BotCommand.from_dict(item) for item in result or []) if cmd is not None]
