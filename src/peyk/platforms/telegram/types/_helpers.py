"""Compatibility helpers for Telegram model parsing and serialization.

These functions preserve the module-level helper surface of the legacy
``models.py`` facade while the concrete model classes live in one-file modules.
"""
from __future__ import annotations
from dataclasses import dataclass
from types import SimpleNamespace as _SimpleNamespace
from typing import Any, Dict, List, Mapping, Optional, Sequence, Union

def validate_callback_data(data: str) -> None:
    """Provides the validate callback data operation for the Telegram integration.

Args:
    data: Value used by this operation."""
    'Raise `ValueError` if `data` violates the `callback_data` limit.\n        \n            The limit (1-64 bytes) is on *UTF-8 encoded byte length*, not\n            character count -- a string well under 64 characters can still\n            exceed 64 bytes once multi-byte characters (e.g. Persian/Farsi\n            text) are encoded. Intentionally mirrors the equivalent Bale-side helper; the concrete\n            client delegates common validation mechanics to ``TelegramLikeClient``.\n            \n        \n        Args:\n            data: Value of the declared parameter type.\n        \n        \n        Returns:\n            The operation result (``None``).\n        \n    \n    Raises:\n        ValueError: Raised when the operation cannot complete.\n    '
    encoded = data.encode('utf-8')
    if not 1 <= len(encoded) <= MAX_CALLBACK_DATA_BYTES:
        raise ValueError(f'callback_data must be 1-{MAX_CALLBACK_DATA_BYTES} bytes when UTF-8 encoded, got {len(encoded)} bytes')

def _button_row_to_dict(row: Sequence[Union[KeyboardButton, Mapping[str, object], str]]) -> List[Dict[str, object]]:
    """_button_row_to_dict Telegram model helper."""
    out: List[Dict[str, object]] = []
    for item in row:
        if isinstance(item, KeyboardButton):
            out.append(item.to_dict())
        elif isinstance(item, str):
            out.append({'text': item})
        else:
            out.append(dict(item))
    return out

def serialize_reply_markup(value: ReplyMarkup) -> Dict[str, object]:
    """Provides the serialize reply markup operation for the Telegram integration.

Args:
    value: Value used by this operation.

Returns:
    Result produced by the operation."""
    'Serialize a `reply_markup` argument for the request body.\n    \n        Typed markups go through their own `to_dict()` (which also enforces\n        the `callback_data` byte limit on inline buttons); raw mappings\n        pass through as plain dicts.\n        \n    \n    Args:\n        value: Value of the declared parameter type.\n    \n    \n    Returns:\n        The operation result (``Dict[str, object]``).\n    '
    if isinstance(value, (InlineKeyboardMarkup, ReplyKeyboardMarkup, ReplyKeyboardRemove, ForceReply)):
        return value.to_dict()
    return dict(value)

def parse_bot_command_scope(data: Optional[dict]) -> Optional[BotCommandScope]:
    """Provides the parse bot command scope operation for the Telegram integration.

Args:
    data: Value used by this operation.

Returns:
    Result produced by the operation."""
    'Dispatch a scope payload to its subtype on the `type` field.\n        \n        Args:\n            data: Value of the declared parameter type.\n        \n        \n        Returns:\n            The operation result (``Optional[BotCommandScope]``).\n        \n    \n    Raises:\n        ValueError: Raised when the operation cannot complete.\n    '
    if data is None:
        return None
    scope_type = data.get('type', 'default')
    if scope_type == 'all_private_chats':
        return BotCommandScopeAllPrivateChats.from_dict(data)
    if scope_type == 'all_group_chats':
        return BotCommandScopeAllGroupChats.from_dict(data)
    if scope_type == 'all_chat_administrators':
        return BotCommandScopeAllChatAdministrators.from_dict(data)
    if scope_type == 'chat':
        return BotCommandScopeChat.from_dict(data)
    if scope_type == 'chat_administrators':
        return BotCommandScopeChatAdministrators.from_dict(data)
    if scope_type == 'chat_member':
        return BotCommandScopeChatMember.from_dict(data)
    if scope_type == 'default':
        return BotCommandScopeDefault.from_dict(data)
    raise ValueError(f'unknown BotCommandScope type: {scope_type!r}')

