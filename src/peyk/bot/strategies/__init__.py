"""Platform strategy registry used by :mod:`peyk.bot`."""
from __future__ import annotations
from typing import Awaitable, Callable, TypeVar
from peyk.platforms.bale import BaleClient
from peyk.platforms.telegram import TelegramClient
from peyk.platforms.rubika import RubikaClient
from peyk.types import Chat, ChatMember, File, Message, User
from . import bale, rubika, telegram
TELEGRAM_CLIENT = TelegramClient
BALE_CLIENT = BaleClient
RUBIKA_CLIENT = RubikaClient
from typing import Callable, Awaitable, Sequence
_OPERATION_MODULES = {'telegram': telegram, 'bale': bale, 'rubika': rubika}

def _module(bot: object) -> object:
    return _OPERATION_MODULES[bot.platform]

async def get_me(bot: object) -> User:
    """Retrieves me from the bot API.

Args:
    bot: Value used by this operation.

Returns:
    Result produced by the bot operation."""
    return await _module(bot).get_me(bot.client, bot)

async def send_message(bot: object, chat_id: int | str, text: str, **kwargs: object) -> Message:
    """Sends message through the bot API.

Args:
    bot: Value used by this operation.
    chat_id: Identifier of the target chat.
    text: Text content supplied to the operation.

Returns:
    Result produced by the bot operation."""
    return await _module(bot).send_message(bot.client, bot, chat_id, text, **kwargs)

async def send_photo(bot: object, chat_id: int | str, media: object, **kwargs: object) -> Message:
    """Sends photo through the bot API.

Args:
    bot: Value used by this operation.
    chat_id: Identifier of the target chat.
    media: Value used by this operation.

Returns:
    Result produced by the bot operation."""
    return await _module(bot).send_photo(bot.client, bot, chat_id, media, **kwargs)

async def send_video(bot: object, chat_id: int | str, media: object, **kwargs: object) -> Message:
    """Sends video through the bot API.

Args:
    bot: Value used by this operation.
    chat_id: Identifier of the target chat.
    media: Value used by this operation.

Returns:
    Result produced by the bot operation."""
    return await _module(bot).send_video(bot.client, bot, chat_id, media, **kwargs)

async def send_audio(bot: object, chat_id: int | str, media: object, **kwargs: object) -> Message:
    """Sends audio through the bot API.

Args:
    bot: Value used by this operation.
    chat_id: Identifier of the target chat.
    media: Value used by this operation.

Returns:
    Result produced by the bot operation."""
    return await _module(bot).send_audio(bot.client, bot, chat_id, media, **kwargs)

async def send_voice(bot: object, chat_id: int | str, media: object, **kwargs: object) -> Message:
    """Sends voice through the bot API.

Args:
    bot: Value used by this operation.
    chat_id: Identifier of the target chat.
    media: Value used by this operation.

Returns:
    Result produced by the bot operation."""
    return await _module(bot).send_voice(bot.client, bot, chat_id, media, **kwargs)

async def send_document(bot: object, chat_id: int | str, media: object, **kwargs: object) -> Message:
    """Sends document through the bot API.

Args:
    bot: Value used by this operation.
    chat_id: Identifier of the target chat.
    media: Value used by this operation.

Returns:
    Result produced by the bot operation."""
    return await _module(bot).send_document(bot.client, bot, chat_id, media, **kwargs)

async def send_contact(bot: object, chat_id: int | str, phone: str, first: str, **kwargs: object) -> Message:
    """Sends contact through the bot API.

Args:
    bot: Value used by this operation.
    chat_id: Identifier of the target chat.
    phone: Value used by this operation.
    first: Value used by this operation.

Returns:
    Result produced by the bot operation."""
    return await _module(bot).send_contact(bot.client, bot, chat_id, phone, first, **kwargs)

async def send_location(bot: object, chat_id: int | str, lat: float, lon: float, **kwargs: object) -> Message:
    """Sends location through the bot API.

Args:
    bot: Value used by this operation.
    chat_id: Identifier of the target chat.
    lat: Value used by this operation.
    lon: Value used by this operation.

Returns:
    Result produced by the bot operation."""
    return await _module(bot).send_location(bot.client, bot, chat_id, lat, lon, **kwargs)

async def send_poll(bot: object, chat_id: int | str, q: str, options: Sequence[str], **kwargs: object) -> Message:
    """Sends poll through the bot API.

Args:
    bot: Value used by this operation.
    chat_id: Identifier of the target chat.
    q: Value used by this operation.
    options: Value used by this operation.

Returns:
    Result produced by the bot operation."""
    return await _module(bot).send_poll(bot.client, bot, chat_id, q, options, **kwargs)

