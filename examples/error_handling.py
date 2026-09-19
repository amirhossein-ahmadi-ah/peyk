"""Router error observer example."""
from peyk import Bot, Router

bot = Bot("TOKEN", platform="telegram")
router = Router(name="errors")

@router.errors()
async def errors(event):
    print(f"handler error: {event.exception}")

bot.include_router(router)

if __name__ == "__main__":
    bot.run()