def serialize_bot_command_scope(value: Union[BotCommandScope, Mapping[str, object]]) -> Dict[str, object]:
    """Provides the serialize bot command scope operation for the Telegram integration.

Args:
    value: Value used by this operation.

Returns:
    Result produced by the operation."""
    'Serialize a scope argument: typed scopes via `to_dict()`, raw\n        mappings pass through.\n    \n    Args:\n        value: Value of the declared parameter type.\n    \n    \n    Returns:\n        The operation result (``Dict[str, object]``).\n    '
    if isinstance(value, (BotCommandScopeDefault, BotCommandScopeAllPrivateChats, BotCommandScopeAllGroupChats, BotCommandScopeAllChatAdministrators, BotCommandScopeChat, BotCommandScopeChatAdministrators, BotCommandScopeChatMember)):
        return value.to_dict()
    return dict(value)

def parse_menu_button(data: Optional[dict]) -> Optional[MenuButton]:
    """Provides the parse menu button operation for the Telegram integration.

Args:
    data: Value used by this operation.

Returns:
    Result produced by the operation."""
    'Dispatch a menu-button payload to its subtype on `type`.\n        \n        Args:\n            data: Value of the declared parameter type.\n        \n        \n        Returns:\n            The operation result (``Optional[MenuButton]``).\n        \n    \n    Raises:\n        ValueError: Raised when the operation cannot complete.\n    '
    if data is None:
        return None
    button_type = data.get('type', 'default')
    if button_type == 'commands':
        return MenuButtonCommands.from_dict(data)
    if button_type == 'web_app':
        return MenuButtonWebApp.from_dict(data)
    if button_type == 'default':
        return MenuButtonDefault.from_dict(data)
    raise ValueError(f'unknown MenuButton type: {button_type!r}')

def serialize_menu_button(value: Union[MenuButton, Mapping[str, object]]) -> Dict[str, object]:
    """Provides the serialize menu button operation for the Telegram integration.

Args:
    value: Value used by this operation.

Returns:
    Result produced by the operation."""
    'Serialize a menu-button argument: typed via `to_dict()`, raw\n        mappings pass through.\n    \n    Args:\n        value: Value of the declared parameter type.\n    \n    \n    Returns:\n        The operation result (``Dict[str, object]``).\n    '
    if isinstance(value, (MenuButtonCommands, MenuButtonWebApp, MenuButtonDefault)):
        return value.to_dict()
    return dict(value)

def _serialize_entities(value: Optional[Sequence[Union[MessageEntity, Mapping[str, object]]]]) -> Optional[List[Dict[str, object]]]:
    """Serialize `MessageEntity` lists: typed via `to_dict()`, raw mappings
    pass through."""
    if value is None:
        return None
    return [e.to_dict() if isinstance(e, MessageEntity) else dict(e) for e in value]

def serialize_input_message_content(value: Union[InputMessageContent, Mapping[str, object]]) -> Dict[str, object]:
    """Provides the serialize input message content operation for the Telegram integration.

Args:
    value: Value used by this operation.

Returns:
    Result produced by the operation."""
    'Serialize an inline-result content argument: typed via `to_dict()`,\n        raw mappings pass through.\n    \n    Args:\n        value: Value of the declared parameter type.\n    \n    \n    Returns:\n        The operation result (``Dict[str, object]``).\n    '
    if isinstance(value, (InputTextMessageContent, InputLocationMessageContent, InputVenueMessageContent, InputContactMessageContent, InputInvoiceMessageContent)):
        return value.to_dict()
    return dict(value)

def _serialize_inline_markup(value: Optional[Union[InlineKeyboardMarkup, Mapping[str, object]]]) -> Optional[Dict[str, object]]:
    """_serialize_inline_markup Telegram model helper."""
    if value is None:
        return None
    if isinstance(value, InlineKeyboardMarkup):
        return value.to_dict()
    return dict(value)

def _serialize_inline_content(value: Optional[Union[InputMessageContent, Mapping[str, object]]]) -> Optional[Dict[str, object]]:
    """_serialize_inline_content Telegram model helper."""
    if value is None:
        return None
    return serialize_input_message_content(value)

def _apply_caption_fields(body: Dict[str, object], obj: object) -> None:
    """Copy the shared caption/parse/caption-entities/above-media fields."""
    if obj.caption is not None:
        body['caption'] = obj.caption
    if obj.parse_mode is not None:
        body['parse_mode'] = obj.parse_mode
    entities = _serialize_entities(obj.caption_entities)
    if entities is not None:
        body['caption_entities'] = entities
    if obj.show_caption_above_media is not None:
        body['show_caption_above_media'] = obj.show_caption_above_media

