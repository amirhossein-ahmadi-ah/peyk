"""A small FSM flow using a memory storage backend."""
from peyk import Bot
from peyk.fsm import MemoryStorage, State, StatesGroup

class Form(StatesGroup):
    name = State()
    age = State()

storage = MemoryStorage()
bot = Bot("TOKEN", platform="telegram")

@bot.command("start")
async def start(message):
    await message.answer("FSM example ready")

if __name__ == "__main__":
    bot.run()
