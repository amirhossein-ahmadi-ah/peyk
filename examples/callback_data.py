"""A complete typed callback-data flow: send the buttons, then handle clicks."""
from peyk import Bot, CallbackData
from peyk.keyboard import InlineKeyboardBuilder


class Product(CallbackData, prefix="product"):
    id: int
    action: str


bot = Bot("TOKEN", platform="telegram")


@bot.command("products")
async def products(message):
    keyboard = (
        InlineKeyboardBuilder()
        .button(text="Buy", callback_data=Product(id=42, action="buy").pack())
        .button(text="Details", callback_data=Product(id=42, action="details").pack())
        .adjust(2)
        .as_markup()
    )
    await message.answer("Choose an action:", reply_markup=keyboard)


@bot.callback_query(Product.filter())
async def callback(query, callback_data: Product):
    await query.answer(f"{callback_data.action}: product #{callback_data.id}")


if __name__ == "__main__":
    bot.run()
