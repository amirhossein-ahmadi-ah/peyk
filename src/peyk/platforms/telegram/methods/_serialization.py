"""Shared private serializers for T1-T5 Telegram method modules."""

from typing import Any, Dict, List, Mapping, Optional, Sequence, Union
from ..models import LinkPreviewOptions, MessageEntity, ReplyParameters

EntitiesInput = Sequence[Union[MessageEntity, Mapping[str, object]]]

def _serialize_entities(entities: Optional[EntitiesInput]) -> Optional[List[Dict[str, object]]]:
    if entities is None:
        return None
    return [e.to_dict() if isinstance(e, MessageEntity) else dict(e) for e in entities]

def _serialize_reply_parameters(value: Optional[Union[ReplyParameters, Mapping[str, object]]]) -> Optional[Dict[str, object]]:
    if value is None:
        return None
    return value.to_dict() if isinstance(value, ReplyParameters) else dict(value)

def _serialize_link_preview(value: Optional[Union[LinkPreviewOptions, Mapping[str, object]]]) -> Optional[Dict[str, object]]:
    if value is None:
        return None
    return value.to_dict() if isinstance(value, LinkPreviewOptions) else dict(value)