def _apply_result_markup(body: Dict[str, object], obj: object) -> None:
    """Copy `reply_markup` + `input_message_content` when present."""
    markup = _serialize_inline_markup(getattr(obj, 'reply_markup', None))
    if markup is not None:
        body['reply_markup'] = markup
    content = _serialize_inline_content(getattr(obj, 'input_message_content', None))
    if content is not None:
        body['input_message_content'] = content

def _apply_thumbnail_fields(body: Dict[str, object], obj: object) -> None:
    """_apply_thumbnail_fields Telegram model helper."""
    if getattr(obj, 'thumbnail_url', None) is not None:
        body['thumbnail_url'] = obj.thumbnail_url
    if getattr(obj, 'thumbnail_width', None) is not None:
        body['thumbnail_width'] = obj.thumbnail_width
    if getattr(obj, 'thumbnail_height', None) is not None:
        body['thumbnail_height'] = obj.thumbnail_height

def serialize_inline_result(value: Union[InlineQueryResult, Mapping[str, object]]) -> Dict[str, object]:
    """Provides the serialize inline result operation for the Telegram integration.

Args:
    value: Value used by this operation.

Returns:
    Result produced by the operation."""
    'Serialize an inline-query-result argument: typed via `to_dict()`,\n        raw mappings pass through.\n    \n    Args:\n        value: Value of the declared parameter type.\n    \n    \n    Returns:\n        The operation result (``Dict[str, object]``).\n    '
    if isinstance(value, (InlineQueryResultArticle, InlineQueryResultPhoto, InlineQueryResultGif, InlineQueryResultMpeg4Gif, InlineQueryResultVideo, InlineQueryResultAudio, InlineQueryResultVoice, InlineQueryResultDocument, InlineQueryResultLocation, InlineQueryResultVenue, InlineQueryResultContact, InlineQueryResultGame, InlineQueryResultCachedPhoto, InlineQueryResultCachedGif, InlineQueryResultCachedMpeg4Gif, InlineQueryResultCachedSticker, InlineQueryResultCachedDocument, InlineQueryResultCachedVideo, InlineQueryResultCachedVoice, InlineQueryResultCachedAudio)):
        return value.to_dict()
    return dict(value)

def _camel_to_snake(name: str) -> str:
    """_camel_to_snake Telegram model helper."""
    return re.sub('(?<!^)(?=[A-Z])', '_', name).lower()

def _parse_api_value(type_name: str, value: object) -> object:
    """_parse_api_value Telegram model helper."""
    if value is None:
        return None
    t = type_name.strip()
    if t.startswith('Array of '):
        inner = t[len('Array of '):]
        if isinstance(value, list):
            return [_parse_api_value(inner, item) for item in value]
        return value
    if ' or ' in t:
        parser = globals().get('parse_' + _camel_to_snake(t.split(' or ')[0]))
        if parser:
            return parser(value)
        return value
    parser = globals().get('parse_' + _camel_to_snake(t))
    if parser:
        try:
            return parser(value)
        except Exception:
            pass
    model = globals().get(t)
    if model is not None and hasattr(model, 'from_dict') and isinstance(value, dict):
        return model.from_dict(value)
    return value

def _serialize_api_value(value: object) -> object:
    """_serialize_api_value Telegram model helper."""
    if value is None:
        return None
    if hasattr(value, 'to_dict'):
        try:
            return value.to_dict()
        except TypeError:
            pass
    if isinstance(value, Mapping):
        return {k: _serialize_api_value(v) for k, v in value.items()}
    if isinstance(value, (list, tuple)):
        return [_serialize_api_value(v) for v in value]
    if hasattr(value, '__dataclass_fields__'):
        return {k: _serialize_api_value(getattr(value, k)) for k in value.__dataclass_fields__}
    return value

def _parse_api_result(type_name: str, value: object) -> object:
    """_parse_api_result Telegram model helper."""
    if type_name == 'Any':
        return value
    if type_name == 'bool':
        return bool(value)
    if type_name == 'int':
        return int(value) if value is not None else value
    if type_name == 'str':
        return str(value) if value is not None else value
    if type_name.startswith('List[') and type_name.endswith(']'):
        inner = type_name[5:-1]
        return [_parse_api_result(inner, item) for item in value] if isinstance(value, list) else value
    return _parse_api_value(type_name, value)

