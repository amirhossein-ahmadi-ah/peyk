from peyk import ButtonStyle, ChatAction, ContentType, ParseMode, Platform
from peyk.platforms.telegram.enums import (
    BotCommandScopeType, DiceEmoji, InputMediaType, MenuButtonType, RichTextType,
    StickerFormat, UpdateType,
)


def test_neutral_enum_wire_values():
    assert ChatAction.TYPING == "typing"
    assert ContentType.TEXT == "text"
    assert ParseMode.HTML == "HTML"
    assert ButtonStyle.PRIMARY == "primary"
    assert Platform.TELEGRAM == "telegram"


def test_telegram_enum_wire_values():
    assert BotCommandScopeType.CHAT_MEMBER == "chat_member"
    assert DiceEmoji.DICE == "🎲"
    assert InputMediaType.PHOTO == "photo"
    assert MenuButtonType.WEB_APP == "web_app"
    assert RichTextType.CUSTOM_EMOJI == "custom_emoji"
    assert StickerFormat.VIDEO == "video"
    assert UpdateType.INLINE_QUERY == "inline_query"
