"""A complete Telegram inline-mode flow, including the button that opens inline mode."""
from peyk import Bot
from peyk.platforms.telegram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    InlineQueryResultArticle,
    InputTextMessageContent,
)


bot = Bot("TOKEN", platform="telegram")


@bot.command("inline")
async def open_inline_mode(message):
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="Search inline",
                    switch_inline_query_current_chat="peyk",
                )
            ]
        ]
    )
    await message.answer(
        "Press the button, then Telegram will insert @your_bot peyk in this chat.",
        reply_markup=keyboard,
    )


@bot.router.inline_query()
async def inline(query):
    text = query.query or "Peyk inline result"
    result = InlineQueryResultArticle(
        id="1",
        title=f"Echo: {text}",
        description="Insert this result into the current chat.",
        input_message_content=InputTextMessageContent(message_text=f"You selected: {text}"),
    )
    await query.answer([result], cache_time=1, is_personal=True)


if __name__ == "__main__":
    bot.run()
