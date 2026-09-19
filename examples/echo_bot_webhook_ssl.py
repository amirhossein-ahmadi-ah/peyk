import ssl

from peyk import Bot, Dispatcher


def main() -> None:
    context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
    # Load the deployment's certificate/key here.
    context.load_cert_chain("cert.pem", "key.pem")

    bot = Bot("TOKEN", platform="telegram")
    dp = Dispatcher()

    @dp.message()
    async def echo(message) -> None:
        await message.answer(message.text or "")

    dp.run_webhook(bot, base_url="https://example.com", host="0.0.0.0", port=8443, ssl_context=context)


if __name__ == "__main__":
    main()
