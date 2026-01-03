from telegram.ext import Application, CommandHandler, MessageHandler, filters
from config import TOKEN, OWNER_ID

async def start(update, context):
    await update.message.reply_text(
        "Hello! Send your message here. It will reach Alpha-117."
    )

async def forward_pm(update, context):
    user = update.message.from_user
    text = update.message.text

    await context.bot.send_message(
        chat_id=OWNER_ID,
        text=f"📩 New Message\n"
             f"From: {user.first_name} (@{user.username})\n"
             f"ID: {user.id}\n\n"
             f"{text}"
    )

app = Application.builder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, forward_pm))

app.run_polling()

