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

async def answer_callback_query(self, callback_query_id: str, *, text: Optional[str]=None, show_alert: Optional[bool]=None, url: Optional[str]=None, cache_time: Optional[int]=None) -> bool:
    """Use this method to send answers to callback queries sent from inline keyboards. The answer will be displayed to the user as a notification at the top of the chat screen or as an alert. On success, True is returned.
Alternatively, the user can be redirected to the specified Game URL. For this option to work, you must first create a game for your bot via @BotFather and accept the terms. Otherwise, you may use links like t.me/your_bot?start=XXXX that open your bot with a parameter.

Args:
    callback_query_id: Unique identifier for the query to be answered
    text: Text of the notification. If not specified, nothing will be shown to the user, 0-200 characters.
    show_alert: If True, an alert will be shown by the client instead of a notification at the top of the chat screen. Defaults to False.
    url: URL that will be opened by the user's client. If you have created a Game and accepted the conditions via @BotFather, specify the URL that opens your game - note that this will only work if the query comes from a callback_game button.

Otherwise, you may use links like t.me/your_bot?start=XXXX that open your bot with a parameter.
    cache_time: The maximum amount of time in seconds that the result of the callback query may be cached client-side. Telegram apps will support caching starting in version 3.14. Defaults to 0.

Returns:
    bool: Result returned by Telegram on successful execution."""
    payload: Dict[str, object] = {'callback_query_id': callback_query_id}
    if text is not None:
        payload['text'] = text
    if show_alert is not None:
        payload['show_alert'] = show_alert
    if url is not None:
        payload['url'] = url
    if cache_time is not None:
        payload['cache_time'] = cache_time
    return bool(await self._call('answerCallbackQuery', json_body=payload))
