"""
Telegram platform test script for peyk dispatcher + FSM + keyboard builder.

Run: python scripts/test_telegram.py
"""
import asyncio
import sys
import os

# Ensure the src directory is on sys.path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from peyk.dispatcher import Router
from peyk.dispatcher.filters import Command, TextEquals, CallbackDataEquals, ChatType
from peyk.fsm import FSMContext, MemoryStorage, State, StatesGroup
from peyk.utils.keyboard_builder import KeyboardBuilder, KeyboardBuildError
from peyk.utils.text_formatting import RichText, bold, italic, link, mention_user, code, render_for
from peyk.platform_core.adapters import TELEGRAM_CAPABILITIES
from peyk.platform_core.contracts import IncomingMessage, IncomingCallbackQuery
from peyk.platforms.telegram.types import InlineKeyboardMarkup


# ── FSM States ──────────────────────────────────────────────────────────────
class Registration(StatesGroup):
    name = State()
    age = State()
    confirm = State()


# ── Helpers ─────────────────────────────────────────────────────────────────
def section(title: str):
    print(f"\n{'='*60}")
    print(f"  {title}")
    print(f"{'='*60}")


def check(label: str, expected, actual):
    status = "PASS" if expected == actual else "FAIL"
    print(f"  [{status}] {label}: expected={expected!r}, got={actual!r}")
    return expected == actual


# ── Keyboard Tests ──────────────────────────────────────────────────────────
def test_telegrams_keyboard():
    section("Telegram Keyboard Builder")

    # 1. Inline keyboard with callback + URL
    kb = KeyboardBuilder()
    kb.button("📝 Register", callback_data="reg_start")
    kb.row()
    kb.url("🌐 Visit", "https://example.com")
    markup = kb.build("telegram")

    check("InlineKeyboardMarkup type", True, isinstance(markup, InlineKeyboardMarkup))
    check("Row count", 2, len(markup.inline_keyboard))
    check("Button text", "📝 Register", markup.inline_keyboard[0][0].text)
    check("Callback data", "reg_start", markup.inline_keyboard[0][0].callback_data)
    check("URL button", "🌐 Visit", markup.inline_keyboard[1][0].text)
    check("URL value", "https://example.com", markup.inline_keyboard[1][0].url)

    # 2. Reply keyboard (request_contact + request_location)
    kb2 = KeyboardBuilder()
    kb2.reply_button("📱 Share Contact", request_contact=True)
    kb2.row()
    kb2.reply_button("📍 Share Location", request_location=True)
    markup2 = kb2.build("telegram")
    check("Reply keyboard row count", 2, len(markup2.keyboard))
    check("Request contact", True, markup2.keyboard[0][0].request_contact)
    check("Request location", True, markup2.keyboard[1][0].request_location)

    # 3. Mixed inline + row navigation
    kb3 = KeyboardBuilder()
    kb3.button("◀️ Prev", callback_data="page_1")
    kb3.button("▶️ Next", callback_data="page_3")
    kb3.row()
    kb3.button("⬅️ Back", callback_data="main_menu")
    markup3 = kb3.build("telegram")
    check("Mixed row count", 2, len(markup3.inline_keyboard))
    check("First row buttons", 2, len(markup3.inline_keyboard[0]))
    check("Second row buttons", 1, len(markup3.inline_keyboard[1]))

    # 4. Error case: Rubika-only button on Telegram
    try:
        kb4 = KeyboardBuilder()
        kb4.selection("Pick", button_id="sel_1", selection_id="s1")
        kb4.build("telegram")
        check("Rubika-only on Telegram", True, False)  # Should have raised
    except KeyboardBuildError:
        check("Rubika-only on Telegram raises", True, True)

    # 5. Error case: callback_data exceeds 64 bytes
    try:
        kb5 = KeyboardBuilder()
        kb5.button("Test", callback_data="x" * 65)
        kb5.build("telegram")
        check("Callback data limit", True, False)
    except KeyboardBuildError:
        check("Callback data limit raises", True, True)

    print("\n  ✅ Telegram keyboard tests complete.")


