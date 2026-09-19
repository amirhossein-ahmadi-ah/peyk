from __future__ import annotations
from collections.abc import Sequence
from typing import Protocol
from peyk.types import Message

class _BotClient(Protocol):

    async def send_media_group(self, chat_id: int | str, media: Sequence[object], **kwargs: object) -> list[object]:
        """Sends media group through the bot API.

Args:
    chat_id: Identifier of the target chat.
    media: Value used by this operation.

Returns:
    Result produced by the bot operation."""
        ...

async def send_media_group(bot: object, chat_id: int | str, media: Sequence[object], **kwargs: object) -> list[Message]:
    """Delegate an audited media-group request to the active native client."""
    client = getattr(bot, 'client')
    result = await getattr(client, 'send_media_group')(chat_id, media, **kwargs)
    return [item if isinstance(item, Message) else Message(raw=item) for item in result]
