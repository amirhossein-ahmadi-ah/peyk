"""Minimal echo bot using the simple API."""
from peyk import Bot

bot = Bot("TOKEN", platform="telegram")

@bot.message()
async def echo(message):
    if message.text:
        await message.answer(message.text)

if __name__ == "__main__":
    bot.run()
