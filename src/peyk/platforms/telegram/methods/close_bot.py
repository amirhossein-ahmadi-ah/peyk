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

async def close_bot(self) -> bool:
    """Close the bot from the cloud Bot API server.
    
        This name intentionally avoids colliding with ``TelegramClient.close()``,
        which closes the local HTTP session.
        
    
    Returns:
        The operation result (``bool``).
    """
    result = await self._call('close')
    return bool(result)
