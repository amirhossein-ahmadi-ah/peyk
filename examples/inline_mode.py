"""Telegram inline-mode observer example."""
from peyk import Bot

bot = Bot("TOKEN", platform="telegram")

@bot.router.inline_query()
async def inline(query):
    # Use the native bot client for the Telegram-only inline answer surface.
    await bot.client.answer_inline_query(query.id, results=[])

if __name__ == "__main__":
    bot.run()
