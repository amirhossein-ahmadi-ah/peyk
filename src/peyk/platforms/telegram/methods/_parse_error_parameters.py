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

def _parse_error_parameters(self, parameters: object) -> object:
    """Call the Telegram Bot API method ``_parse_error_parameters``.

Args:
    parameters: Value passed to the Telegram API method.

Returns:
    The parsed Telegram API result.

Raises:
    TelegramAPIError: If Telegram rejects the request.
"""
    return ResponseParameters.from_dict(parameters)
