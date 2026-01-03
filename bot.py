import asyncio
from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command, CommandStart
from aiogram.types import Message, CallbackQuery

from config import TOKEN, OWNER_ID
from database import (
    add_user, remove_user, list_users,
    add_admin, remove_admin, list_admins, is_admin
)
from keyboards import admin_panel_kb

# ================= CONFIG =================
BOT_VERSION = "ALPHA-CONTROL-v3.1"
DENY_MSG = "⛔ You are not my master.\nOnly my master can use this command."

# ================= INIT ===================
bot = Bot(token=TOKEN)
dp = Dispatcher()

# message_id -> original_user_id
REPLY_MAP = {}

# ================= ROLES ==================
def is_owner(uid: int) -> bool:
    return uid == OWNER_ID

def is_controller(uid: int) -> bool:
    return is_owner(uid) or is_admin(uid)

# ================= START ==================
@dp.message(CommandStart())
async def start_cmd(message: Message):
    await message.answer(
        f"⚡ **ALPHA RELAY ONLINE** ⚡\n\n"
        f"🧠 Version: `{BOT_VERSION}`\n"
        f"👑 Controller: Alpha-117\n\n"
        f"Send a message to relay it.",
        parse_mode="Markdown"
    )

# ================= PANEL ==================
@dp.message(Command("panel"))
async def panel_cmd(message: Message):
    if not is_controller(message.from_user.id):
        await message.answer(DENY_MSG)
        return

    await message.answer(
        "⚡ **ALPHA CONTROL PANEL** ⚡\n\n"
        "🛡️ Clearance: ADMIN\n"
        "📡 Status: ONLINE\n\n"
        "Select an operation:",
        reply_markup=admin_panel_kb(),
        parse_mode="Markdown"
    )

# ================= CALLBACKS ==============
@dp.callback_query()
async def panel_callbacks(call: CallbackQuery):
    if not is_controller(call.from_user.id):
        await call.answer("⛔ Access Denied", show_alert=True)
        return

    if call.data == "status":
        await call.message.answer(
            "🛰️ **SYSTEM STATUS**\n\n"
            f"Admins: {len(list_admins())}\n"
            f"Agents: {len(list_users())}\n"
            "Security: 🔒 Enforced"
        )

    await call.answer()

# ================= AGENT MGMT ==============
@dp.message(Command("adduser"))
async def adduser_cmd(message: Message):
    if not is_controller(message.from_user.id):
        await message.answer(DENY_MSG)
        return

    try:
        uid = int(message.text.split()[1])
        add_user(uid)
        await message.answer(f"✅ Agent `{uid}` enrolled.", parse_mode="Markdown")
    except:
        await message.answer("Usage: /adduser USER_ID")

@dp.message(Command("removeuser"))
async def removeuser_cmd(message: Message):
    if not is_controller(message.from_user.id):
        await message.answer(DENY_MSG)
        return

    try:
        uid = int(message.text.split()[1])
        remove_user(uid)
        await message.answer(f"❌ Agent `{uid}` revoked.", parse_mode="Markdown")
    except:
        await message.answer("Usage: /removeuser USER_ID")

# ================= BROADCAST ==============
@dp.message(Command("broadcast"))
async def broadcast_cmd(message: Message):
    if not is_controller(message.from_user.id):
        await message.answer(DENY_MSG)
        return

    msg = message.text.replace("/broadcast", "").strip()
    if not msg:
        await message.answer("Usage: /broadcast MESSAGE")
        return

    sent = 0
    for uid in list_users():
        try:
            await bot.send_message(uid, f"📢 **ALPHA BROADCAST**\n\n{msg}")
            sent += 1
        except:
            pass

    await message.answer(f"📡 Broadcast sent to {sent} agents.")

# ================= ADMIN MGMT (OWNER ONLY) =================
@dp.message(Command("addadmin"))
async def addadmin_cmd(message: Message):
    if not is_owner(message.from_user.id):
        await message.answer(DENY_MSG)
        return

    try:
        uid = int(message.text.split()[1])
        add_admin(uid)
        await message.answer(f"🛡️ Admin `{uid}` added.", parse_mode="Markdown")
    except:
        await message.answer("Usage: /addadmin USER_ID")

@dp.message(Command("removeadmin"))
async def removeadmin_cmd(message: Message):
    if not is_owner(message.from_user.id):
        await message.answer(DENY_MSG)
        return

    try:
        uid = int(message.text.split()[1])
        remove_admin(uid)
        await message.answer(f"❌ Admin `{uid}` removed.", parse_mode="Markdown")
    except:
        await message.answer("Usage: /removeadmin USER_ID")

@dp.message(Command("listadmins"))
async def listadmins_cmd(message: Message):
    if not is_owner(message.from_user.id):
        await message.answer(DENY_MSG)
        return

    admins = list_admins()
    if not admins:
        await message.answer("No admins.")
    else:
        await message.answer(
            "🛡️ **ADMINS**\n\n" + "\n".join(f"• `{a}`" for a in admins),
            parse_mode="Markdown"
        )

# ================= REPLY SYSTEM =================
@dp.message(F.reply_to_message)
async def reply_handler(message: Message):
    if not is_controller(message.from_user.id):
        return

    replied_msg_id = message.reply_to_message.message_id
    if replied_msg_id not in REPLY_MAP:
        return

    target_user_id = REPLY_MAP[replied_msg_id]

    await bot.send_message(target_user_id, message.text)
    await message.answer("✅ Reply sent.")

# ================= PM FORWARD =================
@dp.message(F.text & ~F.text.startswith("/"))
async def forward_pm(message: Message):
    user = message.from_user

    forwarded = await bot.send_message(
        OWNER_ID,
        f"📩 **INCOMING MESSAGE**\n\n"
        f"👤 {user.first_name} (@{user.username})\n"
        f"🆔 `{user.id}`\n\n"
        f"{message.text}",
        parse_mode="Markdown"
    )

    REPLY_MAP[forwarded.message_id] = user.id

# ================= RUN =================
async def main():
    print(f"🚀 BOT STARTED: {BOT_VERSION}")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
