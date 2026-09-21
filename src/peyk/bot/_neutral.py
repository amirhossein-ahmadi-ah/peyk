"""Conversion helpers from audited platform models to neutral types."""
from __future__ import annotations
from typing import Optional
from peyk.types import Chat, ChatType, ContentType, Message, User

def chat_type(value: Optional[str]) -> ChatType:
    """Performs the chat type operation for the bot client.

Args:
    value: Value used by this operation.

Returns:
    Result produced by the bot operation."""
    if value == 'private':
        return ChatType.PRIVATE
    if value in {'group', 'supergroup'}:
        return ChatType.GROUP
    if value == 'channel':
        return ChatType.CHANNEL
    return ChatType.UNKNOWN

def user(raw: object) -> User:
    """Performs the user operation for the bot client.

Args:
    raw: Value used by this operation.

Returns:
    Result produced by the bot operation."""
    return User(id=getattr(raw, 'id'), is_bot=bool(getattr(raw, 'is_bot', False)), first_name=getattr(raw, 'first_name', '') or '', last_name=getattr(raw, 'last_name', None), username=getattr(raw, 'username', None), language_code=getattr(raw, 'language_code', None), raw=raw)

def chat(raw: object) -> Chat:
    """Performs the chat operation for the bot client.

Args:
    raw: Value used by this operation.

Returns:
    Result produced by the bot operation."""
    return Chat(id=getattr(raw, 'id', getattr(raw, 'chat_id', '')), type=chat_type(getattr(raw, 'type', getattr(raw, 'chat_type', None))), title=getattr(raw, 'title', None), username=getattr(raw, 'username', None), language_code=getattr(raw, 'language_code', None), raw=raw)

def content_type(raw: object) -> ContentType:
    """Performs the content type operation for the bot client.

Args:
    raw: Value used by this operation.

Returns:
    Result produced by the bot operation."""
    if getattr(raw, 'text', None) is not None:
        return ContentType.TEXT
    for attr, kind in (('photo', ContentType.PHOTO), ('video', ContentType.VIDEO), ('audio', ContentType.AUDIO), ('voice', ContentType.VOICE), ('document', ContentType.DOCUMENT), ('sticker', ContentType.STICKER), ('animation', ContentType.ANIMATION), ('contact', ContentType.CONTACT), ('location', ContentType.LOCATION), ('poll', ContentType.POLL), ('venue', ContentType.VENUE), ('new_chat_members', ContentType.NEW_CHAT_MEMBERS), ('left_chat_member', ContentType.LEFT_CHAT_MEMBER), ('successful_payment', ContentType.SUCCESSFUL_PAYMENT)):
        if getattr(raw, attr, None) is not None:
            return kind
    return ContentType.TEXT if getattr(raw, 'caption', None) is not None else ContentType.UNKNOWN

def message_base(raw: object, *, bot: object, chat_override: Optional[Chat]=None) -> Message:
    """Performs the message base operation for the bot client.

Args:
    raw: Value used by this operation.
    bot: Value used by this operation.
    chat_override: Value used by this operation.

Returns:
    Result produced by the bot operation."""
    raw_chat = getattr(raw, 'chat', None)
    normalized_chat = chat_override or (chat(raw_chat) if raw_chat is not None else None)
    sender = getattr(raw, 'from_', None)
    if sender is None:
        sender = getattr(raw, 'sender_id', None)
    from_user = user(sender) if sender is not None and (not isinstance(sender, (str, int))) else User(id=sender, is_bot=False, first_name='', raw=sender) if sender is not None else None
    reply_to_msg = getattr(raw, 'reply_to_message', None)
    reply_to_id = getattr(raw, 'reply_to_message_id', None)
    if reply_to_id is None and reply_to_msg is not None:
        reply_to_id = getattr(reply_to_msg, 'message_id', None)
    
    normalized_reply = None
    if reply_to_msg is not None:
        normalized_reply = Message(message_id=getattr(reply_to_msg, 'message_id', None), chat_id=normalized_chat.id if normalized_chat else None, raw=reply_to_msg, from_user=from_user, chat=normalized_chat, content_type=content_type(reply_to_msg), reply_to_message_id=getattr(reply_to_msg, 'reply_to_message_id', None) or getattr(getattr(reply_to_msg, 'reply_to_message', None), 'message_id', None), media=next((getattr(reply_to_msg, name) for name in ('photo', 'video', 'audio', 'voice', 'document', 'sticker', 'animation', 'contact', 'location', 'poll', 'venue') if getattr(reply_to_msg, name, None) is not None), None), bot=bot)
    
    return Message(message_id=getattr(raw, 'message_id', None), chat_id=normalized_chat.id if normalized_chat else None, chat_type=normalized_chat.type.value if normalized_chat else None, sender_id=from_user.id if from_user else None, text=getattr(raw, 'text', None) if getattr(raw, 'text', None) is not None else getattr(raw, 'caption', None), date=getattr(raw, 'date', getattr(raw, 'time', None)), is_edited=bool(getattr(raw, 'is_edited', False) or getattr(raw, 'edit_date', None) is not None), reply_to_message_id=reply_to_id, reply_to_message=normalized_reply, media=next((getattr(raw, name) for name in ('photo', 'video', 'audio', 'voice', 'document', 'sticker', 'animation', 'contact', 'location', 'poll', 'venue') if getattr(raw, name, None) is not None), None), new_chat_members=[u.id for u in getattr(raw, 'new_chat_members', []) or []], left_chat_member=getattr(getattr(raw, 'left_chat_member', None), 'id', None), successful_payment=getattr(raw, 'successful_payment', None), raw=raw, from_user=from_user, chat=normalized_chat, content_type=content_type(raw), bot=bot)
