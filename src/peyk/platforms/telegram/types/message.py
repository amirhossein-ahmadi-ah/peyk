from __future__ import annotations
from dataclasses import dataclass, field
import re
from typing import Any, Dict, List, Mapping, Optional, Sequence, Union
from .animation import Animation
from .audio import Audio
from .chat import Chat
from .contact import Contact
from .dice import Dice
from .document import Document
from .external_reply_info import ExternalReplyInfo
from .live_photo import LivePhoto
from .location import Location
from .message_entity import MessageEntity
from .photo_size import PhotoSize
from .poll import Poll
from .text_quote import TextQuote
from .user import User
from .venue import Venue
from .video import Video
from .video_note import VideoNote
from .voice import Voice

@dataclass
class Message:
    """This object represents a message.

Attributes:
    message_id: Unique message identifier inside this chat; 0 for ephemeral messages. In specific instances (e.g., a message containing a video sent to a big chat), the server might automatically schedule a message instead of sending it immediately. In such cases, this field will be 0 and the relevant message will be unusable until it is actually sent.
    date: Date the message was sent in Unix time. It is always a positive number, representing a valid date.
    chat: Chat the message belongs to
    message_thread_id: Unique identifier of a message thread or forum topic to which the message belongs; for supergroups and private chats only
    direct_messages_topic: Information about the direct messages chat topic that contains the message
    from: Sender of the message; may be empty for messages sent to channels. For backward compatibility, if the message was sent on behalf of a chat, the field contains a fake sender user in non-channel chats.
    sender_chat: Sender of the message when sent on behalf of a chat. For example, the supergroup itself for messages sent by its anonymous administrators or a linked channel for messages automatically forwarded to the channel's discussion group. For backward compatibility, if the message was sent on behalf of a chat, the field from contains a fake sender user in non-channel chats.
    sender_boost_count: If the sender of the message boosted the chat, the number of boosts added by the user
    sender_business_bot: The bot that actually sent the message on behalf of the business account. Available only for outgoing messages sent on behalf of the connected business account.
    sender_tag: Tag or custom title of the sender of the message; for supergroups only
    guest_query_id: The unique identifier for the guest query. Use this identifier with the method answerGuestQuery to send a response message. If non-empty, the message belongs to the chat where the guest bot was summoned, which may not coincide with other existing bot chats sharing the same identifier.
    business_connection_id: Unique identifier of the business connection from which the message was received. If non-empty, the message belongs to a chat of the corresponding business account that is independent from any potential bot chat which might share the same identifier.
    forward_origin: Information about the original message for forwarded messages
    is_topic_message: True, if the message is sent to a topic in a forum supergroup or a private chat with the bot
    is_automatic_forward: True, if the message is a channel post that was automatically forwarded to the connected discussion group
    reply_to_message: For replies in the same chat and message thread, the original message. Note that the Message object in this field will not contain further reply_to_message fields even if it itself is a reply. If the message is a reply to an ephemeral message, then this field may be omitted.
    external_reply: Information about the message that is being replied to, which may come from another chat or forum topic
    quote: For replies that quote part of the original message, the quoted part of the message
    reply_to_story: For replies to a story, the original story
    reply_to_checklist_task_id: Identifier of the specific checklist task that is being replied to
    reply_to_poll_option_id: Persistent identifier of the specific poll option that is being replied to
    via_bot: Bot through which the message was sent
    guest_bot_caller_user: For a message sent by a guest bot, this is the user whose original message triggered the bot's response
    guest_bot_caller_chat: For a message sent by a guest bot, this is the chat whose original message triggered the bot's response
    edit_date: Date the message was last edited in Unix time
    has_protected_content: True, if the message can't be forwarded
    is_from_offline: True, if the message was sent by an implicit action, for example, as an away or a greeting business message, or as a scheduled message
    is_paid_post: True, if the message is a paid post. Note that such posts must not be deleted for 24 hours to receive the payment and can't be edited.
    media_group_id: The unique identifier inside this chat of a media message group this message belongs to
    author_signature: Signature of the post author for messages in channels, or the custom title of an anonymous group administrator
    paid_star_count: The number of Telegram Stars that were paid by the sender of the message to send it
    text: For text messages, the actual UTF-8 text of the message
    entities: For text messages, special entities like usernames, URLs, bot commands, etc. that appear in the text
    link_preview_options: Options used for link preview generation for the message, if it is a text message and link preview options were changed
    suggested_post_info: Information about suggested post parameters if the message is a suggested post in a channel direct messages chat. If the message is an approved or declined suggested post, then it can't be edited.
    effect_id: Unique identifier of the message effect added to the message
    animation: Message is an animation, information about the animation. For backward compatibility, when this field is set, the document field will also be set.
    audio: Message is an audio file, information about the file
    document: Message is a general file, information about the file
    live_photo: Message is a live photo, information about the live photo. For backward compatibility, when this field is set, the photo field will also be set.
    paid_media: Message contains paid media; information about the paid media
    photo: Message is a photo, available sizes of the photo
    sticker: Message is a sticker, information about the sticker
    story: Message is a forwarded story
    video: Message is a video, information about the video
    video_note: Message is a video note, information about the video message
    voice: Message is a voice message, information about the file
    caption: Caption for the animation, audio, document, paid media, photo, video or voice
    caption_entities: For messages with a caption, special entities like usernames, URLs, bot commands, etc. that appear in the caption
    show_caption_above_media: True, if the caption must be shown above the message media
    has_media_spoiler: True, if the message media is covered by a spoiler animation
    checklist: Message is a checklist
    contact: Message is a shared contact, information about the contact
    dice: Message is a dice with random value
    game: Message is a game, information about the game.
    poll: Message is a native poll, information about the poll
    venue: Message is a venue, information about the venue. For backward compatibility, when this field is set, the location field will also be set.
    location: Message is a shared location, information about the location
    new_chat_members: New members that were added to the group or supergroup and information about them (the bot itself may be one of these members)
    left_chat_member: A member was removed from the group, information about them (this member may be the bot itself)
    chat_owner_left: Service message: chat owner has left
    chat_owner_changed: Service message: chat owner has changed
    new_chat_title: A chat title was changed to this value
    new_chat_photo: A chat photo was change to this value
    delete_chat_photo: Service message: the chat photo was deleted
    group_chat_created: Service message: the group has been created
    supergroup_chat_created: Service message: the supergroup has been created. This field can't be received in a message coming through updates, because bot can't be a member of a supergroup when it is created. It can only be found in reply_to_message if someone replies to a very first message in a directly created supergroup.
    channel_chat_created: Service message: the channel has been created. This field can't be received in a message coming through updates, because bot can't be a member of a channel when it is created. It can only be found in reply_to_message if someone replies to a very first message in a channel.
    message_auto_delete_timer_changed: Service message: auto-delete timer settings changed in the chat
    migrate_to_chat_id: The group has been migrated to a supergroup with the specified identifier. This number may have more than 32 significant bits and some programming languages may have difficulty/silent defects in interpreting it. But it has at most 52 significant bits, so a signed 64-bit integer or double-precision float type are safe for storing this identifier.
    migrate_from_chat_id: The supergroup has been migrated from a group with the specified identifier. This number may have more than 32 significant bits and some programming languages may have difficulty/silent defects in interpreting it. But it has at most 52 significant bits, so a signed 64-bit integer or double-precision float type are safe for storing this identifier.
    pinned_message: Specified message was pinned. Note that the Message object in this field will not contain further reply_to_message fields even if it itself is a reply.
    invoice: Message is an invoice for a payment, information about the invoice.
    successful_payment: Message is a service message about a successful payment, information about the payment.
    refunded_payment: Message is a service message about a refunded payment, information about the payment.
    users_shared: Service message: users were shared with the bot
    chat_shared: Service message: a chat was shared with the bot
    gift: Service message: a regular gift was sent or received
    unique_gift: Service message: a unique gift was sent or received
    gift_upgrade_sent: Service message: upgrade of a gift was purchased after the gift was sent
    connected_website: The domain name of the website on which the user has logged in.
    write_access_allowed: Service message: the user allowed the bot to write messages after adding it to the attachment or side menu, launching a Web App from a link, or accepting an explicit request from a Web App sent by the method requestWriteAccess
    passport_data: Telegram Passport data
    proximity_alert_triggered: Service message. A user in the chat triggered another user's proximity alert while sharing Live Location.
    boost_added: Service message: user boosted the chat
    chat_background_set: Service message: chat background set
    checklist_tasks_done: Service message: some tasks in a checklist were marked as done or not done
    checklist_tasks_added: Service message: tasks were added to a checklist
    direct_message_price_changed: Service message: the price for paid messages in the corresponding direct messages chat of a channel has changed
    forum_topic_created: Service message: forum topic created
    forum_topic_edited: Service message: forum topic edited
    forum_topic_closed: Service message: forum topic closed
    forum_topic_reopened: Service message: forum topic reopened
    general_forum_topic_hidden: Service message: the 'General' forum topic hidden
    general_forum_topic_unhidden: Service message: the 'General' forum topic unhidden
    giveaway_created: Service message: a scheduled giveaway was created
    giveaway: The message is a scheduled giveaway message
    giveaway_winners: A giveaway with public winners was completed
    giveaway_completed: Service message: a giveaway without public winners was completed
    managed_bot_created: Service message: user created a bot that will be managed by the current bot
    paid_message_price_changed: Service message: the price for paid messages has changed in the chat
    poll_option_added: Service message: answer option was added to a poll
    poll_option_deleted: Service message: answer option was deleted from a poll
    suggested_post_approved: Service message: a suggested post was approved
    suggested_post_approval_failed: Service message: approval of a suggested post has failed
    suggested_post_declined: Service message: a suggested post was declined
    suggested_post_paid: Service message: payment for a suggested post was received
    suggested_post_refunded: Service message: payment for a suggested post was refunded
    video_chat_scheduled: Service message: video chat scheduled
    video_chat_started: Service message: video chat started
    video_chat_ended: Service message: video chat ended
    video_chat_participants_invited: Service message: new participants invited to a video chat
    web_app_data: Service message: data sent by a Web App
    reply_markup: Inline keyboard attached to the message. login_url buttons are represented as ordinary url buttons.
    rich_message: Message is a rich formatted message
    receiver_user: For ephemeral messages, the user who received the message
    ephemeral_message_id: For ephemeral messages, identifier of the ephemeral message inside this chat. The identifier may be reused for another ephemeral message after the message is deleted or expires.
    community_chat_added: Service message: chat added to a Community
    community_chat_removed: Service message: chat removed from a Community
    forward_date: For forwarded messages, date the original message was sent in Unix time
    forward_from: For forwarded messages, sender of the original message
    forward_from_chat: For messages forwarded from channels or from anonymous administrators, information about the original sender chat
    forward_from_message_id: For messages forwarded from channels, identifier of the original message in the channel
    forward_sender_name: Sender's name for messages forwarded from users who disallow adding a link to their account in forwarded messages
    forward_signature: For forwarded messages that were originally sent in channels or by an anonymous chat administrator, signature of the message sender if present
    user_shared: Service message: a user was shared with the bot"""
    message_id: int
    date: int
    chat: Chat
    message_thread_id: Optional[int] = None
    from_: Optional[User] = None
    sender_chat: Optional[Chat] = None
    sender_boost_count: Optional[int] = None
    sender_business_bot: Optional[User] = None
    business_connection_id: Optional[str] = None
    forward_origin: Optional[object] = None
    is_topic_message: Optional[bool] = None
    is_automatic_forward: Optional[bool] = None
    reply_to_message: Optional['Message'] = None
    external_reply: Optional[ExternalReplyInfo] = None
    quote: Optional[TextQuote] = None
    reply_to_story: Optional[object] = None
    via_bot: Optional[User] = None
    author_signature: Optional[str] = None
    text: Optional[str] = None
    entities: Optional[List[MessageEntity]] = None
    link_preview_options: Optional[object] = None
    effect_id: Optional[str] = None
    animation: Optional[Animation] = None
    audio: Optional[Audio] = None
    document: Optional[Document] = None
    paid_media: Optional[object] = None
    photo: Optional[List[PhotoSize]] = None
    sticker: Optional[object] = None
    story: Optional[object] = None
    video: Optional[Video] = None
    video_note: Optional[VideoNote] = None
    voice: Optional[Voice] = None
    live_photo: Optional[LivePhoto] = None
    caption: Optional[str] = None
    caption_entities: Optional[List[MessageEntity]] = None
    show_caption_above_media: Optional[bool] = None
    has_media_spoiler: Optional[bool] = None
    contact: Optional[Contact] = None
    dice: Optional[Dice] = None
    game: Optional[object] = None
    poll: Optional[Poll] = None
    venue: Optional[Venue] = None
    location: Optional[Location] = None
    new_chat_members: Optional[List[User]] = None
    left_chat_member: Optional[User] = None
    new_chat_title: Optional[str] = None
    new_chat_photo: Optional[object] = None
    delete_chat_photo: Optional[bool] = None
    group_chat_created: Optional[bool] = None
    supergroup_chat_created: Optional[bool] = None
    channel_chat_created: Optional[bool] = None
    message_auto_delete_timer_changed: Optional[object] = None
    migrate_to_chat_id: Optional[int] = None
    migrate_from_chat_id: Optional[int] = None
    pinned_message: Optional['Message'] = None
    invoice: Optional[object] = None
    successful_payment: Optional[object] = None
    users_shared: Optional[object] = None
    chat_shared: Optional[object] = None
    connected_website: Optional[str] = None
    write_access_allowed: Optional[object] = None
    passport_data: Optional[object] = None
    proximity_alert_triggered: Optional[object] = None
    boost_added: Optional[object] = None
    chat_background_set: Optional[object] = None
    forum_topic_created: Optional[ForumTopicCreated] = None
    forum_topic_edited: Optional[ForumTopicEdited] = None
    forum_topic_closed: Optional[ForumTopicClosed] = None
    forum_topic_reopened: Optional[ForumTopicReopened] = None
    general_forum_topic_hidden: Optional[GeneralForumTopicHidden] = None
    general_forum_topic_unhidden: Optional[GeneralForumTopicUnhidden] = None
    giveaway_created: Optional[object] = None
    giveaway: Optional[object] = None
    giveaway_winners: Optional[object] = None
    giveaway_completed: Optional[object] = None
    paid_message_price_changed: Optional[object] = None
    video_chat_scheduled: Optional[object] = None
    video_chat_started: Optional[object] = None
    video_chat_ended: Optional[object] = None
    video_chat_participants_invited: Optional[object] = None
    web_app_data: Optional[object] = None
    reply_markup: Optional[InlineKeyboardMarkup] = None

    @classmethod
    def from_dict(cls, data: Optional[dict]) -> Optional['Message']:
        """Parse a Telegram API mapping into this type.

Args:
    data: Raw Telegram API mapping, or ``None``.

Returns:
    Parsed type instance, or ``None`` when ``data`` is ``None``."""
        from ..models import ForumTopicClosed
        from ..models import ForumTopicCreated
        from ..models import ForumTopicEdited
        from ..models import ForumTopicReopened
        from ..models import GeneralForumTopicHidden
        from ..models import GeneralForumTopicUnhidden
        from ..models import InlineKeyboardMarkup
        if data is None:
            return None
        members_raw = data.get('new_chat_members')
        return cls(message_id=data['message_id'], date=data.get('date', 0), chat=Chat.from_dict(data.get('chat', {})), message_thread_id=data.get('message_thread_id'), from_=User.from_dict(data.get('from')), sender_chat=Chat.from_dict(data.get('sender_chat')), sender_boost_count=data.get('sender_boost_count'), sender_business_bot=User.from_dict(data.get('sender_business_bot')), business_connection_id=data.get('business_connection_id'), forward_origin=data.get('forward_origin'), is_topic_message=data.get('is_topic_message'), is_automatic_forward=data.get('is_automatic_forward'), reply_to_message=Message.from_dict(data.get('reply_to_message')), external_reply=ExternalReplyInfo.from_dict(data.get('external_reply')), quote=TextQuote.from_dict(data.get('quote')), reply_to_story=data.get('reply_to_story'), via_bot=User.from_dict(data.get('via_bot')), author_signature=data.get('author_signature'), text=data.get('text'), entities=MessageEntity.list_from(data.get('entities')), link_preview_options=data.get('link_preview_options'), effect_id=data.get('effect_id'), animation=Animation.from_dict(data.get('animation')), audio=Audio.from_dict(data.get('audio')), document=Document.from_dict(data.get('document')), paid_media=data.get('paid_media'), photo=PhotoSize.list_from(data.get('photo')), sticker=data.get('sticker'), story=data.get('story'), video=Video.from_dict(data.get('video')), video_note=VideoNote.from_dict(data.get('video_note')), voice=Voice.from_dict(data.get('voice')), live_photo=LivePhoto.from_dict(data.get('live_photo')), caption=data.get('caption'), caption_entities=MessageEntity.list_from(data.get('caption_entities')), show_caption_above_media=data.get('show_caption_above_media'), has_media_spoiler=data.get('has_media_spoiler'), contact=Contact.from_dict(data.get('contact')), dice=Dice.from_dict(data.get('dice')), game=data.get('game'), poll=Poll.from_dict(data.get('poll')), venue=Venue.from_dict(data.get('venue')), location=Location.from_dict(data.get('location')), new_chat_members=[User.from_dict(u) for u in members_raw] if members_raw is not None else None, left_chat_member=User.from_dict(data.get('left_chat_member')), new_chat_title=data.get('new_chat_title'), new_chat_photo=data.get('new_chat_photo'), delete_chat_photo=data.get('delete_chat_photo'), group_chat_created=data.get('group_chat_created'), supergroup_chat_created=data.get('supergroup_chat_created'), channel_chat_created=data.get('channel_chat_created'), message_auto_delete_timer_changed=data.get('message_auto_delete_timer_changed'), migrate_to_chat_id=data.get('migrate_to_chat_id'), migrate_from_chat_id=data.get('migrate_from_chat_id'), pinned_message=Message.from_dict(data.get('pinned_message')), invoice=data.get('invoice'), successful_payment=data.get('successful_payment'), users_shared=data.get('users_shared'), chat_shared=data.get('chat_shared'), connected_website=data.get('connected_website'), write_access_allowed=data.get('write_access_allowed'), passport_data=data.get('passport_data'), proximity_alert_triggered=data.get('proximity_alert_triggered'), boost_added=data.get('boost_added'), chat_background_set=data.get('chat_background_set'), forum_topic_created=ForumTopicCreated.from_dict(data.get('forum_topic_created')), forum_topic_edited=ForumTopicEdited.from_dict(data.get('forum_topic_edited')), forum_topic_closed=ForumTopicClosed.from_dict(data.get('forum_topic_closed')), forum_topic_reopened=ForumTopicReopened.from_dict(data.get('forum_topic_reopened')), general_forum_topic_hidden=GeneralForumTopicHidden.from_dict(data.get('general_forum_topic_hidden')), general_forum_topic_unhidden=GeneralForumTopicUnhidden.from_dict(data.get('general_forum_topic_unhidden')), giveaway_created=data.get('giveaway_created'), giveaway=data.get('giveaway'), giveaway_winners=data.get('giveaway_winners'), giveaway_completed=data.get('giveaway_completed'), paid_message_price_changed=data.get('paid_message_price_changed'), video_chat_scheduled=data.get('video_chat_scheduled'), video_chat_started=data.get('video_chat_started'), video_chat_ended=data.get('video_chat_ended'), video_chat_participants_invited=data.get('video_chat_participants_invited'), web_app_data=data.get('web_app_data'), reply_markup=InlineKeyboardMarkup.from_dict(data.get('reply_markup')))

    @classmethod
    def list_from_result(cls, data: Optional[List[dict]]) -> List['Message']:
        """Parse a Telegram API result list into this type.

Args:
    data: Raw result list, or ``None``.

Returns:
    Parsed type instances."""
        return [cls.from_dict(item) for item in data or []]