# ── Text Formatting Tests ──────────────────────────────────────────────────
def test_text_formatting():
    section("Text Formatting")

    rt = bold("Hello ") + italic("World") + link("Click", "https://t.me")
    rendered = render_for(rt, TELEGRAM_CAPABILITIES)
    expected = "<b>Hello </b><i>World</i><a href=\"https://t.me\">Click</a>"
    check("HTML render", expected, rendered)

    # mention_user
    rt2 = mention_user("@john", 12345)
    check("Mention user HTML", '<a href="tg://user?id=12345">@john</a>', render_for(rt2, TELEGRAM_CAPABILITIES))

    # code
    rt3 = code("print('hi')")
    check("Code HTML", "<code>print('hi')</code>", render_for(rt3, TELEGRAM_CAPABILITIES))

    # plain text extraction
    rt4 = bold("bold") + " plain"
    check("plain_text", "bold plain", rt4.plain_text())

    print("\n  ✅ Text formatting tests complete.")


# ── Dispatcher Tests ────────────────────────────────────────────────────────
async def test_dispatcher():
    section("Telegram Dispatcher")
    storage = MemoryStorage()
    router = Router(name="telegram_main")

    # Track calls
    calls = []

    @router.message(Command("start"))
    async def start_handler(event: IncomingMessage, **data):
        calls.append(("start", event.text))
        fsm = FSMContext(event, storage)
        await fsm.set_state(Registration.name)
        return "start_handled"

    @router.message(TextEquals("cancel"))
    async def cancel_handler(event: IncomingMessage, **data):
        calls.append(("cancel", event.text))
        fsm = FSMContext(event, storage)
        await fsm.set_state(None)
        return "cancelled"

    @router.message(ChatType("private"))
    async def private_message(event: IncomingMessage, **data):
        calls.append(("private", event.chat_id))
        fsm = FSMContext(event, storage)
        state = await fsm.get_state()
        return f"private_in_state_{state}"

    @router.callback_query(CallbackDataEquals("reg_start"))
    async def reg_callback(event: IncomingCallbackQuery, **data):
        calls.append(("reg_start_cb", event.data))
        return "reg_start_handled"

    # 1. /start command
    msg1 = IncomingMessage(message_id=1, chat_id=100, chat_type="private", sender_id=100, text="/start")
    results = await router.propagate_event(msg1)
    check("start handler called", ("start", "/start"), calls[0])
    check("start returns", "start_handled", results[0])

    # 2. Text equals "cancel"
    msg2 = IncomingMessage(message_id=2, chat_id=100, chat_type="private", sender_id=100, text="cancel")
    calls.clear()
    results = await router.propagate_event(msg2)
    check("cancel handler called", ("cancel", "cancel"), calls[0])

    # 3. Private chat type with FSM state
    msg3 = IncomingMessage(message_id=3, chat_id=200, chat_type="private", sender_id=200, text="hello")
    calls.clear()
    results = await router.propagate_event(msg3)
    check("private handler called", ("private", 200), calls[0])
    check("FSM state is None", "private_in_state_None", results[0])

    # 4. Callback query
    cb = IncomingCallbackQuery(id="cb1", from_user_id=100, chat_id=100, message_id=1, data="reg_start")
    calls.clear()
    results = await router.propagate_event(cb)
    check("callback handler called", ("reg_start_cb", "reg_start"), calls[0])
    check("callback result", "reg_start_handled", results[0])

    print("\n  ✅ Dispatcher tests complete.")


