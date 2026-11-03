from peyk.keyboard import *
from peyk.keyboard.render import telegram, bale, rubika
from peyk.platform_core.capabilities import get_capabilities
from peyk.bot.policy import UnsupportedPolicy, StyleFallback

def test_neutral_builder_and_renderers():
    ir = InlineKeyboardBuilder().button(text="Go", callback_data="abc", url=None).row(InlineButton(text="U", url="https://x")).as_markup()
    assert telegram.inline_keyboard(ir, get_capabilities("telegram"), UnsupportedPolicy.DEFAULT).inline_keyboard[0][0].callback_data == "abc"
    assert bale.inline_keyboard(ir, get_capabilities("bale"), UnsupportedPolicy.DEFAULT).inline_keyboard[1][0].url == "https://x"
    assert rubika.inline_keyboard(ir, get_capabilities("rubika"), UnsupportedPolicy.DEFAULT).rows[0].buttons[0].id == "abc"

def test_limits_and_style_fallback():
    try: telegram.inline_keyboard(InlineKeyboard(( (InlineButton("", callback_data="x"),), )), get_capabilities("telegram"), UnsupportedPolicy.DEFAULT)
    except ValueError: pass
    else: assert False
    b=InlineButton("Go",style=ButtonStyle.SUCCESS)
    # Bale now has native color style support!
    x=bale.inline_keyboard(InlineKeyboard(((b,),)),get_capabilities("bale"),(UnsupportedPolicy.DEFAULT,StyleFallback.EMOJI))
    assert x.inline_keyboard[0][0].style == "success"
    assert x.inline_keyboard[0][0].text == "Go"
    from peyk.platform_core.capabilities import CapabilitySet, Support, SupportLevel, Feature
    no_style_caps = CapabilitySet("bale_no_style", {Feature.BUTTON_COLOR_STYLE: Support(SupportLevel.NONE)})
    x_fallback = bale.inline_keyboard(InlineKeyboard(((b,),)), no_style_caps, (UnsupportedPolicy.DEFAULT, StyleFallback.EMOJI))
    assert x_fallback.inline_keyboard[0][0].text.startswith("🟢")

def test_reply_remove_force():
    ir=ReplyKeyboard(((ReplyButton("x",request_contact=True,style=ButtonStyle.PRIMARY),),),resize_keyboard=True)
    assert telegram.reply_keyboard(ir,get_capabilities("telegram"),UnsupportedPolicy.DEFAULT).resize_keyboard is True
    bale_reply = bale.reply_keyboard(ir,get_capabilities("bale"),UnsupportedPolicy.DEFAULT)
    assert bale_reply.resize_keyboard is True
    assert bale_reply.keyboard[0][0].style == "primary"
    assert bale.remove_keyboard(KeyboardRemove(),get_capabilities("bale"),UnsupportedPolicy.DEFAULT).remove_keyboard
    assert rubika.remove_keyboard(KeyboardRemove(),get_capabilities("rubika"),UnsupportedPolicy.DEFAULT)["chat_keypad_type"] == "Remove"


def test_bale_colored_keyboards_builder_e2e():
    inline = (
        InlineKeyboardBuilder()
        .button(text="Primary", url="https://ble.ir", style="primary")
        .button(text="Success", url="https://ble.ir", style=ButtonStyle.SUCCESS)
        .row(
            InlineButton(text="Danger", url="https://ble.ir", style="danger"),
            InlineButton(text="Default", url="https://ble.ir"),
        )
        .as_markup()
    )
    bale_inline = bale.inline_keyboard(inline, get_capabilities("bale"), UnsupportedPolicy.DEFAULT)
    assert bale_inline.inline_keyboard[0][0].style == "primary"
    assert bale_inline.inline_keyboard[0][1].style == "success"
    assert bale_inline.inline_keyboard[1][0].style == "danger"
    assert bale_inline.inline_keyboard[1][1].style is None

    reply = (
        ReplyKeyboardBuilder(resize_keyboard=True, one_time_keyboard=False, input_field_placeholder="Select...")
        .button(text="🟢 تایید", style="success")
        .button(text="🔴 لغو", style=ButtonStyle.DANGER)
        .row(
            ReplyButton(text="🔵 گزینه اصلی", style="primary"),
            ReplyButton(text="⚪️ معمولی"),
        )
        .as_markup()
    )
    bale_reply = bale.reply_keyboard(reply, get_capabilities("bale"), UnsupportedPolicy.DEFAULT)
    assert bale_reply.resize_keyboard is True
    assert bale_reply.one_time_keyboard is False
    assert bale_reply.input_field_placeholder == "Select..."
    assert bale_reply.keyboard[0][0].style == "success"
    assert bale_reply.keyboard[0][1].style == "danger"
    assert bale_reply.keyboard[1][0].style == "primary"
    assert bale_reply.keyboard[1][1].style is None

