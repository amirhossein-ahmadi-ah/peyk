from __future__ import annotations
from typing import Any, Dict, List, Mapping, Optional, Sequence, Union
from peyk.transport import FilePayload
from ..models import *
ChatId = Union[int, str]
EntitiesInput = Sequence[Union[MessageEntity, Mapping[str, object]]]
MediaInput = Union[str, bytes, FilePayload]

async def delete_webhook(self, *, drop_pending_updates: Optional[bool]=None) -> bool:
    """Use this method to remove webhook integration if you decide to switch back to getUpdates. Returns True on success.

Args:
    drop_pending_updates: Pass True to drop all pending updates

Returns:
    bool: Result returned by Telegram on successful execution."""
    payload: Dict[str, object] = {}
    if drop_pending_updates is not None:
        payload['drop_pending_updates'] = drop_pending_updates
    return bool(await self._call('deleteWebhook', json_body=payload))
