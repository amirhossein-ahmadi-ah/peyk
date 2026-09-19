"""Compatibility facade for Telegram Bot API models.

All T1-T18 concrete types now live under ``platforms.telegram.types``.
This module deliberately retains the historical import path and the small
compatibility patches that were part of the pre-refactor model surface.
"""

from __future__ import annotations

from types import SimpleNamespace as _SimpleNamespace

from .errors import ResponseParameters
from .types import *  # noqa: F401,F403
from .types import (
    _helpers,
    _aliases,
)

# Private helpers/constants historically imported by ``client.py`` and by
# downstream users remain available from this facade.
for _name, _value in vars(_helpers).items():
    if _name.startswith("_") or _name in {"validate_callback_data"}:
        globals()[_name] = _value
for _name, _value in vars(_aliases).items():
    if not _name.startswith("_"):
        globals()[_name] = _value

# Explicit public compatibility names that are easiest to discover from the
# old module.
validate_callback_data = _helpers.validate_callback_data
MAX_CALLBACK_DATA_BYTES = _aliases.MAX_CALLBACK_DATA_BYTES

# Preserve the legacy post-definition parsing patches exactly. They are
# compatibility behavior, not model implementations.
_patch_from_dict_attrs(User, {
    'supports_guest_queries': None,
    'supports_join_request_queries': None,
})

_patch_from_dict_attrs(ChatFullInfo, {
    'guard_bot': lambda v: User.from_dict(v),
    'community': lambda v: Community.from_dict(v),
})

_patch_from_dict_attrs(Message, {
    'receiver_user': lambda v: User.from_dict(v),
    'ephemeral_message_id': None,
    'guest_bot_caller_user': lambda v: User.from_dict(v),
    'guest_bot_caller_chat': lambda v: Chat.from_dict(v),
    'guest_query_id': None,
    'community_chat_joined': lambda v: CommunityChatJoined.from_dict(v),
    'community_chat_added': lambda v: CommunityChatAdded.from_dict(v),
    'community_chat_removed': lambda v: CommunityChatRemoved.from_dict(v),
    'rich_message': None,
    'checklist': None,
    'suggested_post_info': None,
    'paid_star_count': None,
    'sender_tag': None,
    'edit_date': None,
    'has_protected_content': None,
    'is_from_offline': None,
    'is_paid_post': None,
    'media_group_id': None,
    'direct_messages_topic': lambda v: DirectMessagesTopic.from_dict(v),
    'chat_owner_left': lambda v: ChatOwnerLeft.from_dict(v),
    'chat_owner_changed': lambda v: ChatOwnerChanged.from_dict(v),
    'refunded_payment': lambda v: RefundedPayment.from_dict(v),
    'passport_data': lambda v: PassportData.from_dict(v),
    'game': lambda v: Game.from_dict(v),
    'invoice': lambda v: Invoice.from_dict(v),
    'successful_payment': lambda v: SuccessfulPayment.from_dict(v),
    'web_app_data': lambda v: WebAppData.from_dict(v),
    'giveaway': lambda v: Giveaway.from_dict(v),
    'giveaway_winners': lambda v: GiveawayWinners.from_dict(v),
    'giveaway_completed': lambda v: GiveawayCompleted.from_dict(v),
    'chat_boost': lambda v: ChatBoostUpdated.from_dict(v),
    'removed_chat_boost': lambda v: ChatBoostRemoved.from_dict(v),
})

_patch_from_dict_attrs(Update, {
    'subscription': lambda v: _SimpleNamespace(subscription=v.get('subscription') if isinstance(v, dict) else None) if v is not None else None,
    'guest_message': lambda v: Message.from_dict(v),
    'managed_bot': None,
    'stopped_message_generation': lambda v: MessageGenerationStopped.from_dict(v),
    'business_connection': lambda v: BusinessConnection.from_dict(v),
    'chat_boost': lambda v: ChatBoostUpdated.from_dict(v),
    'removed_chat_boost': lambda v: ChatBoostRemoved.from_dict(v),
})

