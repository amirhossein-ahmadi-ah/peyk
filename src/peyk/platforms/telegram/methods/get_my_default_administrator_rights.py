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

async def get_my_default_administrator_rights(self, *, for_channels: Optional[bool]=None) -> ChatAdministratorRights:
    """Use this method to get the current default administrator rights of the bot. Returns ChatAdministratorRights on success.

Args:
    for_channels: Pass True to get default administrator rights of the bot in channels. Otherwise, default administrator rights of the bot for groups and supergroups will be returned."""
    payload: Dict[str, object] = {}
    if for_channels is not None:
        payload['for_channels'] = for_channels
    return ChatAdministratorRights.from_dict(await self._call('getMyDefaultAdministratorRights', json_body=payload))
