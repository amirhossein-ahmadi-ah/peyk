"""Webhook runner with an SSL context supplied by the application."""
import ssl
from peyk import Bot, Dispatcher

bot = Bot("TOKEN", platform="telegram")
dp = Dispatcher()
dp.include_router(bot.router)
ssl_context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)

if __name__ == "__main__":
    dp.run_webhook(bot, base_url="https://example.com", secrets=["replace-me"], ssl_context=ssl_context)
