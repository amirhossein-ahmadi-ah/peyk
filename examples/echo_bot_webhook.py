from peyk import Bot, Dispatcher

def main() -> None:
    bot = Bot("TOKEN", platform="telegram")
    dp = Dispatcher()

    @dp.message()
    async def echo(message) -> None:
        await message.answer(message.text or "")

    dp.run_webhook(bot, base_url="https://example.com", path_prefix="/webhook")

if __name__ == "__main__":
    main()
