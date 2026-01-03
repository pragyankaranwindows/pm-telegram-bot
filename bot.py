import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from config import TOKEN, OWNER_ID

bot = Bot(token=TOKEN)
dp = Dispatcher()

@dp.message(Command("start"))
async def start_cmd(message: types.Message):
    await message.answer(
        "Hello! Send your message here. It will reach Alpha-117."
    )

@dp.message()
async def forward_pm(message: types.Message):
    user = message.from_user
    text = message.text

    await bot.send_message(
        OWNER_ID,
        f"📩 New Message\n"
        f"From: {user.first_name} (@{user.username})\n"
        f"ID: {user.id}\n\n"
        f"{text}"
    )

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
