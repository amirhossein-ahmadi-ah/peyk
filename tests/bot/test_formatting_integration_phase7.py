import pytest
from aiohttp import web
from aiohttp.test_utils import TestServer

from peyk import BaleBot, RubikaBot, TelegramBot, BotDefaults, UnsupportedPolicy
from peyk.formatting import Text, Bold
from peyk.platform_core.enums import ParseMode
from peyk.platform_core.errors import UnsupportedFeatureError


@pytest.fixture
async def capture_server():
    calls: list[tuple[str, dict[str, object]]] = []

    async def handle(request: web.Request) -> web.Response:
        method = request.match_info["method"]
        if request.content_type == "application/json":
            body = await request.json()
        else:
            form = await request.post()
            body = {key: value for key, value in form.items() if not hasattr(value, "filename")}
        calls.append((method, body))
        if method == "requestSendFile":
            return web.json_response({"status": "OK", "data": {"upload_url": str(request.url.with_path("/upload/file"))}})
        if method == "sendFile":
            return web.json_response({"status": "OK", "data": {"message_id": "m1", "text": body.get("text", "")}})
        if request.path.startswith("/v3/"):
            return web.json_response({"status": "OK", "data": {"message_id": "m1", "text": body.get("text", "")}})
        return web.json_response({
            "ok": True,
            "result": {
                "message_id": 1,
                "date": 1,
                "chat": {"id": body.get("chat_id", 10), "type": "private"},
                "from": {"id": 2, "is_bot": True, "first_name": "Bot"},
                "text": body.get("text", body.get("caption", "")),
            },
        })

    app = web.Application()
    app.router.add_post("/upload/file", lambda request: web.json_response({"file_id": "f1"}))
    app.router.add_post("/bot{token}/{method}", handle)
    app.router.add_post("/v3/{token}/{method}", handle)
    async with TestServer(app) as server:
        yield str(server.make_url("")), calls


@pytest.mark.asyncio
@pytest.mark.parametrize("platform", ["telegram", "bale", "rubika"])
async def test_text_and_caption_resolve_at_send_time(capture_server, platform):
    base, calls = capture_server
    if platform == "telegram":
        bot = TelegramBot("T", base_url=base)
        chat = 10
    elif platform == "bale":
        bot = BaleBot("B", base_url=base)
        chat = 10
    else:
        bot = RubikaBot("R", base_url=base + "/v3")
        chat = "c1"
    try:
        await bot.send_message(chat, Text("سلام ", Bold("دنیا")))
        await bot.send_photo(chat, b"p", caption=Text("کپشن ", Bold("عکس")))
        first = next(item for item in reversed(calls) if item[0] == "sendMessage")
        second = next(item for item in reversed(calls) if item[0] == "sendFile" or item[0] in {"sendPhoto", "sendVideo", "sendAudio", "sendVoice", "sendDocument"})
        if platform == "telegram":
            assert first[1]["text"] == "سلام <b>دنیا</b>"
            assert first[1]["parse_mode"] == "HTML"
            assert second[1]["caption"] == "کپشن <b>عکس</b>"
            assert second[1]["parse_mode"] == "HTML"
        elif platform == "bale":
            assert first[1]["text"] == "سلام *دنیا*"
            assert second[1]["caption"] == "کپشن *عکس*"
        else:
            assert first[1]["text"] == "سلام دنیا"
            assert first[1]["metadata"]["meta_data_parts"][0]["type"] == "Bold"
            assert second[1]["text"] == "کپشن عکس"
            assert "metadata" not in second[1]
    finally:
        await bot.close()


@pytest.mark.asyncio
async def test_default_parse_mode_and_explicit_unsupported_policy(capture_server):
    base, calls = capture_server
    tg = TelegramBot("T", base_url=base, defaults=BotDefaults(parse_mode=ParseMode.HTML))
    bale = BaleBot("B", base_url=base, defaults=BotDefaults(parse_mode=ParseMode.HTML))
    try:
        await tg.send_message(10, "<b>raw</b>")
        assert calls[-1][1]["parse_mode"] == "HTML"
        with pytest.warns(RuntimeWarning):
            await bale.send_message(10, "*raw*", parse_mode=ParseMode.HTML)
        assert "parse_mode" not in calls[-1][1]
    finally:
        await tg.close()
        await bale.close()


@pytest.mark.asyncio
@pytest.mark.parametrize("factory", [BaleBot, RubikaBot])
async def test_explicit_parse_mode_raise_on_non_telegram(capture_server, factory):
    base, _ = capture_server
    bot = factory("X", base_url=base if factory is BaleBot else base + "/v3", on_unsupported=UnsupportedPolicy.RAISE)
    try:
        with pytest.raises(UnsupportedFeatureError):
            await bot.send_message(10 if factory is BaleBot else "c1", "x", parse_mode=ParseMode.HTML)
    finally:
        await bot.close()


@pytest.mark.asyncio
async def test_rubika_formatted_edit_degrades_to_plain_text(capture_server):
    base, calls = capture_server
    bot = RubikaBot("R", base_url=base + "/v3")
    try:
        with pytest.warns(RuntimeWarning):
            await bot.edit_message_text("c1", "m1", Text("سلام ", Bold("دنیا")))
        method, body = calls[-1]
        assert method == "editMessageText"
        assert body["text"] == "سلام دنیا"
        assert "metadata" not in body
    finally:
        await bot.close()


@pytest.mark.asyncio
@pytest.mark.parametrize("platform", ["telegram", "bale", "rubika"])
async def test_str_and_rich_edit_paths(capture_server, platform):
    base, calls = capture_server
    if platform == "telegram":
        bot, chat = TelegramBot("T", base_url=base), 10
    elif platform == "bale":
        bot, chat = BaleBot("B", base_url=base), 10
    else:
        bot, chat = RubikaBot("R", base_url=base + "/v3"), "c1"
    try:
        await bot.edit_message_text(chat, "m1" if platform == "rubika" else 1, "plain")
        if platform == "rubika":
            with pytest.warns(RuntimeWarning):
                await bot.edit_message_text(chat, "m1", Text("سلام ", Bold("دنیا")))
        else:
            await bot.edit_message_text(chat, 1, Text("سلام ", Bold("دنیا")))
        method, body = calls[-1]
        assert method == "editMessageText"
        assert body["text"] == ("سلام دنیا" if platform == "rubika" else ("سلام <b>دنیا</b>" if platform == "telegram" else "سلام *دنیا*"))
    finally:
        await bot.close()
