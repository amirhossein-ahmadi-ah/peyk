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

def _extract_retry_hint(self, response: object) -> Optional[float]:
    """Call the Telegram Bot API method ``_extract_retry_hint``.

Args:
    response: Value passed to the Telegram API method.

Returns:
    The parsed Telegram API result.

Raises:
    TelegramAPIError: If Telegram rejects the request.
"""
    parameters = response.get('parameters') if isinstance(response, dict) else None
    retry_after = parameters.get('retry_after') if isinstance(parameters, dict) else None
    return float(retry_after) if retry_after is not None else None