_patch_from_dict_attrs(BusinessConnection, {'can_reply': None})
_patch_from_dict_attrs(BotSubscriptionUpdated, {'subscription': lambda v: _SimpleNamespace(**v) if isinstance(v, dict) else None})
_patch_from_dict_attrs(GiveawayCompleted, {'giveaway_message_id': None})
_patch_from_dict_attrs(UniqueGift, {'id': None, 'title': None})
_patch_from_dict_attrs(OwnedGiftRegular, {'date': ('send_date', None)})
_patch_from_dict_attrs(OwnedGiftUnique, {'date': ('send_date', None)})
_patch_from_dict_attrs(WebAppData, {'button_text': None})

# Preserve the final compatibility overrides for gift/payment models.
_old_ogr = OwnedGiftRegular.from_dict.__func__
@classmethod
def _ogr_from_dict(cls, data):
    obj = _old_ogr(cls, data)
    if obj is not None:
        obj.date = data.get('date', data.get('send_date'))
    return obj
OwnedGiftRegular.from_dict = _ogr_from_dict

_old_ogu = OwnedGiftUnique.from_dict.__func__
@classmethod
def _ogu_from_dict(cls, data):
    obj = _old_ogu(cls, data)
    if obj is not None:
        obj.date = data.get('date', data.get('send_date'))
    return obj
OwnedGiftUnique.from_dict = _ogu_from_dict

_old_wad = WebAppData.from_dict.__func__
@classmethod
def _wad_from_dict(cls, data):
    obj = _old_wad(cls, data)
    if obj is not None and getattr(obj, 'button_text', None) is None:
        obj.button_text = ''
    return obj
WebAppData.from_dict = _wad_from_dict

_old_msg2 = Message.from_dict.__func__
@classmethod
def _msg_from_dict_compat(cls, data):
    obj = _old_msg2(cls, data)
    if obj is not None and 'direct_messages_topic' in data:
        obj.direct_messages_topic = data.get('direct_messages_topic')
    return obj
Message.from_dict = _msg_from_dict_compat

_old_ogu2 = OwnedGiftUnique.from_dict.__func__
@classmethod
def _ogu_from_dict_compat(cls, data):
    obj = _old_ogu2(cls, data)
    if obj is not None:
        obj.date = data.get('date', data.get('send_date'))
        obj.is_private = data.get('is_private')
    return obj
OwnedGiftUnique.from_dict = _ogu_from_dict_compat

ShippingOption.to_dict = _shipping_option_to_dict

