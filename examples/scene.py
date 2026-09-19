"""Scene-style flow represented by an ordered StatesGroup."""
from peyk import Bot
from peyk.fsm import State, StatesGroup

class Registration(StatesGroup):
    name = State()
    email = State()
    done = State()

bot = Bot("TOKEN", platform="telegram")

@bot.command("start")
async def start(message):
    await message.answer("Scene-style registration started")

if __name__ == "__main__":
    bot.run()
