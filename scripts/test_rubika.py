"""
Rubika platform test script for peyk dispatcher + FSM + keyboard builder.

Run: python scripts/test_rubika.py
"""
import asyncio
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from peyk.dispatcher import Router
from peyk.dispatcher.filters import Command, TextEquals, CallbackDataEquals, ChatType
from peyk.fsm import FSMContext, MemoryStorage, State, StatesGroup
from peyk.utils.keyboard_builder import KeyboardBuilder, KeyboardBuildError
from peyk.utils.text_formatting import RichText, bold, italic, link, code, spoiler, strikethrough, underline, render_for, render_rubika_metadata
from peyk.platform_core.adapters import RUBIKA_CAPABILITIES
from peyk.platform_core.contracts import IncomingMessage, IncomingCallbackQuery
from peyk.platforms.rubika.types import Keypad, Button, ButtonSelection, ButtonSelectionItem, ButtonCalendar, ButtonNumberPicker, ButtonStringPicker, ButtonTextbox, ButtonLocation


# ── FSM States ──────────────────────────────────────────────────────────────
class Onboarding(StatesGroup):
    nickname = State()
    city = State()
    interest = State()
    finish = State()


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
def test_rubika_keyboard():
    section("Rubika Keyboard Builder — Core Types")

    # 1. Simple button (callback)
    kb = KeyboardBuilder()
    kb.button("📝 Register", callback_data="rubika_reg")
    markup = kb.build("rubika")
    check("Keypad type", True, isinstance(markup, Keypad))
    check("Row count", 1, len(markup.rows))
    check("Button type", True, isinstance(markup.rows[0].buttons[0], Button))
    check("Simple button text", "📝 Register", markup.rows[0].buttons[0].button_text)
    check("Simple button id", "rubika_reg", markup.rows[0].buttons[0].id)
    check("Simple button type", "Simple", markup.rows[0].buttons[0].type)

    print("\n  ✅ Core Rubika keyboard tests complete.")

    # 2. Selection button
    section("Rubika Keyboard Builder — Selection")
    kb2 = KeyboardBuilder()
    kb2.selection("Select Item", button_id="sel_1", selection_id="selection_1",
                  items=[
                      {"text": "Option A", "image_url": None, "type": None},
                      {"text": "Option B", "image_url": None, "type": None},
                  ],
                  search_type="Api", get_type="Api", is_multi_selection=True, columns_count="2")
    markup2 = kb2.build("rubika")
    btn = markup2.rows[0].buttons[0]
    check("Selection type", "Selection", btn.type)
    check("Selection nested type", True, isinstance(btn.button_selection, ButtonSelection))
    check("Selection nested items", 2, len(btn.button_selection.items))
    check("Selection item text", "Option A", btn.button_selection.items[0].text)
    check("Selection is_multi", True, btn.button_selection.is_multi_selection)
    check("Selection columns", "2", btn.button_selection.columns_count)
    check("Selection search_type", "Api", btn.button_selection.search_type)
    check("Selection get_type", "Api", btn.button_selection.get_type)

    print("  ✅ Selection tests complete.")

    # 3. Calendar button
    section("Rubika Keyboard Builder — Calendar")
    kb3 = KeyboardBuilder()
    kb3.calendar("Pick Date", button_id="cal_1", default_value="1403/06/25",
                 calendar_type="DatePersian", min_year="1400", max_year="1450")
    markup3 = kb3.build("rubika")
    btn3 = markup3.rows[0].buttons[0]
    check("Calendar type", "Calendar", btn3.type)
    check("Calendar nested type", True, isinstance(btn3.button_calendar, ButtonCalendar))
    check("Calendar default", "1403/06/25", btn3.button_calendar.default_value)
    check("Calendar min_year", "1400", btn3.button_calendar.min_year)
    check("Calendar max_year", "1450", btn3.button_calendar.max_year)

    print("  ✅ Calendar tests complete.")

    # 4. NumberPicker button
    section("Rubika Keyboard Builder — NumberPicker")
    kb4 = KeyboardBuilder()
    kb4.number_picker("Pick Number", button_id="num_1", min_value="1", max_value="10", default_value="5")
    markup4 = kb4.build("rubika")
    btn4 = markup4.rows[0].buttons[0]
    check("NumberPicker type", "NumberPicker", btn4.type)
    check("NumberPicker nested type", True, isinstance(btn4.button_number_picker, ButtonNumberPicker))
    check("NumberPicker min", "1", btn4.button_number_picker.min_value)
    check("NumberPicker max", "10", btn4.button_number_picker.max_value)
    check("NumberPicker default", "5", btn4.button_number_picker.default_value)

    print("  ✅ NumberPicker tests complete.")

    # 5. StringPicker button
    section("Rubika Keyboard Builder — StringPicker")
    kb5 = KeyboardBuilder()
    kb5.string_picker("Pick City", button_id="str_1", items=["Tehran", "Isfahan", "Shiraz"], default_value="Tehran")
    markup5 = kb5.build("rubika")
    btn5 = markup5.rows[0].buttons[0]
    check("StringPicker type", "StringPicker", btn5.type)
    check("StringPicker nested type", True, isinstance(btn5.button_string_picker, ButtonStringPicker))
    check("StringPicker items", ["Tehran", "Isfahan", "Shiraz"], btn5.button_string_picker.items)
    check("StringPicker default", "Tehran", btn5.button_string_picker.default_value)

    print("  ✅ StringPicker tests complete.")

    # 6. Location button
    section("Rubika Keyboard Builder — Location")
    kb6 = KeyboardBuilder()
    kb6.location("Pick Location", button_id="loc_1", location_type="Picker")
    markup6 = kb6.build("rubika")
    btn6 = markup6.rows[0].buttons[0]
    check("Location type", "Location", btn6.type)
    check("Location nested type", True, isinstance(btn6.button_location, ButtonLocation))
    check("Location loc_type", "Picker", btn6.button_location.type)

    print("  ✅ Location tests complete.")

    # 7. Textbox button
    section("Rubika Keyboard Builder — Textbox")
    kb7 = KeyboardBuilder()
    kb7.textbox("Enter Text", button_id="txt_1", type_line="MultiLine", type_keypad="String",
                place_holder="Type here...", title="Input", default_value="")
    markup7 = kb7.build("rubika")
    btn7 = markup7.rows[0].buttons[0]
    check("Textbox type", "Textbox", btn7.type)
    check("Textbox nested type", True, isinstance(btn7.button_textbox, ButtonTextbox))
    check("Textbox type_line", "MultiLine", btn7.button_textbox.type_line)
    check("Textbox type_keypad", "String", btn7.button_textbox.type_keypad)
    check("Textbox placeholder", "Type here...", btn7.button_textbox.place_holder)
    check("Textbox title", "Input", btn7.button_textbox.title)

    print("  ✅ Textbox tests complete.")

    # 8. CameraImage button
    section("Rubika Keyboard Builder — Camera/Image/File/Audio")
    kb8 = KeyboardBuilder()
    kb8.camera_image("Take Photo", button_id="cam_1")
    kb8.camera_video("Record Video", button_id="vid_1")
    kb8.gallery_image("Pick Photo", button_id="gal_1")
    kb8.gallery_video("Pick Video", button_id="gal_v_1")
    markup8 = kb8.build("rubika")
    check("CameraImage type", "CameraImage", markup8.rows[0].buttons[0].type)
    check("CameraVideo type", "CameraVideo", markup8.rows[0].buttons[1].type)
    check("GalleryImage type", "GalleryImage", markup8.rows[0].buttons[2].type)
    check("GalleryVideo type", "GalleryVideo", markup8.rows[0].buttons[3].type)

    print("  ✅ Camera/Gallery tests complete.")

    # 9. File/Audio/RecordAudio
    kb9 = KeyboardBuilder()
    kb9.file("Send File", button_id="file_1")
    kb9.audio("Send Audio", button_id="audio_1")
    kb9.record_audio("Record", button_id="rec_1")
    markup9 = kb9.build("rubika")
    check("File type", "File", markup9.rows[0].buttons[0].type)
    check("Audio type", "Audio", markup9.rows[0].buttons[1].type)
    check("RecordAudio type", "RecordAudio", markup9.rows[0].buttons[2].type)

    print("  ✅ File/Audio/RecordAudio tests complete.")

    # 10. Link/AskMyPhoneNumber/AskMyLocation/Barcode
    section("Rubika Keyboard Builder — Link/Phone/Location/Barcode")
    kb10 = KeyboardBuilder()
    kb10.rubika_link("Open URL", button_id="link_1", url="https://rubika.ir")
    kb10.ask_my_phone_number("Phone", button_id="phone_1")
    kb10.ask_my_location("Location", button_id="ask_loc_1")
    kb10.barcode("Scan", button_id="barcode_1")
    markup10 = kb10.build("rubika")
    check("Link type", "Link", markup10.rows[0].buttons[0].type)
    check("AskMyPhoneNumber type", "AskMyPhoneNumber", markup10.rows[0].buttons[1].type)
    check("AskMyLocation type", "AskMyLocation", markup10.rows[0].buttons[2].type)
    check("Barcode type", "Barcode", markup10.rows[0].buttons[3].type)

    print("  ✅ Link/Phone/Location/Barcode tests complete.")

    # 11. Complex multi-row keyboard
    section("Rubika Keyboard Builder — Complex Multi-Row")
    kb11 = KeyboardBuilder()
    kb11.button("🏠 Home", callback_data="home")
    kb11.button("📋 Menu", callback_data="menu")
    kb11.row()
    kb11.string_picker("City", button_id="city_sel", items=["Tehran", "Mashhad"])
    kb11.row()
    kb11.number_picker("Age", button_id="age_sel", min_value="18", max_value="99")
    kb11.row()
    kb11.ask_my_phone_number("Share Phone", button_id="phone_share")
    kb11.ask_my_location("Share Location", button_id="loc_share")
    markup11 = kb11.build("rubika")
    check("Complex row count", 4, len(markup11.rows))
    check("Row 1 buttons", 2, len(markup11.rows[0].buttons))
    check("Row 2 buttons", 1, len(markup11.rows[1].buttons))
    check("Row 3 buttons", 1, len(markup11.rows[2].buttons))
    check("Row 4 buttons", 2, len(markup11.rows[3].buttons))
    check("Row 2 type", "StringPicker", markup11.rows[1].buttons[0].type)
    check("Row 3 type", "NumberPicker", markup11.rows[2].buttons[0].type)

    print("  ✅ Complex multi-row tests complete.")