__all__ = ['AcceptedGiftTypes', 'AffiliateInfo', 'Animation', 'Audio', 'BackgroundFill', 'BackgroundFillFreeformGradient', 'BackgroundFillGradient', 'BackgroundFillSolid', 'BackgroundType', 'BackgroundTypeChatTheme', 'BackgroundTypeFill', 'BackgroundTypePattern', 'BackgroundTypeWallpaper', 'Birthdate', 'BotAccessSettings', 'BotCommand', 'BotCommandScope', 'BotCommandScopeAllChatAdministrators', 'BotCommandScopeAllGroupChats', 'BotCommandScopeAllPrivateChats', 'BotCommandScopeChat', 'BotCommandScopeChatAdministrators', 'BotCommandScopeChatMember', 'BotCommandScopeDefault', 'BotDescription', 'BotName', 'BotShortDescription', 'BotSubscriptionUpdated', 'BusinessBotRights', 'BusinessConnection', 'BusinessIntro', 'BusinessLocation', 'BusinessMessagesDeleted', 'BusinessOpeningHours', 'BusinessOpeningHoursInterval', 'CallbackGame', 'CallbackQuery', 'Chat', 'ChatAdministratorRights', 'ChatBackground', 'ChatBoost', 'ChatBoostAdded', 'ChatBoostRemoved', 'ChatBoostSource', 'ChatBoostSourceGiftCode', 'ChatBoostSourceGiveaway', 'ChatBoostSourcePremium', 'ChatBoostUpdated', 'ChatFullInfo', 'ChatInviteLink', 'ChatJoinRequest', 'ChatLocation', 'ChatMember', 'ChatMemberAdministrator', 'ChatMemberBanned', 'ChatMemberLeft', 'ChatMemberMember', 'ChatMemberOwner', 'ChatMemberRestricted', 'ChatMemberUpdated', 'ChatOwnerChanged', 'ChatOwnerLeft', 'ChatPermissions', 'ChatPhoto', 'ChatShared', 'Checklist', 'ChecklistTask', 'ChecklistTasksAdded', 'ChecklistTasksDone', 'ChosenInlineResult', 'Community', 'CommunityChatAdded', 'CommunityChatJoined', 'CommunityChatRemoved', 'Contact', 'CopyTextButton', 'Dice', 'DirectMessagePriceChanged', 'DirectMessagesTopic', 'DisabledButton', 'Document', 'EncryptedCredentials', 'EncryptedPassportElement', 'EphemeralMessageParameters', 'ExternalReplyInfo', 'File', 'ForceReply', 'ForumTopic', 'ForumTopicClosed', 'ForumTopicCreated', 'ForumTopicEdited', 'ForumTopicReopened', 'Game', 'GameHighScore', 'GeneralForumTopicHidden', 'GeneralForumTopicUnhidden', 'Gift', 'GiftBackground', 'GiftInfo', 'Gifts', 'Giveaway', 'GiveawayCompleted', 'GiveawayCreated', 'GiveawayWinners', 'InaccessibleMessage', 'InlineKeyboardButton', 'InlineKeyboardMarkup', 'InlineQuery', 'InlineQueryResult', 'InlineQueryResultArticle', 'InlineQueryResultAudio', 'InlineQueryResultCachedAudio', 'InlineQueryResultCachedDocument', 'InlineQueryResultCachedGif', 'InlineQueryResultCachedMpeg4Gif', 'InlineQueryResultCachedPhoto', 'InlineQueryResultCachedSticker', 'InlineQueryResultCachedVideo', 'InlineQueryResultCachedVoice', 'InlineQueryResultContact', 'InlineQueryResultDocument', 'InlineQueryResultGame', 'InlineQueryResultGif', 'InlineQueryResultLocation', 'InlineQueryResultMpeg4Gif', 'InlineQueryResultPhoto', 'InlineQueryResultVenue', 'InlineQueryResultVideo', 'InlineQueryResultVoice', 'InlineQueryResultsButton', 'InputChecklist', 'InputChecklistTask', 'InputContactMessageContent', 'InputFile', 'InputInvoiceMessageContent', 'InputLocationMessageContent', 'InputMedia', 'InputMediaAnimation', 'InputMediaAudio', 'InputMediaDocument', 'InputMediaItem', 'InputMediaLink', 'InputMediaLivePhoto', 'InputMediaLocation', 'InputMediaPhoto', 'InputMediaSticker', 'InputMediaVenue', 'InputMediaVideo', 'InputMediaVoiceNote', 'InputMessageContent', 'InputPaidMedia', 'InputPaidMediaLivePhoto', 'InputPaidMediaPhoto', 'InputPaidMediaVideo', 'InputPollMedia', 'InputPollOption', 'InputPollOptionMedia', 'InputProfilePhoto', 'InputProfilePhotoAnimated', 'InputProfilePhotoStatic', 'InputRichBlock', 'InputRichBlockAnchor', 'InputRichBlockAnimation', 'InputRichBlockAudio', 'InputRichBlockBlockQuotation', 'InputRichBlockButtons', 'InputRichBlockCollage', 'InputRichBlockDetails', 'InputRichBlockDivider', 'InputRichBlockDocument', 'InputRichBlockExpandableBlockQuotation', 'InputRichBlockFooter', 'InputRichBlockList', 'InputRichBlockListItem', 'InputRichBlockMap', 'InputRichBlockMathematicalExpression', 'InputRichBlockParagraph', 'InputRichBlockPhoto', 'InputRichBlockPreformatted', 'InputRichBlockPullQuotation', 'InputRichBlockSectionHeading', 'InputRichBlockSlideshow', 'InputRichBlockTable', 'InputRichBlockThinking', 'InputRichBlockVideo', 'InputRichBlockVoiceNote', 'InputRichMessage', 'InputRichMessageContent', 'InputRichMessageMedia', 'InputSticker', 'InputStoryContent', 'InputStoryContentPhoto', 'InputStoryContentVideo', 'InputTextMessageContent', 'InputVenueMessageContent', 'Invoice', 'KeyboardButton', 'KeyboardButtonPollType', 'KeyboardButtonRequestChat', 'KeyboardButtonRequestManagedBot', 'KeyboardButtonRequestUsers', 'LabeledPrice', 'Link', 'LinkPreviewOptions', 'LivePhoto', 'Location', 'LocationAddress', 'LoginUrl', 'MAX_CALLBACK_DATA_BYTES', 'ManagedBotCreated', 'ManagedBotUpdated', 'MaskPosition', 'MaybeInaccessibleMessage', 'MenuButton', 'MenuButtonCommands', 'MenuButtonDefault', 'MenuButtonWebApp', 'Message', 'MessageAutoDeleteTimerChanged', 'MessageEntity', 'MessageGenerationStopped', 'MessageId', 'MessageOrigin', 'MessageOriginChannel', 'MessageOriginChat', 'MessageOriginHiddenUser', 'MessageOriginUser', 'MessageReactionCountUpdated', 'MessageReactionUpdated', 'OrderInfo', 'OwnedGift', 'OwnedGiftRegular', 'OwnedGiftUnique', 'OwnedGifts', 'PaidMedia', 'PaidMediaInfo', 'PaidMediaLivePhoto', 'PaidMediaPhoto', 'PaidMediaPreview', 'PaidMediaPurchased', 'PaidMediaVideo', 'PaidMessagePriceChanged', 'PassportData', 'PassportElementError', 'PassportElementErrorDataField', 'PassportElementErrorFile', 'PassportElementErrorFiles', 'PassportElementErrorFrontSide', 'PassportElementErrorReverseSide', 'PassportElementErrorSelfie', 'PassportElementErrorTranslationFile', 'PassportElementErrorTranslationFiles', 'PassportElementErrorUnspecified', 'PassportFile', 'PhotoSize', 'Poll', 'PollAnswer', 'PollMedia', 'PollOption', 'PollOptionAdded', 'PollOptionDeleted', 'PreCheckoutQuery', 'PreparedInlineMessage', 'PreparedKeyboardButton', 'ProximityAlertTriggered', 'ReactionCount', 'ReactionType', 'ReactionTypeCustomEmoji', 'ReactionTypeEmoji', 'ReactionTypePaid', 'RefundedPayment', 'ReplyKeyboardMarkup', 'ReplyKeyboardRemove', 'ReplyMarkup', 'ReplyParameters', 'ResponseParameters', 'RevenueWithdrawalState', 'RevenueWithdrawalStateFailed', 'RevenueWithdrawalStatePending', 'RevenueWithdrawalStateSucceeded', 'RichBlock', 'RichBlockAnchor', 'RichBlockAnimation', 'RichBlockAudio', 'RichBlockBlockQuotation', 'RichBlockButtons', 'RichBlockCaption', 'RichBlockCollage', 'RichBlockDetails', 'RichBlockDivider', 'RichBlockDocument', 'RichBlockExpandableBlockQuotation', 'RichBlockFooter', 'RichBlockList', 'RichBlockListItem', 'RichBlockMap', 'RichBlockMathematicalExpression', 'RichBlockParagraph', 'RichBlockPhoto', 'RichBlockPreformatted', 'RichBlockPullQuotation', 'RichBlockSectionHeading', 'RichBlockSlideshow', 'RichBlockTable', 'RichBlockTableCell', 'RichBlockThinking', 'RichBlockVideo', 'RichBlockVoiceNote', 'RichMessage', 'RichMessageButton', 'RichText', 'RichTextAnchor', 'RichTextAnchorLink', 'RichTextBankCardNumber', 'RichTextBold', 'RichTextBotCommand', 'RichTextButton', 'RichTextCashtag', 'RichTextCode', 'RichTextCustomEmoji', 'RichTextDateTime', 'RichTextEmailAddress', 'RichTextHashtag', 'RichTextItalic', 'RichTextMarked', 'RichTextMathematicalExpression', 'RichTextMention', 'RichTextPhoneNumber', 'RichTextReference', 'RichTextReferenceLink', 'RichTextSpoiler', 'RichTextStrikethrough', 'RichTextSubscript', 'RichTextSuperscript', 'RichTextTextMention', 'RichTextUnderline', 'RichTextUrl', 'SentGuestMessage', 'SentWebAppMessage', 'SharedUser', 'ShippingAddress', 'ShippingOption', 'ShippingQuery', 'StarAmount', 'StarTransaction', 'StarTransactions', 'Sticker', 'StickerSet', 'Story', 'StoryArea', 'StoryAreaPosition', 'StoryAreaType', 'StoryAreaTypeLink', 'StoryAreaTypeLocation', 'StoryAreaTypeSuggestedReaction', 'StoryAreaTypeUniqueGift', 'StoryAreaTypeWeather', 'SuccessfulPayment', 'SuggestedPostApprovalFailed', 'SuggestedPostApproved', 'SuggestedPostDeclined', 'SuggestedPostInfo', 'SuggestedPostPaid', 'SuggestedPostParameters', 'SuggestedPostPrice', 'SuggestedPostRefunded', 'SwitchInlineQueryChosenChat', 'TextQuote', 'TransactionPartner', 'TransactionPartnerAffiliateProgram', 'TransactionPartnerChat', 'TransactionPartnerFragment', 'TransactionPartnerOther', 'TransactionPartnerTelegramAds', 'TransactionPartnerTelegramApi', 'TransactionPartnerUser', 'UniqueGift', 'UniqueGiftBackdrop', 'UniqueGiftBackdropColors', 'UniqueGiftColors', 'UniqueGiftInfo', 'UniqueGiftModel', 'UniqueGiftSymbol', 'Update', 'User', 'UserChatBoosts', 'UserProfileAudios', 'UserProfilePhotos', 'UserRating', 'UsersShared', 'Venue', 'Video', 'VideoChatEnded', 'VideoChatParticipantsInvited', 'VideoChatScheduled', 'VideoChatStarted', 'VideoNote', 'VideoQuality', 'Voice', 'WebAppData', 'WebAppInfo', 'WebhookInfo', 'WriteAccessAllowed', 'parse_background_fill', 'parse_background_type', 'parse_bot_command_scope', 'parse_chat_boost_source', 'parse_chat_member', 'parse_input_media', 'parse_input_paid_media', 'parse_input_story_content', 'parse_maybe_inaccessible_message', 'parse_menu_button', 'parse_message_origin', 'parse_owned_gift', 'parse_paid_media', 'parse_passport_element_error', 'parse_reaction_type', 'parse_revenue_withdrawal_state', 'parse_transaction_partner', 'serialize_bot_command_scope', 'serialize_inline_result', 'serialize_input_message_content', 'serialize_menu_button', 'serialize_reply_markup', 'validate_callback_data']