def parse_reaction_type(data: Optional[dict]) -> Optional[ReactionType]:
    """Provides the parse reaction type operation for the Telegram integration.

Args:
    data: Value used by this operation.

Returns:
    Result produced by the operation."""
    'parse_reaction_type Telegram model helper.\n    \n    Args:\n        data: Value of the declared parameter type.\n    \n    \n    Returns:\n        The operation result (``Optional[ReactionType]``).\n    '
    if data is None:
        return None
    rtype = data.get('type', 'emoji')
    if rtype == 'custom_emoji':
        return ReactionTypeCustomEmoji.from_dict(data)
    if rtype == 'paid':
        return ReactionTypePaid.from_dict(data)
    return ReactionTypeEmoji.from_dict(data)

def parse_message_origin(data: Optional[dict]) -> Optional[MessageOrigin]:
    """Provides the parse message origin operation for the Telegram integration.

Args:
    data: Value used by this operation.

Returns:
    Result produced by the operation."""
    'parse_message_origin Telegram model helper.\n    \n    Args:\n        data: Value of the declared parameter type.\n    \n    \n    Returns:\n        The operation result (``Optional[MessageOrigin]``).\n    '
    if data is None:
        return None
    origin_type = data.get('type', 'user')
    if origin_type == 'hidden_user':
        return MessageOriginHiddenUser.from_dict(data)
    if origin_type == 'chat':
        return MessageOriginChat.from_dict(data)
    if origin_type == 'channel':
        return MessageOriginChannel.from_dict(data)
    return MessageOriginUser.from_dict(data)

def parse_background_fill(data: Optional[dict]) -> Optional[BackgroundFill]:
    """Provides the parse background fill operation for the Telegram integration.

Args:
    data: Value used by this operation.

Returns:
    Result produced by the operation."""
    'parse_background_fill Telegram model helper.\n    \n    Args:\n        data: Value of the declared parameter type.\n    \n    \n    Returns:\n        The operation result (``Optional[BackgroundFill]``).\n    '
    if data is None:
        return None
    ftype = data.get('type', 'solid')
    if ftype == 'gradient':
        return BackgroundFillGradient.from_dict(data)
    if ftype == 'freeform_gradient':
        return BackgroundFillFreeformGradient.from_dict(data)
    return BackgroundFillSolid.from_dict(data)

def parse_background_type(data: Optional[dict]) -> Optional[BackgroundType]:
    """Provides the parse background type operation for the Telegram integration.

Args:
    data: Value used by this operation.

Returns:
    Result produced by the operation."""
    'parse_background_type Telegram model helper.\n    \n    Args:\n        data: Value of the declared parameter type.\n    \n    \n    Returns:\n        The operation result (``Optional[BackgroundType]``).\n    '
    if data is None:
        return None
    btype = data.get('type', 'fill')
    if btype == 'wallpaper':
        return BackgroundTypeWallpaper.from_dict(data)
    if btype == 'pattern':
        return BackgroundTypePattern.from_dict(data)
    if btype == 'chat_theme':
        return BackgroundTypeChatTheme.from_dict(data)
    return BackgroundTypeFill.from_dict(data)

def parse_revenue_withdrawal_state(data: Optional[dict]) -> Optional[RevenueWithdrawalState]:
    """Provides the parse revenue withdrawal state operation for the Telegram integration.

Args:
    data: Value used by this operation.

Returns:
    Result produced by the operation."""
    'parse_revenue_withdrawal_state Telegram model helper.\n    \n    Args:\n        data: Value of the declared parameter type.\n    \n    \n    Returns:\n        The operation result (``Optional[RevenueWithdrawalState]``).\n    '
    if data is None:
        return None
    stype = data.get('type', 'pending')
    if stype == 'succeeded':
        return RevenueWithdrawalStateSucceeded.from_dict(data)
    if stype == 'failed':
        return RevenueWithdrawalStateFailed.from_dict(data)
    return RevenueWithdrawalStatePending.from_dict(data)

def parse_transaction_partner(data: Optional[dict]) -> Optional[TransactionPartner]:
    """Provides the parse transaction partner operation for the Telegram integration.

Args:
    data: Value used by this operation.

Returns:
    Result produced by the operation."""
    'parse_transaction_partner Telegram model helper.\n    \n    Args:\n        data: Value of the declared parameter type.\n    \n    \n    Returns:\n        The operation result (``Optional[TransactionPartner]``).\n    '
    if data is None:
        return None
    partner_type = data.get('type', 'other')
    if partner_type == 'user':
        return TransactionPartnerUser.from_dict(data)
    if partner_type == 'fragment':
        return TransactionPartnerFragment.from_dict(data)
    if partner_type == 'telegram_ads':
        return TransactionPartnerTelegramAds.from_dict(data)
    if partner_type == 'affiliate_program':
        return TransactionPartnerAffiliateProgram.from_dict(data)
    if partner_type == 'chat':
        return TransactionPartnerChat.from_dict(data)
    if partner_type == 'telegram_api':
        return TransactionPartnerTelegramApi.from_dict(data)
    return TransactionPartnerOther.from_dict(data)

