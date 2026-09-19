from __future__ import annotations

import pytest
from aiohttp import web
from aiohttp.test_utils import TestServer

from peyk import BaleBot, Bot, BotNotBoundError, RubikaBot, TelegramBot
from peyk.types import Message
from peyk.platform_core.errors import UnsupportedFeatureError


def _tg_msg(mid: int = 1) -> dict:
    return {"message_id": mid, "date": 1, "chat": {"id": 10, "type": "private"}, "from": {"id": 20, "is_bot": False, "first_name": "U"}, "text": "ok"}

@pytest.fixture
async def server():
    async def handle(request: web.Request) -> web.Response:
        method = request.match_info["method"]
        if method == "requestSendFile":
            return web.json_response({"status": "OK", "data": {"upload_url": str(request.url.with_path("/upload/file"))}})
        if method == "getChatMember":
            body = {"status": "member", "user": {"id": 20, "is_bot": False, "first_name": "U"}}
            if request.path.startswith("/v3/"):
                return web.json_response({"status": "OK", "data": body})
            return web.json_response({"ok": True, "result": body})
        if method == "getMe" and request.path.startswith("/v3/"):
            return web.json_response({"status": "OK", "data": {"bot": {"bot_id": "b1", "bot_title": "Rubot", "username": "rubot"}}})
        if request.path.startswith("/v3/"):
            if method == "getChat":
                return web.json_response({"status": "OK", "data": {"chat": {"chat_id": "c1", "chat_type": "User", "username": "u"}}})
            return web.json_response({"status": "OK", "data": {"message_id": "m1", "text": "ok"}})
        if method == "getMe":
            return web.json_response({"ok": True, "result": {"id": 1, "is_bot": True, "first_name": "Bot"}})
        if method == "getChat":
            return web.json_response({"ok": True, "result": {"id": 10, "type": "private", "username": "u"}})
        return web.json_response({"ok": True, "result": _tg_msg()})
    async def upload(request: web.Request) -> web.Response:
        reader = await request.multipart()
        async for part in reader:
            await part.read()
        return web.json_response({"file_id": "f1"})
    app = web.Application()
    app.router.add_post("/bot{token}/{method}", handle)
    app.router.add_post("/v3/{token}/{method}", handle)
    app.router.add_post("/upload/file", upload)
    async with TestServer(app) as ts:
        yield str(ts.make_url(""))

@pytest.mark.asyncio
async def test_bot_send_message_and_client_types(server: str) -> None:
    tg = TelegramBot("T", base_url=server)
    bale = BaleBot("B", base_url=server)
    rubika = RubikaBot("R", base_url=server + "/v3")
    try:
        assert tg.client.__class__.__name__ == "TelegramClient"
        assert bale.client.__class__.__name__ == "BaleClient"
        assert rubika.client.__class__.__name__ == "RubikaClient"
        for bot in (tg, bale):
            msg = await bot.send_message(10, "hi")
            assert isinstance(msg, Message)
            assert msg.chat_id == 10
        msg = await rubika.send_message("c1", "hi")
        assert isinstance(msg, Message)
        assert msg.chat_id == "c1"
    finally:
        await tg.close(); await bale.close(); await rubika.close()

@pytest.mark.asyncio
async def test_rubika_media_uses_upload_flow(server: str) -> None:
    bot = RubikaBot("R", base_url=server + "/v3")
    try:
        msg = await bot.send_photo("c1", b"image")
        assert isinstance(msg, Message)
    finally:
        await bot.close()

@pytest.mark.asyncio
async def test_rubika_normalized_message_binds_enclosing_chat(server: str) -> None:
    from peyk.platforms.rubika.types import Message as RawMessage, Update
    bot = RubikaBot("R", base_url=server)
    try:
        event = bot.normalize_update(Update(type="NewMessage", chat_id="c1", new_message=RawMessage(message_id="m1", text="hi", sender_id="u1")))
        assert isinstance(event, Message)
        assert event.chat_id == "c1"
        assert event.bot is bot
    finally:
        await bot.close()

@pytest.mark.asyncio
async def test_unbound_message_actions_raise() -> None:
    msg = Message(message_id=1, chat_id=1, text="x")
    with pytest.raises(BotNotBoundError):
        await msg.answer("hi")

