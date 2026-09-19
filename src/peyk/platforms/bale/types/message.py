from __future__ import annotations
from dataclasses import dataclass
from typing import Any, List, Optional
from .animation import Animation
from .audio import Audio
from .chat import Chat
from .contact import Contact
from .document import Document
from .invoice import Invoice
from .location import Location
from .message_entity import MessageEntity
from .photo_size import PhotoSize
from .sticker import Sticker
from .successful_payment import SuccessfulPayment
from .user import User
from .video import Video
from .voice import Voice
from .web_app_data import WebAppData

@dataclass
class Message:
    """Represent the Bale Bot API ``Message`` object.

Preserves the existing dataclass fields and parsing behavior."""
    message_id: int
    from_: Optional[User] = None
    date: Optional[int] = None
    chat: Optional[Chat] = None
    sender_chat: Optional[Chat] = None
    forward_from: Optional[User] = None
    forward_from_chat: Optional[Chat] = None
    forward_from_message_id: Optional[int] = None
    forward_date: Optional[int] = None
    reply_to_message: Optional['Message'] = None
    edit_date: Optional[int] = None
    media_group_id: Optional[str] = None
    text: Optional[str] = None
    entities: Optional[List[MessageEntity]] = None
    animation: Optional[Animation] = None
    audio: Optional[Audio] = None
    document: Optional[Document] = None
    photo: Optional[List[PhotoSize]] = None
    sticker: Optional[Sticker] = None
    video: Optional[Video] = None
    voice: Optional[Voice] = None
    caption: Optional[str] = None
    caption_entities: Optional[List[MessageEntity]] = None
    contact: Optional[Contact] = None
    location: Optional[Location] = None
    new_chat_members: Optional[List[User]] = None
    left_chat_member: Optional[User] = None
    invoice: Optional[Invoice] = None
    successful_payment: Optional[SuccessfulPayment] = None
    web_app_data: Optional[WebAppData] = None
    reply_markup: Optional[object] = None

    @classmethod
    def from_dict(cls, data: Optional[dict]) -> Optional['Message']:
        """Parse raw Bale data into ``Message``.

Args:
    data (Optional[dict]): Raw API object or ``None``.

Returns:
    Optional[Message]: Parsed object or ``None``.

Raises:
    KeyError: If a required raw field is missing."""
        if data is None:
            return None
        new_chat_members_raw = data.get('new_chat_members')
        return cls(message_id=data['message_id'], from_=User.from_dict(data.get('from')), date=data.get('date'), chat=Chat.from_dict(data.get('chat')), sender_chat=Chat.from_dict(data.get('sender_chat')), forward_from=User.from_dict(data.get('forward_from')), forward_from_chat=Chat.from_dict(data.get('forward_from_chat')), forward_from_message_id=data.get('forward_from_message_id'), forward_date=data.get('forward_date'), reply_to_message=Message.from_dict(data.get('reply_to_message')), edit_date=data.get('edit_date'), media_group_id=data.get('media_group_id'), text=data.get('text'), entities=MessageEntity.list_from_result(data.get('entities')), animation=Animation.from_dict(data.get('animation')), audio=Audio.from_dict(data.get('audio')), document=Document.from_dict(data.get('document')), photo=PhotoSize.list_from_result(data.get('photo')), sticker=Sticker.from_dict(data.get('sticker')), video=Video.from_dict(data.get('video')), voice=Voice.from_dict(data.get('voice')), caption=data.get('caption'), caption_entities=MessageEntity.list_from_result(data.get('caption_entities')), contact=Contact.from_dict(data.get('contact')), location=Location.from_dict(data.get('location')), new_chat_members=[User.from_dict(u) for u in new_chat_members_raw] if new_chat_members_raw is not None else None, left_chat_member=User.from_dict(data.get('left_chat_member')), invoice=Invoice.from_dict(data.get('invoice')), successful_payment=SuccessfulPayment.from_dict(data.get('successful_payment')), web_app_data=WebAppData.from_dict(data.get('web_app_data')), reply_markup=data.get('reply_markup'))

    @classmethod
    def list_from_result(cls, data: Optional[List[dict]]) -> List['Message']:
        """Performs the list from result operation for the Bale client.

Args:
    data: Value used by this operation.

Returns:
    Result produced by the Bale operation."""
        "Parse an array of `Message` from a raw `result` list.\n        \n                Used by `sendMediaGroup`, which returns an array of the sent\n                messages rather than a single one.\n                \n        \n        Args:\n            data: Value of the declared parameter type.\n        \n        \n        Returns:\n            The operation result (``List['Message']``).\n        "
        return [cls.from_dict(item) for item in data or []]
