"""Static assertion samples for the three platform clients."""
from __future__ import annotations
from typing import Awaitable, Callable, assert_type
from peyk.platforms.telegram.client import TelegramClient
from peyk.platforms.telegram.models import ChatFullInfo, ChatMember, File, Message, User, WebhookInfo
from peyk.platforms.bale.client import BaleClient
from peyk.platforms.bale.models import Chat, ChatMember, File as BaleFile, Message as BaleMessage, User as BaleUser, WebhookInfo as BaleWebhookInfo
from peyk.platforms.rubika.client import RubikaClient
from peyk.platforms.rubika.models import Bot, Chat as RubikaChat, Message as RubikaMessage, Update

def test_telegram_client_method_types() -> None:
    assert_type(TelegramClient.get_me, Callable[..., Awaitable[User]])
    assert_type(TelegramClient.get_webhook_info, Callable[..., Awaitable[WebhookInfo]])
    assert_type(TelegramClient.get_file, Callable[..., Awaitable[File]])
    assert_type(TelegramClient.get_chat, Callable[..., Awaitable[ChatFullInfo]])
    assert_type(TelegramClient.get_chat_member, Callable[..., Awaitable[ChatMember]])
    assert_type(TelegramClient.delete_message, Callable[..., Awaitable[bool]])
    assert_type(TelegramClient.leave_chat, Callable[..., Awaitable[bool]])
    assert_type(TelegramClient.set_chat_title, Callable[..., Awaitable[bool]])
    assert_type(TelegramClient.send_message, Callable[..., Awaitable[Message]])
    assert_type(TelegramClient.send_media_group, Callable[..., Awaitable[list[Message]]])

def test_bale_client_method_types() -> None:
    assert_type(BaleClient.get_me, Callable[..., Awaitable[BaleUser]])
    assert_type(BaleClient.get_webhook_info, Callable[..., Awaitable[BaleWebhookInfo]])
    assert_type(BaleClient.get_file, Callable[..., Awaitable[BaleFile]])
    assert_type(BaleClient.get_chat, Callable[..., Awaitable[Chat]])
    assert_type(BaleClient.get_chat_member, Callable[..., Awaitable[ChatMember]])
    assert_type(BaleClient.delete_message, Callable[..., Awaitable[bool]])
    assert_type(BaleClient.send_message, Callable[..., Awaitable[BaleMessage]])
    assert_type(BaleClient.send_photo, Callable[..., Awaitable[BaleMessage]])
    assert_type(BaleClient.send_video, Callable[..., Awaitable[BaleMessage]])
    assert_type(BaleClient.send_media_group, Callable[..., Awaitable[list[BaleMessage]]])

def test_rubika_client_method_types() -> None:
    assert_type(RubikaClient.get_me, Callable[..., Awaitable[Bot]])
    assert_type(RubikaClient.get_chat, Callable[..., Awaitable[RubikaChat]])
    assert_type(RubikaClient.get_file, Callable[..., Awaitable[str]])
    assert_type(RubikaClient.get_updates, Callable[..., Awaitable[tuple[list[Update], str | None]]])
    assert_type(RubikaClient.send_message, Callable[..., Awaitable[RubikaMessage]])
    assert_type(RubikaClient.send_contact, Callable[..., Awaitable[RubikaMessage]])
    assert_type(RubikaClient.send_file, Callable[..., Awaitable[RubikaMessage]])
    assert_type(RubikaClient.send_location, Callable[..., Awaitable[RubikaMessage]])
    assert_type(RubikaClient.send_poll, Callable[..., Awaitable[RubikaMessage]])
    assert_type(RubikaClient.delete_message, Callable[..., Awaitable[bool]])