def parse_paid_media(data: Optional[dict]) -> Optional[PaidMedia]:
    """Provides the parse paid media operation for the Telegram integration.

Args:
    data: Value used by this operation.

Returns:
    Result produced by the operation."""
    'parse_paid_media Telegram model helper.\n    \n    Args:\n        data: Value of the declared parameter type.\n    \n    \n    Returns:\n        The operation result (``Optional[PaidMedia]``).\n    '
    if data is None:
        return None
    cls = {'live_photo': PaidMediaLivePhoto, 'photo': PaidMediaPhoto, 'preview': PaidMediaPreview, 'video': PaidMediaVideo}.get(data.get('type', ''))
    return cls.from_dict(data) if cls else data

def parse_owned_gift(data: Optional[dict]) -> Optional[OwnedGift]:
    """Provides the parse owned gift operation for the Telegram integration.

Args:
    data: Value used by this operation.

Returns:
    Result produced by the operation."""
    'parse_owned_gift Telegram model helper.\n    \n    Args:\n        data: Value of the declared parameter type.\n    \n    \n    Returns:\n        The operation result (``Optional[OwnedGift]``).\n    '
    if data is None:
        return None
    cls = {'regular': OwnedGiftRegular, 'unique': OwnedGiftUnique}.get(data.get('type'), OwnedGiftRegular)
    return cls.from_dict(data)

def parse_input_media(data: Optional[dict]) -> Optional[InputMedia]:
    """Provides the parse input media operation for the Telegram integration.

Args:
    data: Value used by this operation.

Returns:
    Result produced by the operation."""
    'parse_input_media Telegram model helper.\n    \n    Args:\n        data: Value of the declared parameter type.\n    \n    \n    Returns:\n        The operation result (``Optional[InputMedia]``).\n    '
    if data is None:
        return None
    cls = {'animation': InputMediaAnimation, 'audio': InputMediaAudio, 'document': InputMediaDocument, 'live_photo': InputMediaLivePhoto, 'photo': InputMediaPhoto, 'video': InputMediaVideo}.get(data.get('type', ''))
    return cls.from_dict(data) if cls else data

def parse_input_paid_media(data: Optional[dict]) -> Optional[InputPaidMedia]:
    """Provides the parse input paid media operation for the Telegram integration.

Args:
    data: Value used by this operation.

Returns:
    Result produced by the operation."""
    'parse_input_paid_media Telegram model helper.\n    \n    Args:\n        data: Value of the declared parameter type.\n    \n    \n    Returns:\n        The operation result (``Optional[InputPaidMedia]``).\n    '
    if data is None:
        return None
    cls = {'live_photo': InputPaidMediaLivePhoto, 'photo': InputPaidMediaPhoto, 'video': InputPaidMediaVideo}.get(data.get('type', ''))
    return cls.from_dict(data) if cls else data

def parse_input_story_content(data: Optional[dict]) -> Optional[InputStoryContent]:
    """Provides the parse input story content operation for the Telegram integration.

Args:
    data: Value used by this operation.

Returns:
    Result produced by the operation."""
    'parse_input_story_content Telegram model helper.\n    \n    Args:\n        data: Value of the declared parameter type.\n    \n    \n    Returns:\n        The operation result (``Optional[InputStoryContent]``).\n    '
    if data is None:
        return None
    cls = {'photo': InputStoryContentPhoto, 'video': InputStoryContentVideo}.get(data.get('type', ''))
    return cls.from_dict(data) if cls else data

def parse_passport_element_error(data: Optional[dict]) -> Optional[PassportElementError]:
    """Provides the parse passport element error operation for the Telegram integration.

Args:
    data: Value used by this operation.

Returns:
    Result produced by the operation."""
    'parse_passport_element_error Telegram model helper.\n    \n    Args:\n        data: Value of the declared parameter type.\n    \n    \n    Returns:\n        The operation result (``Optional[PassportElementError]``).\n    '
    if data is None:
        return None
    cls = {'data': PassportElementErrorDataField, 'front_side': PassportElementErrorFrontSide, 'reverse_side': PassportElementErrorReverseSide, 'selfie': PassportElementErrorSelfie, 'file': PassportElementErrorFile, 'files': PassportElementErrorFiles, 'translation_file': PassportElementErrorTranslationFile, 'translation_files': PassportElementErrorTranslationFiles, 'unspecified': PassportElementErrorUnspecified}.get(data.get('source', ''))
    return cls.from_dict(data) if cls else data

