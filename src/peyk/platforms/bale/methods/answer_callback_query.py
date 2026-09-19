from __future__ import annotations
from ..errors import BaleAPIError
from peyk.transport import FilePayload
from typing import Any, Dict, Optional

async def answer_callback_query(self, callback_query_id: str, *, text: Optional[str]=None, show_alert: Optional[bool]=None) -> bool:
    """Answers the callback query request through the Bale API.

Args:
    callback_query_id: Identifier of the callback query.
    text: Text content supplied to the operation.
    show_alert: Value used by this operation.

Returns:
    Result produced by the Bale operation."""
    'Send a response to an incoming callback query.\n    \n            Must be called for every callback query, even if no feedback\n            is needed -- the client keeps the button in a "pending" state\n            until the bot responds.\n    \n            Per docs.bale.ai (Khordad 1404 update): check the first character\n            of `callback_query_id` -- if it starts with `1`, the user is on\n            an older client version that does not support this feature.\n    \n            `text`: 0-200 characters, shown as a notification or alert.\n            `show_alert`: if True, shows as an alert dialog; otherwise as\n            a notification at the top.\n            \n    \n    Args:\n        callback_query_id: Value of the declared parameter type.\n        text: Value of the declared parameter type.\n        show_alert: Value of the declared parameter type.\n    \n    \n    Returns:\n        The operation result (``bool``).\n    '
    payload: Dict[str, object] = {'callback_query_id': callback_query_id}
    if text is not None:
        payload['text'] = text
    if show_alert is not None:
        payload['show_alert'] = show_alert
    return bool(await self._call('answerCallbackQuery', json_body=payload))
