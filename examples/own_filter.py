"""Custom filter implemented with the public filter base class."""
from peyk import Bot
from peyk.filters import BaseFilter

class HasWord(BaseFilter):
    def __init__(self, word: str) -> None:
        self.word = word

    async def __call__(self, event: object, **data: object) -> bool:
        text = getattr(event, "text", None)
        return isinstance(text, str) and self.word in text

bot = Bot("TOKEN", platform="telegram")

@bot.message(HasWord("peyk"))
async def found(message):
    await message.answer("found")

if __name__ == "__main__":
    bot.run()
