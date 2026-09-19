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

async def get_chat_menu_button(self, *, chat_id: Optional[ChatId]=None) -> MenuButton:
    """Use this method to get the current value of the bot's menu button in a private chat, or the default menu button. Returns MenuButton on success.

Args:
    chat_id: Unique identifier for the target private chat. If not specified, the bot's default menu button will be returned."""
    payload: Dict[str, object] = {}
    if chat_id is not None:
        payload['chat_id'] = chat_id
    return parse_menu_button(await self._call('getChatMenuButton', json_body=payload))