# ── Text Formatting Tests ──────────────────────────────────────────────────
def test_rubika_text_formatting():
    section("Rubika Text Formatting")

    # Rubika returns plain text by default
    rt = bold("Hello ") + italic("World") + code("test")
    rendered = render_for(rt, RUBIKA_CAPABILITIES)
    check("Rubika plain text", "Hello Worldtest", rendered)

    # metadata rendering
    rt2 = bold("Hello") + " World"
    text, metadata = render_rubika_metadata(rt2)
    check("Rubika metadata text", "Hello World", text)
    check("Rubika metadata count", 1, len(metadata))
    check("Rubika metadata type", "Bold", metadata[0]["type"])
    check("Rubika metadata from_index", 0, metadata[0]["from_index"])
    check("Rubika metadata length", 5, metadata[0]["length"])

    # Spoiler, strikethrough, underline
    rt3 = spoiler("secret") + strikethrough("old") + underline("imp")
    text3, meta3 = render_rubika_metadata(rt3)
    check("Rubika all metadata count", 3, len(meta3))
    check("Rubika spoiler type", "Spoiler", meta3[0]["type"])
    check("Rubika strike type", "Strike", meta3[1]["type"])
    check("Rubika underline type", "Underline", meta3[2]["type"])

    # Link metadata
    rt4 = link("Click", "https://rubika.ir")
    text4, meta4 = render_rubika_metadata(rt4)
    check("Rubika link text", "Click", text4)
    check("Rubika link metadata type", "Link", meta4[0]["type"])
    check("Rubika link metadata url", "https://rubika.ir", meta4[0]["link_url"])

    print("\n  ✅ Rubika text formatting tests complete.")


