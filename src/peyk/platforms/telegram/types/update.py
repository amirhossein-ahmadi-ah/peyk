from __future__ import annotations
from dataclasses import dataclass, field
import re
from typing import Any, Dict, List, Mapping, Optional, Sequence, Union
from .chat_join_request import ChatJoinRequest
from .chat_member_updated import ChatMemberUpdated
from .message import Message

@dataclass
class Update:
    """This object represents an incoming update.
At most one of the optional fields can be present in any given update.

Attributes:
    update_id: The update's unique identifier. Update identifiers start from a certain positive number and increase sequentially. This identifier becomes especially handy if you're using webhooks, since it allows you to ignore repeated updates or to restore the correct update sequence, should they get out of order. If there are no new updates for at least a week, then identifier of the next update will be chosen randomly instead of sequentially.
    message: New incoming message of any kind - text, photo, sticker, etc.
    edited_message: New version of a message that is known to the bot and was edited. This update may at times be triggered by changes to message fields that are either unavailable or not actively used by your bot.
    channel_post: New incoming channel post of any kind - text, photo, sticker, etc.
    edited_channel_post: New version of a channel post that is known to the bot and was edited. This update may at times be triggered by changes to message fields that are either unavailable or not actively used by your bot.
    business_connection: The bot was connected to or disconnected from a business account, or a user edited an existing connection with the bot
    business_message: New message from a connected business account
    edited_business_message: New version of a message from a connected business account
    deleted_business_messages: Messages were deleted from a connected business account
    guest_message: New guest message. The bot can use the field Message.guest_query_id and the method answerGuestQuery to send a message in response.
    message_reaction: A reaction to a message was changed by a user. The bot must be an administrator in the chat and must explicitly specify "message_reaction" in the list of allowed_updates to receive these updates. The update isn't received for reactions set by bots.
    message_reaction_count: Reactions to a message with anonymous reactions were changed. The bot must be an administrator in the chat and must explicitly specify "message_reaction_count" in the list of allowed_updates to receive these updates. The updates are grouped and can be sent with delay up to a few minutes.
    inline_query: New incoming inline query
    chosen_inline_result: The result of an inline query that was chosen by a user and sent to their chat partner. Please see our documentation on the feedback collecting for details on how to enable these updates for your bot.
    callback_query: New incoming callback query
    shipping_query: New incoming shipping query. Only for invoices with flexible price.
    pre_checkout_query: New incoming pre-checkout query. Contains full information about checkout.
    purchased_paid_media: A user purchased paid media with a non-empty payload sent by the bot in a non-channel chat
    poll: New poll state. Bots receive only updates about manually stopped polls and polls, which are sent by the bot.
    poll_answer: A user changed their answer in a non-anonymous poll. Bots receive new votes only in polls that were sent by the bot itself.
    my_chat_member: The bot's chat member status was updated in a chat. For private chats, this update is received only when the bot is blocked or unblocked by the user.
    chat_member: A chat member's status was updated in a chat. The bot must be an administrator in the chat and must explicitly specify "chat_member" in the list of allowed_updates to receive these updates.
    chat_join_request: A request to join the chat has been sent. The bot must have the can_invite_users administrator right in the chat to receive these updates.
    chat_boost: A chat boost was added or changed. The bot must be an administrator in the chat to receive these updates.
    removed_chat_boost: A boost was removed from a chat. The bot must be an administrator in the chat to receive these updates.
    managed_bot: A new bot was created to be managed by the bot, or token or owner of a managed bot was changed
    subscription: User payment subscription has changed"""
    update_id: int
    message: Optional[Message] = None
    edited_message: Optional[Message] = None
    channel_post: Optional[Message] = None
    edited_channel_post: Optional[Message] = None
    business_connection: Optional[object] = None
    business_message: Optional[Message] = None
    edited_business_message: Optional[Message] = None
    deleted_business_messages: Optional[object] = None
    message_reaction: Optional[object] = None
    message_reaction_count: Optional[object] = None
    inline_query: Optional[InlineQuery] = None
    chosen_inline_result: Optional[ChosenInlineResult] = None
    callback_query: Optional[CallbackQuery] = None
    shipping_query: Optional[object] = None
    pre_checkout_query: Optional[object] = None
    purchased_paid_media: Optional[object] = None
    poll: Optional[object] = None
    poll_answer: Optional[object] = None
    my_chat_member: Optional[ChatMemberUpdated] = None
    chat_member: Optional[ChatMemberUpdated] = None
    chat_join_request: Optional[ChatJoinRequest] = None
    chat_boost: Optional[object] = None
    removed_chat_boost: Optional[object] = None

    @classmethod
    def from_dict(cls, data: dict) -> 'Update':
        """Parse a Telegram API mapping into this type.

Args:
    data: Raw Telegram API mapping, or ``None``.

Returns:
    Parsed type instance, or ``None`` when ``data`` is ``None``."""
        from ..models import CallbackQuery
        from ..models import ChosenInlineResult
        from ..models import InlineQuery
        return cls(update_id=data['update_id'], message=Message.from_dict(data.get('message')), edited_message=Message.from_dict(data.get('edited_message')), channel_post=Message.from_dict(data.get('channel_post')), edited_channel_post=Message.from_dict(data.get('edited_channel_post')), business_connection=data.get('business_connection'), business_message=Message.from_dict(data.get('business_message')), edited_business_message=Message.from_dict(data.get('edited_business_message')), deleted_business_messages=data.get('deleted_business_messages'), message_reaction=data.get('message_reaction'), message_reaction_count=data.get('message_reaction_count'), inline_query=InlineQuery.from_dict(data.get('inline_query')), chosen_inline_result=ChosenInlineResult.from_dict(data.get('chosen_inline_result')), callback_query=CallbackQuery.from_dict(data.get('callback_query')), shipping_query=data.get('shipping_query'), pre_checkout_query=data.get('pre_checkout_query'), purchased_paid_media=data.get('purchased_paid_media'), poll=data.get('poll'), poll_answer=data.get('poll_answer'), my_chat_member=ChatMemberUpdated.from_dict(data.get('my_chat_member')), chat_member=ChatMemberUpdated.from_dict(data.get('chat_member')), chat_join_request=ChatJoinRequest.from_dict(data.get('chat_join_request')), chat_boost=data.get('chat_boost'), removed_chat_boost=data.get('removed_chat_boost'))

    @classmethod
    def list_from_result(cls, data: Optional[List[dict]]) -> List['Update']:
        """Provides the list from result operation for the Telegram integration.

Args:
    data: Value used by this operation.

Returns:
    Result produced by the operation."""
        "Parse the array ``getUpdates`` returns from a raw ``result`` list.\n        \n        Args:\n            data: Value of the declared parameter type.\n        \n        \n        Returns:\n            The operation result (``List['Update']``).\n        "
        return [cls.from_dict(item) for item in data or []]
