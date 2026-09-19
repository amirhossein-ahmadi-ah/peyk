"""Bale-specific operation strategies."""
from __future__ import annotations
from typing import Optional, Sequence
from peyk.platforms.bale import BaleClient
from peyk.types import Chat, ChatMember, File, Message, User
from peyk.types._convert import chat, message_base, user

def to_message(raw: object, bot: object) -> Message:
    """Performs the to message operation for the bot client.

Args:
    raw: Value used by this operation.
    bot: Value used by this operation.

Returns:
    Result produced by the bot operation."""
    return message_base(raw, bot=bot)

async def get_me(client: BaleClient, bot: object) -> User:
    """Retrieves me from the bot API.

Args:
    client: Value used by this operation.
    bot: Value used by this operation.

Returns:
    Result produced by the bot operation."""
    return user(await client.get_me())

async def send_message(client: BaleClient, bot: object, chat_id: int | str, text: str, **kwargs: object) -> Message:
    """Sends message through the bot API.

Args:
    client: Value used by this operation.
    bot: Value used by this operation.
    chat_id: Identifier of the target chat.
    text: Text content supplied to the operation.

Returns:
    Result produced by the bot operation."""
    return to_message(await client.send_message(chat_id, text, **kwargs), bot)

async def send_photo(client: BaleClient, bot: object, chat_id: int | str, media: object, **kwargs: object) -> Message:
    """Sends photo through the bot API.

Args:
    client: Value used by this operation.
    bot: Value used by this operation.
    chat_id: Identifier of the target chat.
    media: Value used by this operation.

Returns:
    Result produced by the bot operation."""
    return to_message(await client.send_photo(chat_id, media, **kwargs), bot)

async def send_video(client: BaleClient, bot: object, chat_id: int | str, media: object, **kwargs: object) -> Message:
    """Sends video through the bot API.

Args:
    client: Value used by this operation.
    bot: Value used by this operation.
    chat_id: Identifier of the target chat.
    media: Value used by this operation.

Returns:
    Result produced by the bot operation."""
    return to_message(await client.send_video(chat_id, media, **kwargs), bot)

async def send_audio(client: BaleClient, bot: object, chat_id: int | str, media: object, **kwargs: object) -> Message:
    """Sends audio through the bot API.

Args:
    client: Value used by this operation.
    bot: Value used by this operation.
    chat_id: Identifier of the target chat.
    media: Value used by this operation.

Returns:
    Result produced by the bot operation."""
    return to_message(await client.send_audio(chat_id, media, **kwargs), bot)

async def send_voice(client: BaleClient, bot: object, chat_id: int | str, media: object, **kwargs: object) -> Message:
    """Sends voice through the bot API.

Args:
    client: Value used by this operation.
    bot: Value used by this operation.
    chat_id: Identifier of the target chat.
    media: Value used by this operation.

Returns:
    Result produced by the bot operation."""
    return to_message(await client.send_voice(chat_id, media, **kwargs), bot)

async def send_document(client: BaleClient, bot: object, chat_id: int | str, media: object, **kwargs: object) -> Message:
    """Sends document through the bot API.

Args:
    client: Value used by this operation.
    bot: Value used by this operation.
    chat_id: Identifier of the target chat.
    media: Value used by this operation.

Returns:
    Result produced by the bot operation."""
    return to_message(await client.send_document(chat_id, media, **kwargs), bot)

async def send_contact(client: BaleClient, bot: object, chat_id: int | str, phone_number: str, first_name: str, **kwargs: object) -> Message:
    """Sends contact through the bot API.

Args:
    client: Value used by this operation.
    bot: Value used by this operation.
    chat_id: Identifier of the target chat.
    phone_number: Value used by this operation.
    first_name: Value used by this operation.

Returns:
    Result produced by the bot operation."""
    return to_message(await client.send_contact(chat_id, phone_number, first_name, **kwargs), bot)

async def send_location(client: BaleClient, bot: object, chat_id: int | str, latitude: float, longitude: float, **kwargs: object) -> Message:
    """Sends location through the bot API.

Args:
    client: Value used by this operation.
    bot: Value used by this operation.
    chat_id: Identifier of the target chat.
    latitude: Value used by this operation.
    longitude: Value used by this operation.

Returns:
    Result produced by the bot operation."""
    return to_message(await client.send_location(chat_id, latitude, longitude, **kwargs), bot)

async def send_poll(client: BaleClient, bot: object, chat_id: int | str, question: str, options: Sequence[str], **kwargs: object) -> Message:
    """Sends poll through the bot API.

Args:
    client: Value used by this operation.
    bot: Value used by this operation.
    chat_id: Identifier of the target chat.
    question: Value used by this operation.
    options: Value used by this operation.

Returns:
    Result produced by the bot operation."""
    return to_message(await client.send_poll(chat_id, question, options, **kwargs), bot)

async def edit_message_text(client: BaleClient, bot: object, chat_id: int | str, message_id: int | str, text: str, **kwargs: object) -> Message:
    """Edits message text through the bot API.

Args:
    client: Value used by this operation.
    bot: Value used by this operation.
    chat_id: Identifier of the target chat.
    message_id: Identifier of the target message.
    text: Text content supplied to the operation.

Returns:
    Result produced by the bot operation."""
    return to_message(await client.edit_message_text(chat_id, message_id, text, **kwargs), bot)