@pytest.mark.asyncio
async def test_unknown_callback_answer_degrades_once(server: str) -> None:
    bot = RubikaBot("R", base_url=server + "/v3")
    try:
        from peyk.types import CallbackQuery
        event = CallbackQuery(id=None, data="b", bot=bot)
        with pytest.warns(RuntimeWarning):
            assert await event.answer("ok") is False
    finally:
        await bot.close()

@pytest.mark.asyncio
async def test_functional_unsupported_raises(server: str) -> None:
    bot = BaleBot("B", base_url=server)
    try:
        with pytest.raises(UnsupportedFeatureError):
            await bot.send_poll(1, "q", ["a", "b"])
    finally:
        await bot.close()

@pytest.mark.asyncio
@pytest.mark.parametrize("bot_kind", ["telegram", "bale"])
async def test_all_common_operations_on_telegram_like_platforms(server: str, bot_kind: str) -> None:
    bot = TelegramBot("T", base_url=server) if bot_kind == "telegram" else BaleBot("B", base_url=server)
    try:
        assert isinstance(await bot.send_message(10, "x"), Message)
        assert isinstance(await bot.send_photo(10, b"p"), Message)
        assert isinstance(await bot.send_video(10, b"v"), Message)
        assert isinstance(await bot.send_audio(10, b"a"), Message)
        assert isinstance(await bot.send_voice(10, b"v"), Message)
        assert isinstance(await bot.send_document(10, b"d"), Message)
        assert isinstance(await bot.send_contact(10, "+1", "U"), Message)
        assert isinstance(await bot.send_location(10, 1.0, 2.0), Message)
        assert isinstance(await bot.edit_message_text(10, 1, "y"), Message)
        assert isinstance(await bot.edit_message_reply_markup(10, 1), Message)
        assert await bot.delete_message(10, 1)
        assert isinstance(await bot.forward_message(10, 11, 1), Message)
        assert await bot.answer_callback_query("c1", text="ok")
        assert await bot.send_chat_action(10, "typing")
        assert (await bot.get_chat(10)).id == 10
        assert (await bot.get_chat_member(10, 20)).status == "member"
        assert await bot.ban_chat_member(10, 20)
        assert await bot.unban_chat_member(10, 20)
        assert (await bot.get_file("f1")).id is not None
    finally:
        await bot.close()

@pytest.mark.asyncio
async def test_rubika_supported_common_operations(server: str) -> None:
    bot = RubikaBot("R", base_url=server + "/v3")
    try:
        assert isinstance(await bot.send_message("c1", "x"), Message)
        assert isinstance(await bot.send_contact("c1", "+1", "U"), Message)
        assert isinstance(await bot.send_location("c1", 1.0, 2.0), Message)
        assert isinstance(await bot.send_poll("c1", "q", ["a", "b"]), Message)
        assert isinstance(await bot.edit_message_text("c1", 1, "y"), Message)
        assert await bot.delete_message("c1", 1)
        assert isinstance(await bot.forward_message("c1", "c2", 1), Message)
        assert (await bot.get_chat("c1")).id == "c1"
        assert await bot.ban_chat_member("c1", 20)
        assert await bot.unban_chat_member("c1", 20)
        assert (await bot.get_file("f1")).id is not None
    finally:
        await bot.close()

@pytest.mark.asyncio
@pytest.mark.parametrize("platform", ["telegram", "bale", "rubika"])
async def test_bound_message_answer_on_all_platforms(server: str, platform: str) -> None:
    if platform == "telegram":
        from peyk.platforms.telegram.types import Chat, Message as RawMessage, Update
        bot = TelegramBot("T", base_url=server)
        raw = Update(update_id=1, message=RawMessage(message_id=7, date=1, chat=Chat(id=10, type="private"), text="in"))
    elif platform == "bale":
        from peyk.platforms.bale.types import Chat, Message as RawMessage, Update
        bot = BaleBot("B", base_url=server)
        raw = Update(update_id=1, message=RawMessage(message_id=7, chat=Chat(id=10, type="private"), text="in"))
    else:
        from peyk.platforms.rubika.types import Message as RawMessage, Update
        bot = RubikaBot("R", base_url=server + "/v3")
        raw = Update(type="NewMessage", chat_id="c1", new_message=RawMessage(message_id="7", text="in", sender_id="u1"))
    try:
        event = bot.normalize_update(raw)
        assert isinstance(event, Message)
        assert event.bot is bot
        sent = await event.answer("hi")
        assert isinstance(sent, Message)
    finally:
        await bot.close()
