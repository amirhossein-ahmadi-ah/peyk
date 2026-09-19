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

def _resolve_sticker_ref(value: object, index: int, files: Dict[str, FilePayload]) -> str:
    """Resolve a sticker input to a string reference, registering uploads."""
    if isinstance(value, str):
        return value
    attach_name = f'file{index}_sticker'
    from ..client import TelegramClient
    files[attach_name] = TelegramClient._as_file_payload(value, default_filename=f'sticker_{index}.webp')
    return f'attach://{attach_name}'
