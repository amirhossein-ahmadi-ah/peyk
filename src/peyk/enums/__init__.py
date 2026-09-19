"""Platform-neutral finite enums used by the public Peyk API."""
from __future__ import annotations
from enum import Enum

class ContentType(str, Enum):
    """ContentType defines a public API type for peyk."""
    TEXT = 'text'
    PHOTO = 'photo'
    VIDEO = 'video'
    AUDIO = 'audio'
    VOICE = 'voice'
    DOCUMENT = 'document'
    STICKER = 'sticker'
    ANIMATION = 'animation'
    CONTACT = 'contact'
    LOCATION = 'location'
    POLL = 'poll'
    VENUE = 'venue'
    NEW_CHAT_MEMBERS = 'new_chat_members'
    LEFT_CHAT_MEMBER = 'left_chat_member'
    SUCCESSFUL_PAYMENT = 'successful_payment'
    UNKNOWN = 'unknown'

class ChatType(str, Enum):
    """ChatType defines a public API type for peyk."""
    PRIVATE = 'private'
    GROUP = 'group'
    CHANNEL = 'channel'
    UNKNOWN = 'unknown'

class ChatAction(str, Enum):
    """ChatAction defines a public API type for peyk."""
    TYPING = 'typing'
    UPLOAD_PHOTO = 'upload_photo'
    RECORD_VIDEO = 'record_video'
    UPLOAD_VIDEO = 'upload_video'
    RECORD_VOICE = 'record_voice'
    UPLOAD_VOICE = 'upload_voice'
    UPLOAD_DOCUMENT = 'upload_document'
    CHOOSE_STICKER = 'choose_sticker'
    FIND_LOCATION = 'find_location'
    RECORD_VIDEO_NOTE = 'record_video_note'
    UPLOAD_VIDEO_NOTE = 'upload_video_note'

class ButtonStyle(str, Enum):
    """ButtonStyle defines a public API type for peyk."""
    PRIMARY = 'primary'
    SUCCESS = 'success'
    DANGER = 'danger'

class ParseMode(str, Enum):
    """ParseMode defines a public API type for peyk."""
    MARKDOWN = 'Markdown'
    MARKDOWN_V2 = 'MarkdownV2'
    HTML = 'HTML'

class Platform(str, Enum):
    """Platform defines a public API type for peyk."""
    TELEGRAM = 'telegram'
    BALE = 'bale'
    RUBIKA = 'rubika'
    CUSTOM = 'custom'
__all__ = ['ContentType', 'ChatType', 'ChatAction', 'ParseMode', 'ButtonStyle', 'Platform']
