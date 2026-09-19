"""Dispatcher + Router example with a real router tree and event flow."""
from peyk import Bot, Dispatcher, Router, F


bot = Bot("TOKEN", platform="telegram")
dispatcher = Dispatcher()
messages = Router(name="messages")
admin = Router(name="admin")


@messages.message(F.text)
async def echo(message):
    await message.answer(f"echo: {message.text}")


@admin.command("admin")
async def admin_command(message):
    await message.answer("Admin router handled /admin")


# Child routers are registered on the dispatcher, not only defined locally.
dispatcher.include_router(messages)
dispatcher.include_router(admin)


if __name__ == "__main__":
    dispatcher.run_polling(bot)