# ── Dispatcher Tests ────────────────────────────────────────────────────────
async def test_dispatcher():
    section("Rubika Dispatcher")
    storage = MemoryStorage()
    router = Router(name="rubika_main")

    calls = []

    @router.message(Command("start"))
    async def start_handler(event: IncomingMessage, **data):
        calls.append(("start", event.text))
        fsm = FSMContext(event, storage)
        await fsm.set_state(Onboarding.nickname)
        return "rubika_start_handled"

    @router.message(TextEquals("cancel"))
    async def cancel_handler(event: IncomingMessage, **data):
        calls.append(("cancel", event.text))
        fsm = FSMContext(event, storage)
        await fsm.set_state(None)
        return "rubika_cancelled"

    @router.message(ChatType("group"))
    async def group_message(event: IncomingMessage, **data):
        calls.append(("group", event.chat_id))
        return "group_handled"

    @router.callback_query(CallbackDataEquals("rubika_reg"))
    async def reg_callback(event: IncomingCallbackQuery, **data):
        calls.append(("reg_cb", event.data))
        return "reg_callback_handled"

    # 1. /start command
    msg1 = IncomingMessage(message_id="msg_1", chat_id="chat_100", chat_type="User", sender_id="user_100", text="/start")
    results = await router.propagate_event(msg1)
    check("start handler called", ("start", "/start"), calls[0])
    check("start result", "rubika_start_handled", results[0])

    # 2. Text equals "cancel"
    msg2 = IncomingMessage(message_id="msg_2", chat_id="chat_100", chat_type="User", sender_id="user_100", text="cancel")
    calls.clear()
    results = await router.propagate_event(msg2)
    check("cancel handler called", ("cancel", "cancel"), calls[0])

    # 3. Group chat type
    msg3 = IncomingMessage(message_id="msg_3", chat_id="chat_200", chat_type="Group", sender_id="user_201", text="hello group")
    calls.clear()
    results = await router.propagate_event(msg3)
    check("group handler called", ("group", "chat_200"), calls[0])
    check("group result", "group_handled", results[0])

    # 4. Callback query (Rubika has no id on callback)
    cb = IncomingCallbackQuery(id=None, from_user_id="user_100", chat_id="chat_100", message_id="msg_1", data="rubika_reg")
    calls.clear()
    results = await router.propagate_event(cb)
    check("callback handler called", ("reg_cb", "rubika_reg"), calls[0])
    check("callback result", "reg_callback_handled", results[0])

    print("\n  ✅ Rubika dispatcher tests complete.")


