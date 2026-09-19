"""Run the same handler logic on multiple platforms."""
from peyk import Bot, run

telegram = Bot("TELEGRAM_TOKEN", platform="telegram")
bale = Bot("BALE_TOKEN", platform="bale")

@telegram.command("start")
@bale.command("start")
async def start(message):
    await message.answer("Hello from the shared handler")

if __name__ == "__main__":
    run(telegram, bale)