# ── FSM Tests ──────────────────────────────────────────────────────────────
async def test_fsm():
    section("Telegram FSM")
    storage = MemoryStorage()

    # Create a message to act as the conversation context
    msg = IncomingMessage(message_id=10, chat_id=42, chat_type="private", sender_id=42, text="/start")
    ctx = FSMContext(msg, storage, platform="telegram")

    # 1. Initial state
    state = await ctx.get_state()
    check("Initial state is None", None, state)

    # 2. Set state
    await ctx.set_state(Registration.name)
    state = await ctx.get_state()
    check("Set state to Registration:name", "Registration:name", state)

    # 3. Update data
    data = await ctx.update_data(username="test_user")
    check("Update data username", "test_user", data["username"])

    # 4. Get data
    data = await ctx.get_data()
    check("Get data", {"username": "test_user"}, data)

    # 5. Clear
    await ctx.clear()
    state = await ctx.get_state()
    data = await ctx.get_data()
    check("Clear state", None, state)
    check("Clear data", {}, data)

    # 6. Conversation key
    key = ctx.key
    check("Conversation key", "telegram:chat=42:user=42", key)

    # 7. State string representation
    s = Registration.name
    check("State str", "Registration:name", str(s))
    check("State eq", True, Registration.name == State("Registration:name"))

    await storage.close()
    print("\n  ✅ FSM tests complete.")


# ── State Filter Tests ─────────────────────────────────────────────────────
async def test_state_filter():
    section("Telegram State Filter")
    from peyk.dispatcher.filters import StateFilter

    storage = MemoryStorage()
    msg = IncomingMessage(message_id=11, chat_id=50, chat_type="private", sender_id=50, text="hello")

    # Set state first
    ctx = FSMContext(msg, storage, platform="telegram")
    await ctx.set_state(Registration.age)

    # Create filter
    filter_match = StateFilter(Registration.age, storage, platform="telegram")
    filter_no_match = StateFilter(Registration.name, storage, platform="telegram")

    result1 = await filter_match(msg)
    result2 = await filter_no_match(msg)

    check("StateFilter matches", True, result1)
    check("StateFilter rejects", False, result2)

    print("\n  ✅ State filter tests complete.")


# ── Middleware Tests ───────────────────────────────────────────────────────
async def test_middleware():
    section("Telegram Middleware")
    from peyk.dispatcher.middlewares import LoggingMiddleware

    storage = MemoryStorage()
    router = Router(name="mw_test")
    middleware_calls = []

    class TrackingMiddleware:
        async def __call__(self, handler, event, data):
            middleware_calls.append("before")
            result = await handler()
            middleware_calls.append("after")
            return result

    # Instantiate the middleware and register
    router.middleware(TrackingMiddleware())

    @router.message(Command("help"))
    async def help_handler(event: IncomingMessage, **data):
        middleware_calls.append("handler")
        return "help_ok"

    msg = IncomingMessage(message_id=20, chat_id=100, chat_type="private", sender_id=100, text="/help")
    results = await router.propagate_event(msg)

    check("Middleware before", "before", middleware_calls[0])
    check("Middleware handler", "handler", middleware_calls[1])
    check("Middleware after", "after", middleware_calls[2])
    check("Handler result", "help_ok", results[0])

    print("\n  ✅ Middleware tests complete.")


# ── Include Router Tests ───────────────────────────────────────────────────
async def test_include_router():
    section("Telegram Include Router")

    parent = Router(name="parent")
    child = Router(name="child")
    parent.include_router(child)

    child_calls = []

    @child.message(Command("child_cmd"))
    async def child_handler(event: IncomingMessage, **data):
        child_calls.append(event.text)
        return "child_handled"

    msg = IncomingMessage(message_id=30, chat_id=100, chat_type="private", sender_id=100, text="/child_cmd")
    results = await parent.propagate_event(msg)

    check("Child handler called", "/child_cmd", child_calls[0])
    check("Parent dispatches to child", "child_handled", results[0])

    print("\n  ✅ Include router tests complete.")


# ── Main ────────────────────────────────────────────────────────────────────
async def main():
    print("\n" + "🔷" * 30)
    print("  TELEGRAM PLATFORM TEST SUITE")
    print("🔷" * 30)

    test_telegrams_keyboard()
    test_text_formatting()
    await test_dispatcher()
    await test_fsm()
    await test_state_filter()
    await test_middleware()
    await test_include_router()

    print("\n" + "=" * 60)
    print("  ALL TELEGRAM TESTS COMPLETE ✅")
    print("=" * 60)


if __name__ == "__main__":
    asyncio.run(main())
