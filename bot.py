import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from config import TOKEN, OWNER_ID
from database import add_user, remove_user, is_allowed, list_users

bot = Bot(token=TOKEN)
dp = Dispatcher()

# ---------------- BASIC ----------------

@dp.message(Command("start"))
async def start_cmd(message: types.Message):
    await message.answer(
        "🤖 PM Bot Online\n"
        "Send your message here, it will reach Alpha-117."
    )

# ---------------- ADMIN PANEL ----------------

def owner_only(message: types.Message) -> bool:
    return message.from_user.id == OWNER_ID

@dp.message(Command("panel"))
async def panel(message: types.Message):
    if not owner_only(message):
        return

    await message.answer(
        "🎛️ *Admin Panel*\n\n"
        "/adduser <id>\n"
        "/removeuser <id>\n"
        "/listusers\n"
        "/broadcast <msg>",
        parse_mode="Markdown"
    )

@dp.message(Command("adduser"))
async def adduser_cmd(message: types.Message):
    if not owner_only(message):
        return

    parts = message.text.split()
    if len(parts) != 2:
        await message.answer("Usage: /adduser <user_id>")
        return

    add_user(int(parts[1]))
    await message.answer("✅ User added to allowed list")

@dp.message(Command("removeuser"))
async def removeuser_cmd(message: types.Message):
    if not owner_only(message):
        return

    parts = message.text.split()
    if len(parts) != 2:
        await message.answer("Usage: /removeuser <user_id>")
        return

    remove_user(int(parts[1]))
    await message.answer("❌ User removed")

@dp.message(Command("listusers"))
async def listusers_cmd(message: types.Message):
    if not owner_only(message):
        return

    users = list_users()
    if not users:
        await message.answer("No allowed users.")
        return

    text = "👥 Allowed Users:\n" + "\n".join(str(u) for u in users)
    await message.answer(text)

@dp.message(Command("broadcast"))
async def broadcast_cmd(message: types.Message):
    if not owner_only(message):
        return

    msg = message.text.replace("/broadcast", "").strip()
    if not msg:
        await message.answer("Usage: /broadcast <message>")
        return

    users = list_users()
    sent = 0

    for uid in users:
        try:
            await bot.send_message(uid, msg)
            sent += 1
        except:
            pass

    await message.answer(f"📢 Broadcast sent to {sent} users")

# ---------------- PM FORWARD ----------------

@dp.message()
async def forward_pm(message: types.Message):
    user = message.from_user

    await bot.send_message(
        OWNER_ID,
        f"📩 New Message\n"
        f"From: {user.first_name} (@{user.username})\n"
        f"ID: {user.id}\n\n"
        f"{message.text}"
    )

# ---------------- RUN ----------------

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
