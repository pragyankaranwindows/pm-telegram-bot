import asyncio
from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command, CommandStart
from aiogram.types import Message, CallbackQuery

from config import TOKEN, OWNER_ID
from database import add_user, remove_user, list_users
from keyboards import admin_panel_kb

# -------- VERSION --------
BOT_VERSION = "ALPHA-CONTROL-v2.2"

# -------- INIT --------
bot = Bot(token=TOKEN)
dp = Dispatcher()

DENY_MSG = "⛔ You are not my master.\nOnly my master can use this command."

def is_owner(user_id: int) -> bool:
    return user_id == OWNER_ID

# -------- START --------
@dp.message(CommandStart())
async def start_cmd(message: Message):
    await message.answer(
        f"⚡ **ALPHA RELAY ONLINE** ⚡\n\n"
        f"🧠 Version: `{BOT_VERSION}`\n"
        f"👑 Controller: Alpha-117\n\n"
        f"Send a message to relay it.",
        parse_mode="Markdown"
    )

# -------- ADMIN PANEL --------
@dp.message(Command("panel"))
async def panel_cmd(message: Message):
    if not is_owner(message.from_user.id):
        await message.answer(DENY_MSG)
        return

    await message.answer(
        "⚡ **ALPHA CONTROL PANEL** ⚡\n\n"
        "🛡️ Clearance: OWNER\n"
        "📡 Status: ONLINE\n\n"
        "Select an operation:",
        reply_markup=admin_panel_kb(),
        parse_mode="Markdown"
    )

# -------- CALLBACK HANDLER --------
@dp.callback_query()
async def panel_callbacks(call: CallbackQuery):
    if not is_owner(call.from_user.id):
        await call.answer("⛔ You are not my master.", show_alert=True)
        return

    if call.data == "add_user":
        await call.message.answer(
            "➕ **Enroll Agent**\n\n"
            "Use command:\n`/adduser USER_ID`",
            parse_mode="Markdown"
        )

    elif call.data == "remove_user":
        await call.message.answer(
            "➖ **Revoke Agent**\n\n"
            "Use command:\n`/removeuser USER_ID`",
            parse_mode="Markdown"
        )

    elif call.data == "list_users":
        users = list_users()
        if not users:
            await call.message.answer("👥 No active agents.")
        else:
            text = "👥 **ACTIVE AGENTS**\n\n"
            text += "\n".join(f"🧿 `{u}`" for u in users)
            await call.message.answer(text, parse_mode="Markdown")

    elif call.data == "broadcast":
        await call.message.answer(
            "📢 **GLOBAL BROADCAST**\n\n"
            "Use command:\n`/broadcast MESSAGE`",
            parse_mode="Markdown"
        )

    elif call.data == "status":
        await call.message.answer(
            "🛰️ **SYSTEM STATUS**\n\n"
            "• Core: 🟢 Online\n"
            "• Relay: 🟢 Stable\n"
            "• Security: 🔒 Enforced"
        )

    await call.answer()

# -------- ADMIN COMMANDS --------
@dp.message(Command("adduser"))
async def adduser_cmd(message: Message):
    if not is_owner(message.from_user.id):
        await message.answer(DENY_MSG)
        return

    parts = message.text.split()
    if len(parts) != 2:
        await message.answer("Usage: /adduser USER_ID")
        return

    try:
        uid = int(parts[1])
        add_user(uid)
        await message.answer(f"✅ Agent `{uid}` enrolled.", parse_mode="Markdown")
    except:
        await message.answer("Invalid USER_ID")

@dp.message(Command("removeuser"))
async def removeuser_cmd(message: Message):
    if not is_owner(message.from_user.id):
        await message.answer(DENY_MSG)
        return

    parts = message.text.split()
    if len(parts) != 2:
        await message.answer("Usage: /removeuser USER_ID")
        return

    try:
        uid = int(parts[1])
        remove_user(uid)
        await message.answer(f"❌ Agent `{uid}` revoked.", parse_mode="Markdown")
    except:
        await message.answer("Invalid USER_ID")

@dp.message(Command("broadcast"))
async def broadcast_cmd(message: Message):
    if not is_owner(message.from_user.id):
        await message.answer(DENY_MSG)
        return

    msg = message.text.replace("/broadcast", "").strip()
    if not msg:
        await message.answer("Usage: /broadcast MESSAGE")
        return

    sent = 0
    for uid in list_users():
        try:
            await bot.send_message(
                uid,
                f"📢 **ALPHA BROADCAST**\n\n{msg}",
                parse_mode="Markdown"
            )
            sent += 1
        except:
            pass

    await message.answer(f"📡 Broadcast sent to {sent} agents.")

# -------- PM FORWARD (TEXT ONLY) --------
@dp.message(F.text & ~F.text.startswith("/"))
async def forward_pm(message: Message):
    user = message.from_user
    await bot.send_message(
        OWNER_ID,
        f"📩 **INCOMING MESSAGE**\n\n"
        f"👤 {user.first_name} (@{user.username})\n"
        f"🆔 `{user.id}`\n\n"
        f"{message.text}",
        parse_mode="Markdown"
    )

# -------- RUN --------
async def main():
    print(f"🚀 BOT STARTED: {BOT_VERSION}")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
