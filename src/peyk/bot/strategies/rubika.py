"""Rubika-specific operation strategies, including file-upload emulation."""
from __future__ import annotations
from dataclasses import replace
from typing import Optional, Sequence
from peyk.platforms.rubika import RubikaClient
from peyk.types import Chat, ChatMember, File, Message, User
from peyk.types._convert import chat, message_base

def to_message(raw: object, bot: object) -> Message:
    """Performs the to message operation for the bot client.

Args:
    raw: Value used by this operation.
    bot: Value used by this operation.

Returns:
    Result produced by the bot operation."""
    return message_base(raw, bot=bot)

def _kwargs(kwargs: dict[str, object]) -> dict[str, object]:
    result = dict(kwargs)
    markup = result.pop('reply_markup', None)
    if markup is not None:
        if isinstance(markup, dict) and 'chat_keypad_type' in markup:
            result.update(markup)
        else:
            result['inline_keypad'] = markup
    return result

async def get_me(client: RubikaClient, bot: object) -> User:
    """Retrieves me from the bot API.

Args:
    client: Value used by this operation.
    bot: Value used by this operation.

Returns:
    Result produced by the bot operation."""
    raw = await client.get_me()
    return User(id=raw.bot_id, is_bot=True, first_name=raw.bot_title, username=raw.username, raw=raw)

async def send_message(client: RubikaClient, bot: object, chat_id: int | str, text: str, **kwargs: object) -> Message:
    """Sends message through the bot API.

Args:
    client: Value used by this operation.
    bot: Value used by this operation.
    chat_id: Identifier of the target chat.
    text: Text content supplied to the operation.

Returns:
    Result produced by the bot operation."""
    result = to_message(await client.send_message(str(chat_id), text, **_kwargs(kwargs)), bot)
    return replace(result, chat_id=chat_id) if result.chat_id is None else result

async def _media(client: RubikaClient, bot: object, chat_id: int | str, media: object, file_type: str, **kwargs: object) -> Message:
    if not isinstance(media, (bytes, bytearray)):
        if isinstance(media, str):
            return to_message(await client.send_file(str(chat_id), media, text=kwargs.pop('caption', None)), bot)
        raise TypeError('Rubika media emulation requires bytes or a file_id string')
    result = to_message(await client.upload_and_send_file(str(chat_id), bytes(media), file_type=file_type, text=kwargs.pop('caption', None), **_kwargs(kwargs)), bot)
    return replace(result, chat_id=chat_id) if result.chat_id is None else result

async def send_photo(client: RubikaClient, bot: object, chat_id: int | str, media: object, **kwargs: object) -> Message:
    """Sends photo through the bot API.

Args:
    client: Value used by this operation.
    bot: Value used by this operation.
    chat_id: Identifier of the target chat.
    media: Value used by this operation.

Returns:
    Result produced by the bot operation."""
    return await _media(client, bot, chat_id, media, 'Photo', **kwargs)

async def send_video(client: RubikaClient, bot: object, chat_id: int | str, media: object, **kwargs: object) -> Message:
    """Sends video through the bot API.

Args:
    client: Value used by this operation.
    bot: Value used by this operation.
    chat_id: Identifier of the target chat.
    media: Value used by this operation.

Returns:
    Result produced by the bot operation."""
    return await _media(client, bot, chat_id, media, 'Video', **kwargs)

async def send_audio(client: RubikaClient, bot: object, chat_id: int | str, media: object, **kwargs: object) -> Message:
    """Sends audio through the bot API.

Args:
    client: Value used by this operation.
    bot: Value used by this operation.
    chat_id: Identifier of the target chat.
    media: Value used by this operation.

Returns:
    Result produced by the bot operation."""
    return await _media(client, bot, chat_id, media, 'Music', **kwargs)

