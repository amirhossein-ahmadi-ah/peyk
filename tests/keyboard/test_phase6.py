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
    x=bale.inline_keyboard(InlineKeyboard(((b,),)),get_capabilities("bale"),(UnsupportedPolicy.DEFAULT,StyleFallback.EMOJI))
    assert x.inline_keyboard[0][0].text.startswith("🟢")

def test_reply_remove_force():
    ir=ReplyKeyboard(((ReplyButton("x",request_contact=True),),),resize_keyboard=True)
    assert telegram.reply_keyboard(ir,get_capabilities("telegram"),UnsupportedPolicy.DEFAULT).resize_keyboard is True
    assert bale.remove_keyboard(KeyboardRemove(),get_capabilities("bale"),UnsupportedPolicy.DEFAULT).remove_keyboard
    assert rubika.remove_keyboard(KeyboardRemove(),get_capabilities("rubika"),UnsupportedPolicy.DEFAULT)["chat_keypad_type"] == "Remove"

