from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def admin_panel_kb():
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="➕ Enroll Agent", callback_data="add_user"),
            InlineKeyboardButton(text="➖ Revoke Agent", callback_data="remove_user")
        ],
        [
            InlineKeyboardButton(text="👥 Active Agents", callback_data="list_users")
        ],
        [
            InlineKeyboardButton(text="📢 Global Broadcast", callback_data="broadcast")
        ],
        [
            InlineKeyboardButton(text="🛰️ System Status", callback_data="status")
        ]
    ])