async def send_voice(client: RubikaClient, bot: object, chat_id: int | str, media: object, **kwargs: object) -> Message:
    """Sends voice through the bot API.

Args:
    client: Value used by this operation.
    bot: Value used by this operation.
    chat_id: Identifier of the target chat.
    media: Value used by this operation.

Returns:
    Result produced by the bot operation."""
    return await _media(client, bot, chat_id, media, 'Voice', **kwargs)

async def send_document(client: RubikaClient, bot: object, chat_id: int | str, media: object, **kwargs: object) -> Message:
    """Sends document through the bot API.

Args:
    client: Value used by this operation.
    bot: Value used by this operation.
    chat_id: Identifier of the target chat.
    media: Value used by this operation.

Returns:
    Result produced by the bot operation."""
    return await _media(client, bot, chat_id, media, 'File', **kwargs)

async def send_contact(client: RubikaClient, bot: object, chat_id: int | str, phone_number: str, first_name: str, **kwargs: object) -> Message:
    """Sends contact through the bot API.

Args:
    client: Value used by this operation.
    bot: Value used by this operation.
    chat_id: Identifier of the target chat.
    phone_number: Value used by this operation.
    first_name: Value used by this operation.

Returns:
    Result produced by the bot operation."""
    return to_message(await client.send_contact(str(chat_id), first_name, str(kwargs.pop('last_name', '')), phone_number, **_kwargs(kwargs)), bot)

async def send_location(client: RubikaClient, bot: object, chat_id: int | str, latitude: float, longitude: float, **kwargs: object) -> Message:
    """Sends location through the bot API.

Args:
    client: Value used by this operation.
    bot: Value used by this operation.
    chat_id: Identifier of the target chat.
    latitude: Value used by this operation.
    longitude: Value used by this operation.

Returns:
    Result produced by the bot operation."""
    return to_message(await client.send_location(str(chat_id), str(latitude), str(longitude), **_kwargs(kwargs)), bot)

async def send_poll(client: RubikaClient, bot: object, chat_id: int | str, question: str, options: Sequence[str], **kwargs: object) -> Message:
    """Sends poll through the bot API.

Args:
    client: Value used by this operation.
    bot: Value used by this operation.
    chat_id: Identifier of the target chat.
    question: Value used by this operation.
    options: Value used by this operation.

Returns:
    Result produced by the bot operation."""
    return to_message(await client.send_poll(str(chat_id), question, list(options)), bot)

async def edit_message_text(client: RubikaClient, bot: object, chat_id: int | str, message_id: int | str, text: str, **kwargs: object) -> Message:
    """Edits message text through the bot API.

Args:
    client: Value used by this operation.
    bot: Value used by this operation.
    chat_id: Identifier of the target chat.
    message_id: Identifier of the target message.
    text: Text content supplied to the operation.

Returns:
    Result produced by the bot operation."""
    await client.edit_message_text(str(chat_id), str(message_id), text)
    return Message(message_id=message_id, chat_id=chat_id, text=text, raw=None, bot=bot)

async def edit_message_reply_markup(client: RubikaClient, bot: object, chat_id: int | str, message_id: int | str, **kwargs: object) -> Message:
    """Edits message reply markup through the bot API.

Args:
    client: Value used by this operation.
    bot: Value used by this operation.
    chat_id: Identifier of the target chat.
    message_id: Identifier of the target message.

Returns:
    Result produced by the bot operation."""
    await client.edit_message_keypad(str(chat_id), str(message_id), inline_keypad=kwargs.get('reply_markup'))
    return Message(message_id=message_id, chat_id=chat_id, raw=None, bot=bot)

async def delete_message(client: RubikaClient, bot: object, chat_id: int | str, message_id: int | str) -> bool:
    """Removes message through the bot API.

Args:
    client: Value used by this operation.
    bot: Value used by this operation.
    chat_id: Identifier of the target chat.
    message_id: Identifier of the target message.

Returns:
    Result produced by the bot operation."""
    return await client.delete_message(str(chat_id), str(message_id))