async def edit_message_reply_markup(client: BaleClient, bot: object, chat_id: int | str, message_id: int | str, **kwargs: object) -> Message:
    """Edits message reply markup through the bot API.

Args:
    client: Value used by this operation.
    bot: Value used by this operation.
    chat_id: Identifier of the target chat.
    message_id: Identifier of the target message.

Returns:
    Result produced by the bot operation."""
    return to_message(await client.edit_message_reply_markup(chat_id, message_id, **kwargs), bot)

async def delete_message(client: BaleClient, bot: object, chat_id: int | str, message_id: int | str) -> bool:
    """Removes message through the bot API.

Args:
    client: Value used by this operation.
    bot: Value used by this operation.
    chat_id: Identifier of the target chat.
    message_id: Identifier of the target message.

Returns:
    Result produced by the bot operation."""
    return await client.delete_message(chat_id, int(message_id))

async def forward_message(client: BaleClient, bot: object, chat_id: int | str, from_chat_id: int | str, message_id: int | str) -> Message:
    """Performs the forward message operation for the bot client.

Args:
    client: Value used by this operation.
    bot: Value used by this operation.
    chat_id: Identifier of the target chat.
    from_chat_id: Value used by this operation.
    message_id: Identifier of the target message.

Returns:
    Result produced by the bot operation."""
    return to_message(await client.forward_message(chat_id, from_chat_id, int(message_id)), bot)

async def answer_callback_query(client: BaleClient, bot: object, callback_query_id: str, *, text: Optional[str], show_alert: bool) -> bool:
    """Answers the callback query request through the bot API.

Args:
    client: Value used by this operation.
    bot: Value used by this operation.
    callback_query_id: Identifier of the callback query.
    text: Text content supplied to the operation.
    show_alert: Value used by this operation.

Returns:
    Result produced by the bot operation."""
    return await client.answer_callback_query(callback_query_id, text=text, show_alert=show_alert)

async def send_chat_action(client: BaleClient, bot: object, chat_id: int | str, action: str) -> bool:
    """Sends chat action through the bot API.

Args:
    client: Value used by this operation.
    bot: Value used by this operation.
    chat_id: Identifier of the target chat.
    action: Value used by this operation.

Returns:
    Result produced by the bot operation."""
    return await client.send_chat_action(chat_id, action)

async def get_chat(client: BaleClient, bot: object, chat_id: int | str) -> Chat:
    """Retrieves chat from the bot API.

Args:
    client: Value used by this operation.
    bot: Value used by this operation.
    chat_id: Identifier of the target chat.

Returns:
    Result produced by the bot operation."""
    return chat(await client.get_chat(chat_id))

async def get_chat_member(client: BaleClient, bot: object, chat_id: int | str, user_id: int) -> ChatMember:
    """Retrieves chat member from the bot API.

Args:
    client: Value used by this operation.
    bot: Value used by this operation.
    chat_id: Identifier of the target chat.
    user_id: Identifier of the target user.

Returns:
    Result produced by the bot operation."""
    raw = await client.get_chat_member(chat_id, user_id)
    raw_user = getattr(raw, 'user', None)
    return ChatMember(status=getattr(raw, 'status', ''), user=user(raw_user) if raw_user is not None else None, raw=raw)

async def ban_chat_member(client: BaleClient, bot: object, chat_id: int | str, user_id: int) -> bool:
    """Performs the ban chat member operation for the bot client.

Args:
    client: Value used by this operation.
    bot: Value used by this operation.
    chat_id: Identifier of the target chat.
    user_id: Identifier of the target user.

Returns:
    Result produced by the bot operation."""
    return await client.ban_chat_member(chat_id, user_id)

async def unban_chat_member(client: BaleClient, bot: object, chat_id: int | str, user_id: int) -> bool:
    """Performs the unban chat member operation for the bot client.

Args:
    client: Value used by this operation.
    bot: Value used by this operation.
    chat_id: Identifier of the target chat.
    user_id: Identifier of the target user.

Returns:
    Result produced by the bot operation."""
    return await client.unban_chat_member(chat_id, user_id)

async def get_file(client: BaleClient, bot: object, file_id: str) -> File:
    """Retrieves file from the bot API.

Args:
    client: Value used by this operation.
    bot: Value used by this operation.
    file_id: Identifier of the file.

Returns:
    Result produced by the bot operation."""
    raw = await client.get_file(file_id)
    return File(id=getattr(raw, 'file_id', str(raw)), path=getattr(raw, 'file_path', None), name=getattr(raw, 'file_name', None), size=getattr(raw, 'file_size', None), raw=raw)

async def download(client: BaleClient, bot: object, file_id: str) -> bytes:
    """Performs the download operation for the bot client.

Args:
    client: Value used by this operation.
    bot: Value used by this operation.
    file_id: Identifier of the file.

Returns:
    Result produced by the bot operation."""
    file = await client.get_file(file_id)
    if file.file_path is None:
        raise ValueError('Bale getFile returned no file_path')
    base = client._base_url.rsplit('/bot', 1)[0]
    response = await client._session.request('GET', f'{base}/file/bot{client._token}/{file.file_path}')
    return response.body
