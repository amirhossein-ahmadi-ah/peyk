"""Compose RichText without embedding a platform-specific format."""
from peyk import Bot
from peyk.formatting import Text

bot = Bot("TOKEN", platform="telegram")

@bot.command("format")
async def formatted(message):
    text = Text("Hello ").bold("world").line().link("docs", "https://example.com")
    await message.answer(text)

if __name__ == "__main__":
    bot.run()
