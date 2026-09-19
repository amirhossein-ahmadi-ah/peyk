"""Static type assertions for the shared client and normalized adapters."""

from __future__ import annotations

from typing import TYPE_CHECKING, assert_type, cast

from peyk.platform_core.adapters.bale import normalize_update as normalize_bale_update
from peyk.platform_core.adapters.rubika import normalize_update as normalize_rubika_update
from peyk.platform_core.adapters.telegram import normalize_update as normalize_telegram_update
from peyk.platform_core.contracts import (
    IncomingBotMembershipChange,
    IncomingCallbackQuery,
    IncomingChatMemberStatusUpdate,
    IncomingMessage,
    IncomingMessageDeleted,
    IncomingPreCheckoutQuery,
    IncomingShippingQuery,
)
from peyk.platforms.bale.client import BaleClient
from peyk.platforms.bale.models import Chat as BaleChat
from peyk.platforms.bale.models import ChatMember as BaleChatMember
from peyk.platforms.bale.models import File as BaleFile
from peyk.platforms.bale.models import Update as BaleUpdate
from peyk.platforms.bale.models import User as BaleUser
from peyk.platforms.bale.models import WebhookInfo as BaleWebhookInfo
from peyk.platforms.rubika.models import Update as RubikaUpdate
from peyk.platforms.telegram.client import TelegramClient
from peyk import Chat, TelegramBot
from peyk.platforms.telegram.models import ChatFullInfo as TelegramChat
from peyk.platforms.telegram.models import ChatMember as TelegramChatMember
from peyk.platforms.telegram.models import File as TelegramFile
from peyk.platforms.telegram.models import Update as TelegramUpdate
from peyk.platforms.telegram.models import User as TelegramUser
from peyk.platforms.telegram.models import WebhookInfo as TelegramWebhookInfo


if TYPE_CHECKING:
    async def test_bale_client_types() -> None:
        client = cast(BaleClient, object())
        assert_type(await client.get_me(), BaleUser)
        assert_type(await client.get_webhook_info(), BaleWebhookInfo)
        assert_type(await client.get_file("file"), BaleFile)
        assert_type(await client.get_chat(1), BaleChat)
        assert_type(await client.get_chat_member(1, 2), BaleChatMember)

    async def test_bot_types() -> None:
        bot = cast(TelegramBot, object())
        assert_type(bot.client, TelegramClient)
        assert_type(await bot.get_chat(1), Chat)

    async def test_telegram_client_types() -> None:
        client = cast(TelegramClient, object())
        assert_type(await client.get_me(), TelegramUser)
        assert_type(await client.get_webhook_info(), TelegramWebhookInfo)
        assert_type(await client.get_file("file"), TelegramFile)
        assert_type(await client.get_chat(1), TelegramChat)
        assert_type(await client.get_chat_member(1, 2), TelegramChatMember)

    BaleNormalized = (
        IncomingMessage
        | IncomingCallbackQuery
        | IncomingPreCheckoutQuery
        | BaleUpdate
    )
    TelegramNormalized = (
        IncomingMessage
        | IncomingCallbackQuery
        | IncomingChatMemberStatusUpdate
        | IncomingPreCheckoutQuery
        | IncomingShippingQuery
        | TelegramUpdate
    )
    RubikaNormalized = (
        IncomingMessage
        | IncomingMessageDeleted
        | IncomingBotMembershipChange
        | RubikaUpdate
    )

    assert_type(normalize_bale_update(cast(BaleUpdate, object())), BaleNormalized)
    assert_type(
        normalize_telegram_update(cast(TelegramUpdate, object())), TelegramNormalized
    )
    assert_type(normalize_rubika_update(cast(RubikaUpdate, object())), RubikaNormalized)
