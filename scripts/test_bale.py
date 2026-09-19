"""
Bale platform test script for peyk dispatcher + FSM + keyboard builder.

Run: python scripts/test_bale.py
"""
import asyncio
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from peyk.dispatcher import Router
from peyk.dispatcher.filters import Command, TextEquals, CallbackDataEquals, ChatType
from peyk.fsm import FSMContext, MemoryStorage, State, StatesGroup
from peyk.utils.keyboard_builder import KeyboardBuilder, KeyboardBuildError
from peyk.utils.text_formatting import RichText, bold, italic, link, mention_user, mention_username, code, bale_expandable, render_for
from peyk.platform_core.adapters import BALE_CAPABILITIES
from peyk.platform_core.contracts import IncomingMessage, IncomingCallbackQuery
from peyk.platforms.bale.types import InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup


# ── FSM States ──────────────────────────────────────────────────────────────
class Survey(StatesGroup):
    name = State()
    rating = State()
    done = State()


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
def test_bale_keyboard():
    section("Bale Keyboard Builder")

    # 1. Inline keyboard with callback + URL
    kb = KeyboardBuilder()
    kb.button("📝 Register", callback_data="bale_reg_start")
    kb.row()
    kb.url("🌐 Visit", "https://bale.ai")
    markup = kb.build("bale")

    check("InlineKeyboardMarkup type", True, isinstance(markup, InlineKeyboardMarkup))
    check("Row count", 2, len(markup.inline_keyboard))
    check("Button text", "📝 Register", markup.inline_keyboard[0][0].text)
    check("Callback data", "bale_reg_start", markup.inline_keyboard[0][0].callback_data)
    check("URL button", "🌐 Visit", markup.inline_keyboard[1][0].text)
    check("URL value", "https://bale.ai", markup.inline_keyboard[1][0].url)

    # 2. Reply keyboard with request_contact + request_location
    kb2 = KeyboardBuilder()
    kb2.reply_button("📱 Share Contact", request_contact=True)
    kb2.row()
    kb2.reply_button("📍 Share Location", request_location=True)
    markup2 = kb2.build("bale")
    check("Reply keyboard row count", 2, len(markup2.keyboard))
    check("Request contact", True, markup2.keyboard[0][0].request_contact)
    check("Request location", True, markup2.keyboard[1][0].request_location)

    # 3. Navigation keyboard (3 rows)
    kb3 = KeyboardBuilder()
    kb3.button("🏠 Main", callback_data="main")
    kb3.button("📋 Orders", callback_data="orders")
    kb3.row()
    kb3.button("◀️ Back", callback_data="back")
    kb3.row()
    kb3.url("🆘 Support", "https://support.bale.ai")
    markup3 = kb3.build("bale")
    check("Nav row count", 3, len(markup3.inline_keyboard))
    check("First row buttons", 2, len(markup3.inline_keyboard[0]))
    check("Last row url", "https://support.bale.ai", markup3.inline_keyboard[2][0].url)

    # 4. Error: callback_data exceeds 64 bytes
    try:
        kb4 = KeyboardBuilder()
        kb4.button("Test", callback_data="x" * 65)
        kb4.build("bale")
        check("Callback data limit", True, False)
    except KeyboardBuildError:
        check("Callback data limit raises", True, True)

    # 5. Error: Rubika-only button type on Bale
    try:
        kb5 = KeyboardBuilder()
        kb5.string_picker("Pick", button_id="sp1", items=["a", "b"])
        kb5.build("bale")
        check("Rubika-only on Bale", True, False)
    except KeyboardBuildError:
        check("Rubika-only on Bale raises", True, True)

    # 6. Multiple buttons per row
    kb6 = KeyboardBuilder()
    kb6.button("A", callback_data="a")
    kb6.button("B", callback_data="b")
    kb6.button("C", callback_data="c")
    markup6 = kb6.build("bale")
    check("3 buttons in row", 3, len(markup6.inline_keyboard[0]))

    print("\n  ✅ Bale keyboard tests complete.")


# ── Text Formatting Tests ──────────────────────────────────────────────────
def test_bale_text_formatting():
    section("Bale Text Formatting")

    # Bale uses its own markdown-style syntax
    rt = bold("Hello ") + italic("World")
    rendered = render_for(rt, BALE_CAPABILITIES)
    check("Bale bold+italic", "*Hello *_World_", rendered)

    # Link
    rt2 = link("Click", "https://bale.ai")
    check("Bale link", "[Click](https://bale.ai)", render_for(rt2, BALE_CAPABILITIES))

    # mention_user
    rt3 = mention_user("@john", 12345)
    check("Bale mention user", "[@john](uid:12345)", render_for(rt3, BALE_CAPABILITIES))

    # mention_username
    rt4 = mention_username("support", "bale_support")
    check("Bale mention username", "[support](ble.ir/bale_support)", render_for(rt4, BALE_CAPABILITIES))

    # bale_expandable
    rt5 = bale_expandable("Title", bold("content"))
    check("Bale expandable", "[Title]```*content*```", render_for(rt5, BALE_CAPABILITIES))

    # code
    rt6 = code("print('hi')")
    check("Bale code", "```print('hi')```", render_for(rt6, BALE_CAPABILITIES))

    # plain_text still works
    rt7 = bold("bold") + " plain"
    check("plain_text", "bold plain", rt7.plain_text())

    print("\n  ✅ Bale text formatting tests complete.")


