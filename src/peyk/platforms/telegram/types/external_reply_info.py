from __future__ import annotations
from dataclasses import dataclass, field
import re
from typing import Any, Dict, List, Mapping, Optional, Sequence, Union
from .chat import Chat
from .text_quote import TextQuote

@dataclass
class ExternalReplyInfo:
    """This object contains information about a message that is being replied to, which may come from another chat or forum topic.

Attributes:
    origin: Origin of the message replied to by the given message
    chat: Chat the original message belongs to. Available only if the chat is a supergroup or a channel.
    message_id: Unique message identifier inside the original chat. Available only if the original chat is a supergroup or a channel.
    link_preview_options: Options used for link preview generation for the original message, if it is a text message
    animation: Message is an animation, information about the animation
    audio: Message is an audio file, information about the file
    document: Message is a general file, information about the file
    live_photo: Message is a live photo, information about the live photo
    paid_media: Message contains paid media; information about the paid media
    photo: Message is a photo, available sizes of the photo
    sticker: Message is a sticker, information about the sticker
    story: Message is a forwarded story
    video: Message is a video, information about the video
    video_note: Message is a video note, information about the video message
    voice: Message is a voice message, information about the file
    has_media_spoiler: True, if the message media is covered by a spoiler animation
    checklist: Message is a checklist
    contact: Message is a shared contact, information about the contact
    dice: Message is a dice with random value
    game: Message is a game, information about the game.
    giveaway: Message is a scheduled giveaway, information about the giveaway
    giveaway_winners: A giveaway with public winners was completed
    invoice: Message is an invoice for a payment, information about the invoice.
    location: Message is a shared location, information about the location
    poll: Message is a native poll, information about the poll
    venue: Message is a venue, information about the venue"""
    origin: Optional[object] = None
    chat: Optional[Chat] = None
    message_id: Optional[int] = None
    link_preview_options: Optional[object] = None
    animation: Optional[object] = None
    audio: Optional[object] = None
    document: Optional[object] = None
    photo: Optional[object] = None
    sticker: Optional[object] = None
    story: Optional[object] = None
    video: Optional[object] = None
    video_note: Optional[object] = None
    voice: Optional[object] = None
    live_photo: Optional[object] = None
    has_media_spoiler: Optional[bool] = None
    contact: Optional[object] = None
    dice: Optional[object] = None
    game: Optional[object] = None
    giveaway: Optional[object] = None
    giveaway_winners: Optional[object] = None
    invoice: Optional[object] = None
    location: Optional[object] = None
    poll: Optional[object] = None
    venue: Optional[object] = None
    quote: Optional[TextQuote] = None

    @classmethod
    def from_dict(cls, data: Optional[dict]) -> Optional['ExternalReplyInfo']:
        """Parse a Telegram API mapping into this type.

Args:
    data: Raw Telegram API mapping, or ``None``.

Returns:
    Parsed type instance, or ``None`` when ``data`` is ``None``."""
        if data is None:
            return None
        return cls(origin=data.get('origin'), chat=Chat.from_dict(data.get('chat')), message_id=data.get('message_id'), link_preview_options=data.get('link_preview_options'), animation=data.get('animation'), audio=data.get('audio'), document=data.get('document'), photo=data.get('photo'), sticker=data.get('sticker'), story=data.get('story'), video=data.get('video'), video_note=data.get('video_note'), voice=data.get('voice'), live_photo=data.get('live_photo'), has_media_spoiler=data.get('has_media_spoiler'), contact=data.get('contact'), dice=data.get('dice'), game=data.get('game'), giveaway=data.get('giveaway'), giveaway_winners=data.get('giveaway_winners'), invoice=data.get('invoice'), location=data.get('location'), poll=data.get('poll'), venue=data.get('venue'), quote=TextQuote.from_dict(data.get('quote')))