async def forward_message(client: RubikaClient, bot: object, chat_id: int | str, from_chat_id: int | str, message_id: int | str) -> Message:
    """Performs the forward message operation for the bot client.

Args:
    client: Value used by this operation.
    bot: Value used by this operation.
    chat_id: Identifier of the target chat.
    from_chat_id: Value used by this operation.
    message_id: Identifier of the target message.

Returns:
    Result produced by the bot operation."""
    return to_message(await client.forward_message(str(from_chat_id), str(message_id), str(chat_id)), bot)

async def answer_callback_query(client: RubikaClient, bot: object, callback_query_id: str, *, text: Optional[str], show_alert: bool) -> bool:
    """Answers the callback query request through the bot API.

Args:
    client: Value used by this operation.
    bot: Value used by this operation.
    callback_query_id: Identifier of the callback query.
    text: Text content supplied to the operation.
    show_alert: Value used by this operation.

Returns:
    Result produced by the bot operation."""
    raise NotImplementedError('Rubika has no confirmed callback-answer operation')

async def send_chat_action(client: RubikaClient, bot: object, chat_id: int | str, action: str) -> bool:
    """Sends chat action through the bot API.

Args:
    client: Value used by this operation.
    bot: Value used by this operation.
    chat_id: Identifier of the target chat.
    action: Value used by this operation.

Returns:
    Result produced by the bot operation."""
    raise NotImplementedError('Rubika has no audited send-chat-action operation')

async def get_chat(client: RubikaClient, bot: object, chat_id: int | str) -> Chat:
    """Retrieves chat from the bot API.

Args:
    client: Value used by this operation.
    bot: Value used by this operation.
    chat_id: Identifier of the target chat.

Returns:
    Result produced by the bot operation."""
    return chat(await client.get_chat(str(chat_id)))

async def get_chat_member(client: RubikaClient, bot: object, chat_id: int | str, user_id: int) -> ChatMember:
    """Retrieves chat member from the bot API.

Args:
    client: Value used by this operation.
    bot: Value used by this operation.
    chat_id: Identifier of the target chat.
    user_id: Identifier of the target user.

Returns:
    Result produced by the bot operation."""
    raise NotImplementedError('Rubika has no audited get-chat-member operation')

async def ban_chat_member(client: RubikaClient, bot: object, chat_id: int | str, user_id: int) -> bool:
    """Performs the ban chat member operation for the bot client.

Args:
    client: Value used by this operation.
    bot: Value used by this operation.
    chat_id: Identifier of the target chat.
    user_id: Identifier of the target user.

Returns:
    Result produced by the bot operation."""
    return await client.ban_chat_member(str(chat_id), str(user_id))

async def unban_chat_member(client: RubikaClient, bot: object, chat_id: int | str, user_id: int) -> bool:
    """Performs the unban chat member operation for the bot client.

Args:
    client: Value used by this operation.
    bot: Value used by this operation.
    chat_id: Identifier of the target chat.
    user_id: Identifier of the target user.

Returns:
    Result produced by the bot operation."""
    return await client.unban_chat_member(str(chat_id), str(user_id))

async def get_file(client: RubikaClient, bot: object, file_id: str) -> File:
    """Retrieves file from the bot API.

Args:
    client: Value used by this operation.
    bot: Value used by this operation.
    file_id: Identifier of the file.

Returns:
    Result produced by the bot operation."""
    raw = await client.get_file(file_id)
    return File(id=getattr(raw, 'file_id', str(raw)), path=getattr(raw, 'file_path', None), name=getattr(raw, 'file_name', None), raw=raw)

async def download(client: RubikaClient, bot: object, file_id: str) -> bytes:
    """Performs the download operation for the bot client.

Args:
    client: Value used by this operation.
    bot: Value used by this operation.
    file_id: Identifier of the file.

Returns:
    Result produced by the bot operation."""
    url = await client.get_file(file_id)
    if not isinstance(url, str) or not url:
        raise ValueError('Rubika getFile returned no download URL')
    response = await client._session.request('GET', url)
    return response.body