async def edit_message_text(bot: object, chat_id: int | str, mid: int | str, text: str, **kwargs: object) -> Message:
    """Edits message text through the bot API.

Args:
    bot: Value used by this operation.
    chat_id: Identifier of the target chat.
    mid: Value used by this operation.
    text: Text content supplied to the operation.

Returns:
    Result produced by the bot operation."""
    return await _module(bot).edit_message_text(bot.client, bot, chat_id, mid, text, **kwargs)

async def edit_message_reply_markup(bot: object, chat_id: int | str, mid: int | str, **kwargs: object) -> Message:
    """Edits message reply markup through the bot API.

Args:
    bot: Value used by this operation.
    chat_id: Identifier of the target chat.
    mid: Value used by this operation.

Returns:
    Result produced by the bot operation."""
    return await _module(bot).edit_message_reply_markup(bot.client, bot, chat_id, mid, **kwargs)

async def delete_message(bot: object, chat_id: int | str, mid: int | str) -> bool:
    """Removes message through the bot API.

Args:
    bot: Value used by this operation.
    chat_id: Identifier of the target chat.
    mid: Value used by this operation.

Returns:
    Result produced by the bot operation."""
    return await _module(bot).delete_message(bot.client, bot, chat_id, mid)

async def forward_message(bot: object, chat_id: int | str, from_chat: int | str, mid: int | str) -> Message:
    """Performs the forward message operation for the bot client.

Args:
    bot: Value used by this operation.
    chat_id: Identifier of the target chat.
    from_chat: Value used by this operation.
    mid: Value used by this operation.

Returns:
    Result produced by the bot operation."""
    return await _module(bot).forward_message(bot.client, bot, chat_id, from_chat, mid)

async def answer_callback_query(bot: object, qid: str, *, text: str | None, show_alert: bool) -> bool:
    """Answers the callback query request through the bot API.

Args:
    bot: Value used by this operation.
    qid: Value used by this operation.
    text: Text content supplied to the operation.
    show_alert: Value used by this operation.

Returns:
    Result produced by the bot operation."""
    return await _module(bot).answer_callback_query(bot.client, bot, qid, text=text, show_alert=show_alert)

async def send_chat_action(bot: object, chat_id: int | str, action: str) -> bool:
    """Sends chat action through the bot API.

Args:
    bot: Value used by this operation.
    chat_id: Identifier of the target chat.
    action: Value used by this operation.

Returns:
    Result produced by the bot operation."""
    return await _module(bot).send_chat_action(bot.client, bot, chat_id, action)

async def get_chat(bot: object, chat_id: int | str) -> Chat:
    """Retrieves chat from the bot API.

Args:
    bot: Value used by this operation.
    chat_id: Identifier of the target chat.

Returns:
    Result produced by the bot operation."""
    return await _module(bot).get_chat(bot.client, bot, chat_id)

async def get_chat_member(bot: object, chat_id: int | str, uid: int) -> ChatMember:
    """Retrieves chat member from the bot API.

Args:
    bot: Value used by this operation.
    chat_id: Identifier of the target chat.
    uid: Value used by this operation.

Returns:
    Result produced by the bot operation."""
    return await _module(bot).get_chat_member(bot.client, bot, chat_id, uid)

async def get_chat_administrators(bot: object, chat_id: int | str) -> list[ChatMember]:
    """Retrieves the administrator list for a chat from the bot API.

Args:
    bot: Value used by this operation.
    chat_id: Identifier of the target chat.

Returns:
    Result produced by the bot operation."""
    return await _module(bot).get_chat_administrators(bot.client, bot, chat_id)

async def ban_chat_member(bot: object, chat_id: int | str, uid: int) -> bool:
    """Performs the ban chat member operation for the bot client.

Args:
    bot: Value used by this operation.
    chat_id: Identifier of the target chat.
    uid: Value used by this operation.

Returns:
    Result produced by the bot operation."""
    return await _module(bot).ban_chat_member(bot.client, bot, chat_id, uid)

async def unban_chat_member(bot: object, chat_id: int | str, uid: int) -> bool:
    """Performs the unban chat member operation for the bot client.

Args:
    bot: Value used by this operation.
    chat_id: Identifier of the target chat.
    uid: Value used by this operation.

Returns:
    Result produced by the bot operation."""
    return await _module(bot).unban_chat_member(bot.client, bot, chat_id, uid)

async def get_file(bot: object, file_id: str) -> File:
    """Retrieves file from the bot API.

Args:
    bot: Value used by this operation.
    file_id: Identifier of the file.

Returns:
    Result produced by the bot operation."""
    return await _module(bot).get_file(bot.client, bot, file_id)

async def download(bot: object, file_id: str) -> bytes:
    """Performs the download operation for the bot client.

Args:
    bot: Value used by this operation.
    file_id: Identifier of the file.

Returns:
    Result produced by the bot operation."""
    return await _module(bot).download(bot.client, bot, file_id)
from .send_media_group import send_media_group
