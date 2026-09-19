"""Telegram Bot API enum values added for Phase 10A.

Values are copied from the repository's audited Telegram Bot API surface and,
where the local aiogram YAML reference was unavailable, from the official Bot
API schema/documentation. Wire values are kept verbatim.
"""
from enum import Enum

class BotCommandScopeType(str, Enum):
    """BotCommandScopeType defines a public API type for peyk."""
    DEFAULT = 'default'
    ALL_PRIVATE_CHATS = 'all_private_chats'
    ALL_GROUP_CHATS = 'all_group_chats'
    ALL_CHAT_ADMINISTRATORS = 'all_chat_administrators'
    CHAT = 'chat'
    CHAT_ADMINISTRATORS = 'chat_administrators'
    CHAT_MEMBER = 'chat_member'

class BotSubscriptionUpdatedState(str, Enum):
    """BotSubscriptionUpdatedState defines a public API type for peyk."""
    ACTIVE = 'active'
    CANCELLED = 'cancelled'
    PENDING = 'pending'
from peyk.enums import ButtonStyle

class Currency(str, Enum):
    """Currency defines a public API type for peyk."""
    XTR = 'XTR'

class DiceEmoji(str, Enum):
    """DiceEmoji defines a public API type for peyk."""
    DICE = '🎲'
    DARTS = '🎯'
    BASKETBALL = '🏀'
    FOOTBALL = '⚽'
    SLOT_MACHINE = '🎰'
    BOWLING = '🎳'

class EncryptedPassportElement(str, Enum):
    """EncryptedPassportElement defines a public API type for peyk."""
    DATA = 'data'
    FRONT_SIDE = 'front_side'
    REVERSE_SIDE = 'reverse_side'
    SELFIE = 'selfie'
    FILES = 'files'
    TRANSLATION = 'translation'
    UTILITY_BILL = 'utility_bill'

class InlineQueryResultType(str, Enum):
    """InlineQueryResultType defines a public API type for peyk."""
    ARTICLE = 'article'
    PHOTO = 'photo'
    GIF = 'gif'
    MPEG4_GIF = 'mpeg4_gif'
    VIDEO = 'video'
    AUDIO = 'audio'
    VOICE = 'voice'
    DOCUMENT = 'document'
    LOCATION = 'location'
    VENUE = 'venue'
    CONTACT = 'contact'
    GAME = 'game'
    STICKER = 'sticker'

class InputMediaType(str, Enum):
    """InputMediaType defines a public API type for peyk."""
    ANIMATION = 'animation'
    DOCUMENT = 'document'
    AUDIO = 'audio'
    PHOTO = 'photo'
    VIDEO = 'video'

class InputRichBlockType(str, Enum):
    """InputRichBlockType defines a public API type for peyk."""
    PARAGRAPH = 'paragraph'
    HEADING = 'heading'
    PRE = 'pre'
    FOOTER = 'footer'
    DIVIDER = 'divider'
    MATHEMATICAL_EXPRESSION = 'mathematical_expression'
    ANCHOR = 'anchor'
    LIST = 'list'
    BLOCKQUOTE = 'blockquote'
    EXPANDABLE_BLOCKQUOTE = 'expandable_blockquote'
    PULLQUOTE = 'pullquote'
    COLLAGE = 'collage'
    SLIDESHOW = 'slideshow'
    TABLE = 'table'
    DETAILS = 'details'
    MAP = 'map'
    BUTTONS = 'buttons'
    ANIMATION = 'animation'
    AUDIO = 'audio'
    DOCUMENT = 'document'
    PHOTO = 'photo'
    VIDEO = 'video'
    VOICE_NOTE = 'voice_note'
    THINKING = 'thinking'

class KeyboardButtonPollTypeType(str, Enum):
    """KeyboardButtonPollTypeType defines a public API type for peyk."""
    QUIZ = 'quiz'
    REGULAR = 'regular'

class MaskPositionPoint(str, Enum):
    """MaskPositionPoint defines a public API type for peyk."""
    FOREHEAD = 'forehead'
    EYES = 'eyes'
    MOUTH = 'mouth'
    CHIN = 'chin'

class MenuButtonType(str, Enum):
    """MenuButtonType defines a public API type for peyk."""
    COMMANDS = 'commands'
    WEB_APP = 'web_app'
    DEFAULT = 'default'