# ── FSM Tests ──────────────────────────────────────────────────────────────
async def test_fsm():
    section("Rubika FSM")
    storage = MemoryStorage()

    msg = IncomingMessage(message_id="msg_10", chat_id="chat_42", chat_type="User", sender_id="user_42", text="/start")
    ctx = FSMContext(msg, storage, platform="rubika")

    # 1. Initial state
    state = await ctx.get_state()
    check("Initial state is None", None, state)

    # 2. Set state
    await ctx.set_state(Onboarding.city)
    state = await ctx.get_state()
    check("Set state to Onboarding:city", "Onboarding:city", state)

    # 3. Update data
    data = await ctx.update_data(nickname="Ali", city="Tehran")
    check("Update data nickname", "Ali", data["nickname"])
    check("Update data city", "Tehran", data["city"])

    # 4. Get data
    data = await ctx.get_data()
    check("Get data", {"nickname": "Ali", "city": "Tehran"}, data)

    # 5. Clear
    await ctx.clear()
    state = await ctx.get_state()
    data = await ctx.get_data()
    check("Clear state", None, state)
    check("Clear data", {}, data)

    # 6. Conversation key
    key = ctx.key
    check("Conversation key", "rubika:chat=chat_42:user=user_42", key)

    # 7. State string representation
    s = Onboarding.interest
    check("State str", "Onboarding:interest", str(s))
    check("State eq", True, Onboarding.interest == State("Onboarding:interest"))

    await storage.close()
    print("\n  ✅ Rubika FSM tests complete.")


# ── State Filter Tests ─────────────────────────────────────────────────────
async def test_state_filter():
    section("Rubika State Filter")
    from peyk.dispatcher.filters import StateFilter

    storage = MemoryStorage()
    msg = IncomingMessage(message_id="msg_11", chat_id="chat_50", chat_type="User", sender_id="user_50", text="hello")

    ctx = FSMContext(msg, storage, platform="rubika")
    await ctx.set_state(Onboarding.finish)

    filter_match = StateFilter(Onboarding.finish, storage, platform="rubika")
    filter_no_match = StateFilter(Onboarding.nickname, storage, platform="rubika")

    result1 = await filter_match(msg)
    result2 = await filter_no_match(msg)

    check("StateFilter matches", True, result1)
    check("StateFilter rejects", False, result2)

    print("\n  ✅ Rubika state filter tests complete.")


# ── Middleware Tests ───────────────────────────────────────────────────────
async def test_middleware():
    section("Rubika Middleware")
    storage = MemoryStorage()
    router = Router(name="rubika_mw_test")

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

    msg = IncomingMessage(message_id="msg_20", chat_id="chat_100", chat_type="User", sender_id="user_100", text="/help")
    results = await router.propagate_event(msg)

    check("Middleware before", "before", middleware_calls[0])
    check("Middleware handler", "handler", middleware_calls[1])
    check("Middleware after", "after", middleware_calls[2])
    check("Handler result", "help_ok", results[0])

    print("\n  ✅ Rubika middleware tests complete.")


# ── Include Router Tests ───────────────────────────────────────────────────
async def test_include_router():
    section("Rubika Include Router")

    parent = Router(name="rubika_parent")
    child = Router(name="rubika_child")
    parent.include_router(child)

    child_calls = []

    @child.message(Command("child_cmd"))
    async def child_handler(event: IncomingMessage, **data):
        child_calls.append(event.text)
        return "child_handled"

    msg = IncomingMessage(message_id="msg_30", chat_id="chat_100", chat_type="User", sender_id="user_100", text="/child_cmd")
    results = await parent.propagate_event(msg)

    check("Child handler called", "/child_cmd", child_calls[0])
    check("Parent dispatches to child", "child_handled", results[0])

    print("\n  ✅ Rubika include router tests complete.")


# ── Main ────────────────────────────────────────────────────────────────────
async def main():
    print("\n" + "🔴" * 30)
    print("  RUBIKA PLATFORM TEST SUITE")
    print("🔴" * 30)

    test_rubika_keyboard()
    test_rubika_text_formatting()
    await test_dispatcher()
    await test_fsm()
    await test_state_filter()
    await test_middleware()
    await test_include_router()

    print("\n" + "=" * 60)
    print("  ALL RUBIKA TESTS COMPLETE ✅")
    print("=" * 60)


if __name__ == "__main__":
    asyncio.run(main())
