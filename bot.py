import asyncio
from aiogram import Bot, Dispatcher, F, types
from aiogram.filters import Command, CommandStart
from aiogram.types import CallbackQuery, Message

from config import TOKEN, OWNER_ID
from database import add_user, remove_user, list_users
from keyboards import admin_panel_kb

# ---------------- INIT ----------------

bot = Bot(token=TOKEN)
dp = Dispatcher()

def is_owner(user_id: int) -> bool:
    return user_id == OWNER_ID

# ---------------- START ----------------

@dp.message(CommandStart())
async def start_cmd(message: Message):
    await message.answer(
        "🤖 **PM RELAY NODE ONLINE**\n\n"
        "Send your message here.\n"
        "It will be delivered to **Alpha-117**.",
        parse_mode="Markdown"
    )

# ---------------- ADMIN PANEL ----------------

@dp.message(Command("panel"))
async def admin_panel(message: Message):
    if not is_owner(message.from_user.id):
        return

    await message.answer(
        "⚡ **ALPHA CONTROL PANEL** ⚡\n\n"
        "🧠 *Command Authority:* OWNER\n"
        "🛡️ *Security Level:* MAX\n"
        "📡 *System Status:* ONLINE\n\n"
        "Select an operation below:",
        reply_markup=admin_panel_kb(),
        parse_mode="Markdown"
    )

# ---------------- CALLBACK HANDLER ----------------

@dp.callback_query()
async def admin_callbacks(call: CallbackQuery):
    if not is_owner(call.from_user.id):
        await call.answer("⛔ Access Denied", show_alert=True)
        return

    action = call.data

    if action == "add_user":
        await call.message.answer(
            "➕ **Enroll New Agent**\n\n"
            "Command:\n"
            "`/adduser USER_ID`",
            parse_mode="Markdown"
        )

    elif action == "remove_user":
        await call.message.answer(
            "➖ **Revoke Agent Access**\n\n"
            "Command:\n"
            "`/removeuser USER_ID`",
            parse_mode="Markdown"
        )

    elif action == "list_users":
        users = list_users()
        if not users:
            await call.message.answer("👥 No active agents.")
        else:
            text = "👥 **ACTIVE AGENTS**\n\n"
            text += "\n".join(f"🧿 `{u}`" for u in users)
            await call.message.answer(text, parse_mode="Markdown")

    elif action == "broadcast":
        await call.message.answer(
            "📢 **GLOBAL BROADCAST MODE**\n\n"
            "Command:\n"
            "`/broadcast MESSAGE`",
            parse_mode="Markdown"
        )

    elif action == "status":
        await call.message.answer(
            "🛰️ **SYSTEM STATUS**\n\n"
            "• Core: 🟢 Online\n"
            "• Relay: 🟢 Stable\n"
            "• Agents: 🟢 Active\n"
            "• Security: 🔒 Enforced"
        )

    await call.answer()

# ---------------- ADMIN COMMANDS ----------------

@dp.message(Command("adduser"))
async def adduser_cmd(message: Message):
    if not is_owner(message.from_user.id):
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
        return

    msg = message.text.replace("/broadcast", "").strip()
    if not msg:
        await message.answer("Usage: /broadcast MESSAGE")
        return

    users = list_users()
    sent = 0

    for uid in users:
        try:
            await bot.send_message(
                uid,
                f"📢 **COMMAND CORE MESSAGE**\n\n{msg}",
                parse_mode="Markdown"
            )
            sent += 1
        except:
            pass

    await message.answer(f"📡 Broadcast delivered to {sent} agents.")

# ---------------- PM FORWARD (TEXT ONLY, NO COMMANDS) ----------------

@dp.message(F.text & ~F.text.startswith("/"))
async def forward_pm(message: Message):
    user = message.from_user

    await bot.send_message(
        OWNER_ID,
        f"📩 **INCOMING TRANSMISSION**\n\n"
        f"👤 {user.first_name} (@{user.username})\n"
        f"🆔 `{user.id}`\n\n"
        f"{message.text}",
        parse_mode="Markdown"
    )

# ---------------- RUN ----------------

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
