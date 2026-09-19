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

async def set_chat_menu_button(self, *, chat_id: Optional[ChatId]=None, menu_button: Optional[Union[MenuButton, Mapping[str, object]]]=None) -> bool:
    """Use this method to change the bot's menu button in a private chat, or the default menu button. Returns True on success.

Args:
    chat_id: Unique identifier for the target private chat. If not specified, the bot's default menu button will be changed.
    menu_button: A JSON-serialized object for the bot's new menu button. Defaults to MenuButtonDefault.

Returns:
    bool: Result returned by Telegram on successful execution."""
    payload: Dict[str, object] = {}
    if chat_id is not None:
        payload['chat_id'] = chat_id
    if menu_button is not None:
        payload['menu_button'] = serialize_menu_button(menu_button)
    return bool(await self._call('setChatMenuButton', json_body=payload))
