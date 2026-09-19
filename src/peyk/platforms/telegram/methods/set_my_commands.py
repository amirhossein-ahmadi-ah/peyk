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

async def set_my_commands(self, commands: Sequence[Union[BotCommand, Mapping[str, object]]], *, scope: Optional[Union[BotCommandScope, Mapping[str, object]]]=None, language_code: Optional[str]=None) -> bool:
    """Use this method to change the list of the bot's commands. See this manual for more details about bot commands. Returns True on success.

Args:
    commands: A JSON-serialized list of bot commands to be set as the list of the bot's commands. At most 100 commands can be specified.
    scope: A JSON-serialized object, describing scope of users for which the commands are relevant. Defaults to BotCommandScopeDefault.
    language_code: A two-letter ISO 639-1 language code. If empty, commands will be applied to all users from the given scope, for whose language there are no dedicated commands.

Returns:
    bool: Result returned by Telegram on successful execution."""
    payload: Dict[str, object] = {'commands': [c.to_dict() if isinstance(c, BotCommand) else dict(c) for c in commands]}
    if scope is not None:
        payload['scope'] = serialize_bot_command_scope(scope)
    if language_code is not None:
        payload['language_code'] = language_code
    return bool(await self._call('setMyCommands', json_body=payload))
