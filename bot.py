import asyncio
from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command, CommandStart
from aiogram.types import Message, CallbackQuery

from config import TOKEN, OWNER_ID
from database import add_user, remove_user, list_users
from keyboards import admin_panel_kb

BOT_VERSION = "ALPHA-CONTROL-v2.0"

bot = Bot(token=TOKEN)
dp = Dispatcher()

def is_owner(uid: int) -> bool:
    return uid == OWNER_ID

# ---------------- START ----------------

@dp.message(CommandStart())
async def start_cmd(message: Message):
    await message.answer(
        f"⚡ **ALPHA RELAY ONLINE** ⚡\n\n"
        f"🧠 Version: `{BOT_VERSION}`\n"
        f"👑 Controller: Alpha-117\n\n"
        f"Send a message to relay it.",
        parse_mode="Markdown"
    )

# ---------------- ADMIN PANEL ----------------

@dp.message(Command("panel"))
async def panel_cmd(message: Message):
    if not is_owner(message.from_user.id):
        return

    await message.answer(
        "⚡ **ALPHA CONTROL PANEL** ⚡\n\n"
        "🛡️ Clearance: OWNER\n"
        "📡 Status: ONLINE\n\n"
        "Select operation:",
        reply_markup=admin_panel_kb(),
        parse_mode="Markdown"
    )

# ---------------- CALLBACKS ----------------

@dp.callback_query()
async def panel_callbacks(call: CallbackQuery):
    if not is_owner(call.from_user.id):
        await call.answer("⛔ ACCESS DENIED", show_alert=True)
        return

    if call.data == "add_user":
        await call.message.answer("➕ Use:\n`/adduser USER_ID`", parse_mode="Markdown")

    elif call.data == "remove_user":
        await call.message.answer("➖ Use:\n`/removeuser USER_ID`", parse_mode="Markdown")

    elif call.data == "list_users":
        users = list_users()
        if not users:
            await call.message.answer("👥 No active agents.")
        else:
            await call.message.answer(
                "👥 **ACTIVE AGENTS**\n\n" + "\n".join(f"🧿 `{u}`" for u in users),
                parse_mode="Markdown"
            )

    elif call.data == "broadcast":
        await call.message.answer("📢 Use:\n`/broadcast MESSAGE`", parse_mode="Markdown")

    elif call.data == "status":
        await call.message.answer(
            "🛰️ **SYSTEM STATUS**\n\n"
            "Core: 🟢 Online\n"
            "Security: 🔒 Enforced\n"
            "Relay: 🟢 Stable"
        )

    await call.answer()

# ---------------- ADMIN COMMANDS ----------------

@dp.message(Command("adduser"))
async def adduser_cmd(message: Message):
    if not is_owner(message.from_user.id):
        return

    try:
        uid = int(message.text.split()[1])
        add_user(uid)
        await message.answer(f"✅ Agent `{uid}` added.", parse_mode="Markdown")
    except:
        await message.answer("Usage: /adduser USER_ID")

@dp.message(Command("removeuser"))
async def removeuser_cmd(message: Message):
    if not is_owner(message.from_user.id):
        return

    try:
        uid = int(message.text.split()[1])
        remove_user(uid)
        await message.answer(f"❌ Agent `{uid}` removed.", parse_mode="Markdown")
    except:
        await message.answer("Usage: /removeuser USER_ID")

@dp.message(Command("broadcast"))
async def broadcast_cmd(message: Message):
    if not is_owner(message.from_user.id):
        return

    msg = message.text.replace("/broadcast", "").strip()
    if not msg:
        await message.answer("Usage: /broadcast MESSAGE")
        return

    count = 0
    for uid in list_users():
        try:
            await bot.send_message(uid, f"📢 **ALPHA BROADCAST**\n\n{msg}", parse_mode="Markdown")
            count += 1
        except:
            pass

    await message.answer(f"📡 Broadcast sent to {count} agents.")

# ---------------- PM FORWARD (TEXT ONLY) ----------------

@dp.message(F.text & ~F.text.startswith("/"))
async def forward_pm(message: Message):
    user = message.from_user
    await bot.send_message(
        OWNER_ID,
        f"📩 **INCOMING MESSAGE**\n\n"
        f"👤 {user.first_name} (@{user.username})\n"
        f"🆔 `{user.id}`\n\n"
        f"{message.text}",
        parse_mode="Markdo_
