"""Webhook runner example."""
from peyk import Bot, Dispatcher

bot = Bot("TOKEN", platform="telegram")
dp = Dispatcher()
dp.include_router(bot.router)

if __name__ == "__main__":
    dp.run_webhook(bot, base_url="https://example.com", secrets=["replace-me"])
