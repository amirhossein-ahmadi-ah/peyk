"""Typed callback-data packing and filtering."""
from peyk import Bot, CallbackData

class Product(CallbackData, prefix="product"):
    id: int
    action: str

bot = Bot("TOKEN", platform="telegram")

@bot.callback_query(Product.filter())
async def callback(query, callback_data):
    await query.answer(f"{callback_data.action}: {callback_data.id}")

if __name__ == "__main__":
    bot.run()
