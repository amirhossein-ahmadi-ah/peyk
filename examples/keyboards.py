"""Neutral keyboard builders, styles, and Rubika-native buttons."""
from peyk import Bot
from peyk.keyboard import ButtonStyle, InlineKeyboardBuilder, Selection

bot = Bot("TOKEN", platform="telegram")
keyboard = (InlineKeyboardBuilder()
            .button(text="Primary", callback_data="primary", style=ButtonStyle.PRIMARY)
            .button(text="Success", callback_data="success", style=ButtonStyle.SUCCESS)
            .adjust(1)
            .as_markup())

rubika_selection = Selection(text="Choose", button_id="choose")

@bot.command("start")
async def start(message):
    await message.answer("Keyboard example", reply_markup=keyboard)

if __name__ == "__main__":
    bot.run()
