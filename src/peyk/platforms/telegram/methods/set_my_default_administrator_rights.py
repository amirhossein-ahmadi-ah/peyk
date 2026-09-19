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

async def set_my_default_administrator_rights(self, *, rights: Optional[ChatAdministratorRights]=None, for_channels: Optional[bool]=None) -> bool:
    """Use this method to change the default administrator rights requested by the bot when it's added as an administrator to groups or channels. These rights will be suggested to users, but they are free to modify the list before adding the bot. Returns True on success.

Args:
    rights: A JSON-serialized object describing new default administrator rights. If not specified, the default administrator rights will be cleared.
    for_channels: Pass True to change the default administrator rights of the bot in channels. Otherwise, the default administrator rights of the bot for groups and supergroups will be changed.

Returns:
    bool: Result returned by Telegram on successful execution."""
    payload: Dict[str, object] = {}
    if rights is not None:
        payload['rights'] = rights.to_dict()
    if for_channels is not None:
        payload['for_channels'] = for_channels
    return bool(await self._call('setMyDefaultAdministratorRights', json_body=payload))
