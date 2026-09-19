"""Command-oriented beginner example."""
from peyk import Bot, CommandStart

bot = Bot("TOKEN", platform="telegram")

@bot.message(CommandStart())
async def start(message, command):
    await message.answer(f"Welcome, {command.command}!")

if __name__ == "__main__":
    bot.run()