# ── Dispatcher Tests ────────────────────────────────────────────────────────
async def test_dispatcher():
    section("Bale Dispatcher")
    storage = MemoryStorage()
    router = Router(name="bale_main")

    calls = []

    @router.message(Command("start"))
    async def start_handler(event: IncomingMessage, **data):
        calls.append(("start", event.text))
        fsm = FSMContext(event, storage)
        await fsm.set_state(Survey.name)
        return "bale_start_handled"

    @router.message(TextEquals("cancel", case_sensitive=False))
    async def cancel_handler(event: IncomingMessage, **data):
        calls.append(("cancel", event.text))
        fsm = FSMContext(event, storage)
        await fsm.set_state(None)
        return "bale_cancelled"

    @router.message(ChatType("group"))
    async def group_message(event: IncomingMessage, **data):
        calls.append(("group", event.chat_id))
        return "group_handled"

    @router.callback_query(CallbackDataEquals("bale_reg_start"))
    async def reg_callback(event: IncomingCallbackQuery, **data):
        calls.append(("reg_start_cb", event.data))
        return "reg_callback_handled"

    # 1. /start command
    msg1 = IncomingMessage(message_id=1, chat_id=100, chat_type="private", sender_id=100, text="/start")
    results = await router.propagate_event(msg1)
    check("start handler called", ("start", "/start"), calls[0])
    check("start result", "bale_start_handled", results[0])

    # 2. Text equals "Cancel" (case insensitive)
    msg2 = IncomingMessage(message_id=2, chat_id=100, chat_type="private", sender_id=100, text="Cancel")
    calls.clear()
    results = await router.propagate_event(msg2)
    check("cancel handler called", ("cancel", "Cancel"), calls[0])

    # 3. Group chat type
    msg3 = IncomingMessage(message_id=3, chat_id=200, chat_type="group", sender_id=201, text="hello group")
    calls.clear()
    results = await router.propagate_event(msg3)
    check("group handler called", ("group", 200), calls[0])
    check("group result", "group_handled", results[0])

    # 4. Callback query
    cb = IncomingCallbackQuery(id="cb_bale_1", from_user_id=100, chat_id=100, message_id=1, data="bale_reg_start")
    calls.clear()
    results = await router.propagate_event(cb)
    check("callback handler called", ("reg_start_cb", "bale_reg_start"), calls[0])
    check("callback result", "reg_callback_handled", results[0])

    print("\n  ✅ Bale dispatcher tests complete.")


# ── FSM Tests ──────────────────────────────────────────────────────────────
async def test_fsm():
    section("Bale FSM")
    storage = MemoryStorage()

    msg = IncomingMessage(message_id=10, chat_id=42, chat_type="private", sender_id=42, text="/start")
    ctx = FSMContext(msg, storage, platform="bale")

    # 1. Initial state
    state = await ctx.get_state()
    check("Initial state is None", None, state)

    # 2. Set state
    await ctx.set_state(Survey.rating)
    state = await ctx.get_state()
    check("Set state to Survey:rating", "Survey:rating", state)

    # 3. Update data
    data = await ctx.update_data(name="Ali", rating=5)
    check("Update data name", "Ali", data["name"])
    check("Update data rating", 5, data["rating"])

    # 4. Get data
    data = await ctx.get_data()
    check("Get data", {"name": "Ali", "rating": 5}, data)

    # 5. Clear
    await ctx.clear()
    state = await ctx.get_state()
    data = await ctx.get_data()
    check("Clear state", None, state)
    check("Clear data", {}, data)

    # 6. Conversation key
    key = ctx.key
    check("Conversation key", "bale:chat=42:user=42", key)

    # 7. State string representation
    s = Survey.name
    check("State str", "Survey:name", str(s))
    check("State eq", True, Survey.name == State("Survey:name"))

    await storage.close()
    print("\n  ✅ Bale FSM tests complete.")


# ── State Filter Tests ─────────────────────────────────────────────────────
async def test_state_filter():
    section("Bale State Filter")
    from peyk.dispatcher.filters import StateFilter

    storage = MemoryStorage()
    msg = IncomingMessage(message_id=11, chat_id=50, chat_type="private", sender_id=50, text="hello")

    ctx = FSMContext(msg, storage, platform="bale")
    await ctx.set_state(Survey.done)

    filter_match = StateFilter(Survey.done, storage, platform="bale")
    filter_no_match = StateFilter(Survey.name, storage, platform="bale")

    result1 = await filter_match(msg)
    result2 = await filter_no_match(msg)

    check("StateFilter matches", True, result1)
    check("StateFilter rejects", False, result2)

    print("\n  ✅ Bale state filter tests complete.")


# ── Middleware Tests ───────────────────────────────────────────────────────
async def test_middleware():
    section("Bale Middleware")
    storage = MemoryStorage()
    router = Router(name="bale_mw_test")

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

    print("\n  ✅ Bale middleware tests complete.")


# ── Include Router Tests ───────────────────────────────────────────────────
async def test_include_router():
    section("Bale Include Router")

    parent = Router(name="bale_parent")
    child = Router(name="bale_child")
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

    print("\n  ✅ Bale include router tests complete.")


# ── Main ────────────────────────────────────────────────────────────────────
async def main():
    print("\n" + "🔵" * 30)
    print("  BALE PLATFORM TEST SUITE")
    print("🔵" * 30)

    test_bale_keyboard()
    test_bale_text_formatting()
    await test_dispatcher()
    await test_fsm()
    await test_state_filter()
    await test_middleware()
    await test_include_router()

    print("\n" + "=" * 60)
    print("  ALL BALE TESTS COMPLETE ✅")
    print("=" * 60)


if __name__ == "__main__":
    asyncio.run(main())