class RichBlockType(str, Enum):
    """RichBlockType defines a public API type for peyk."""
    PARAGRAPH = 'paragraph'
    HEADING = 'heading'
    PRE = 'pre'
    FOOTER = 'footer'
    DIVIDER = 'divider'
    MATHEMATICAL_EXPRESSION = 'mathematical_expression'
    ANCHOR = 'anchor'
    LIST = 'list'
    BLOCKQUOTE = 'blockquote'
    EXPANDABLE_BLOCKQUOTE = 'expandable_blockquote'
    PULLQUOTE = 'pullquote'
    COLLAGE = 'collage'
    SLIDESHOW = 'slideshow'
    TABLE = 'table'
    DETAILS = 'details'
    MAP = 'map'
    BUTTONS = 'buttons'
    ANIMATION = 'animation'
    AUDIO = 'audio'
    DOCUMENT = 'document'
    PHOTO = 'photo'
    VIDEO = 'video'
    VOICE_NOTE = 'voice_note'
    THINKING = 'thinking'

class RichTextType(str, Enum):
    """RichTextType defines a public API type for peyk."""
    BOLD = 'bold'
    ITALIC = 'italic'
    UNDERLINE = 'underline'
    STRIKETHROUGH = 'strikethrough'
    SPOILER = 'spoiler'
    DATETIME = 'datetime'
    TEXT_MENTION = 'text_mention'
    SUBSCRIPT = 'subscript'
    SUPERSCRIPT = 'superscript'
    MARKED = 'marked'
    CODE = 'code'
    CUSTOM_EMOJI = 'custom_emoji'
    MATHEMATICAL_EXPRESSION = 'mathematical_expression'
    URL = 'url'
    EMAIL_ADDRESS = 'email_address'
    PHONE_NUMBER = 'phone_number'
    BANK_CARD_NUMBER = 'bank_card_number'
    MENTION = 'mention'
    HASHTAG = 'hashtag'
    CASHTAG = 'cashtag'
    BOT_COMMAND = 'bot_command'
    BUTTON = 'button'
    ANCHOR = 'anchor'
    ANCHOR_LINK = 'anchor_link'
    REFERENCE = 'reference'
    REFERENCE_LINK = 'reference_link'

class StickerFormat(str, Enum):
    """StickerFormat defines a public API type for peyk."""
    STATIC = 'static'
    ANIMATED = 'animated'
    VIDEO = 'video'

class TopicIconColor(str, Enum):
    """TopicIconColor defines a public API type for peyk."""
    BLUE = '0x6FB9F0'
    YELLOW = '0xFFD67E'
    PURPLE = '0xCB86DB'
    GREEN = '0x8EEE98'
    PINK = '0xFF93B2'
    RED = '0xFF6F61'

class TransactionPartnerUserTransactionType(str, Enum):
    """TransactionPartnerUserTransactionType defines a public API type for peyk."""
    DEPOSIT = 'deposit'
    WITHDRAWAL = 'withdrawal'

class UpdateType(str, Enum):
    """UpdateType defines a public API type for peyk."""
    MESSAGE = 'message'
    EDITED_MESSAGE = 'edited_message'
    CHANNEL_POST = 'channel_post'
    EDITED_CHANNEL_POST = 'edited_channel_post'
    BUSINESS_CONNECTION = 'business_connection'
    BUSINESS_MESSAGE = 'business_message'
    EDITED_BUSINESS_MESSAGE = 'edited_business_message'
    DELETED_BUSINESS_MESSAGES = 'deleted_business_messages'
    MESSAGE_REACTION = 'message_reaction'
    MESSAGE_REACTION_COUNT = 'message_reaction_count'
    INLINE_QUERY = 'inline_query'
    CHOSEN_INLINE_RESULT = 'chosen_inline_result'
    CALLBACK_QUERY = 'callback_query'
    SHIPPING_QUERY = 'shipping_query'
    PRE_CHECKOUT_QUERY = 'pre_checkout_query'
    PURCHASED_PAID_MEDIA = 'purchased_paid_media'
    POLL = 'poll'
    POLL_ANSWER = 'poll_answer'
    MY_CHAT_MEMBER = 'my_chat_member'
    CHAT_MEMBER = 'chat_member'
    CHAT_JOIN_REQUEST = 'chat_join_request'
    CHAT_BOOST = 'chat_boost'
    REMOVED_CHAT_BOOST = 'removed_chat_boost'
    MANAGED_BOT = 'managed_bot'
    SUBSCRIPTION = 'subscription'
    STOPPED_MESSAGE_GENERATION = 'stopped_message_generation'
__all__ = [name for name in globals() if not name.startswith('_')]