def parse_chat_boost_source(data: Optional[dict]) -> Optional[ChatBoostSource]:
    """Provides the parse chat boost source operation for the Telegram integration.

Args:
    data: Value used by this operation.

Returns:
    Result produced by the operation."""
    'parse_chat_boost_source Telegram model helper.\n    \n    Args:\n        data: Value of the declared parameter type.\n    \n    \n    Returns:\n        The operation result (``Optional[ChatBoostSource]``).\n    '
    if data is None:
        return None
    source = data.get('source')
    cls = {'premium': ChatBoostSourcePremium, 'gift_code': ChatBoostSourceGiftCode, 'giveaway': ChatBoostSourceGiveaway}.get(source)
    return cls.from_dict(data) if cls is not None else None

def _patch_from_dict_attrs(cls, attrs):
    """_patch_from_dict_attrs Telegram model helper."""
    old = cls.from_dict.__func__

    @classmethod
    def _from_dict(c, data):
        obj = old(c, data)
        if obj is None:
            return None
        for name, parser in attrs.items():
            raw_name = name
            if isinstance(parser, tuple):
                raw_name, parser = parser
            raw = data.get(raw_name)
            setattr(obj, name, parser(raw) if parser is not None else raw)
        return obj
    cls.from_dict = _from_dict
    for name in attrs:
        if name not in getattr(cls, '__annotations__', {}):
            setattr(cls, name, None)
    return cls

def _shipping_option_to_dict(self):
    """_shipping_option_to_dict Telegram model helper."""
    return {'id': self.id, 'title': self.title, 'prices': [_serialize_api_value(p) for p in self.prices or []]}

def _passport_cls(name, source, extra_fields):
    """_passport_cls Telegram model helper."""
    annotations = {k: t for k, t in extra_fields}
    annotations['source'] = str
    namespace = {'__annotations__': annotations, 'source': source}

    @classmethod
    def from_dict(cls, data):
        """Executes the from_dict operation.
        
        Args:
            data: Value of the declared parameter type.
        
        
        Returns:
            The operation result (``Any``).
        """
        if data is None:
            return None
        kw = {'source': data.get('source', source)}
        for k, _ in extra_fields:
            kw[k] = data.get(k)
        return cls(**kw)
    namespace['from_dict'] = from_dict

    @classmethod
    def list_from(cls, data):
        """Executes the list_from operation.
        
        Args:
            data: Value of the declared parameter type.
        
        
        Returns:
            The operation result (``Any``).
        """
        return [cls.from_dict(x) for x in data or []]
    namespace['list_from'] = list_from

    def to_dict(self):
        """Executes the to_dict operation.
        
        Returns:
            The operation result (``Any``).
        """
        return {k: getattr(self, k) for k in annotations if getattr(self, k, None) is not None}
    namespace['to_dict'] = to_dict
    return dataclass(type(name, (), namespace))

def _ogr_from_dict(cls, data):
    """_ogr_from_dict Telegram model helper."""
    obj = _old_ogr(cls, data)
    if obj is not None:
        obj.date = data.get('date', data.get('send_date'))
    return obj

def _ogu_from_dict(cls, data):
    """_ogu_from_dict Telegram model helper."""
    obj = _old_ogu(cls, data)
    if obj is not None:
        obj.date = data.get('date', data.get('send_date'))
    return obj

def _wad_from_dict(cls, data):
    """_wad_from_dict Telegram model helper."""
    obj = _old_wad(cls, data)
    if obj is not None and getattr(obj, 'button_text', None) is None:
        obj.button_text = ''
    return obj

def _msg_from_dict_compat(cls, data):
    """_msg_from_dict_compat Telegram model helper."""
    obj = _old_msg2(cls, data)
    if obj is not None and 'direct_messages_topic' in data:
        obj.direct_messages_topic = data.get('direct_messages_topic')
    return obj

def _ogu_from_dict_compat(cls, data):
    """_ogu_from_dict_compat Telegram model helper."""
    obj = _old_ogu2(cls, data)
    if obj is not None:
        obj.date = data.get('date', data.get('send_date'))
        obj.is_private = data.get('is_private')
    return obj
