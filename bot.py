import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = int(os.getenv("ADMIN_ID"))
WEBHOOK_URL = os.getenv("WEBHOOK_URL")

message_to_user = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Salam! Näme hyzmat?")

async def forward_to_admin(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    text = update.message.text
    sent_msg = await context.bot.send_message(
        chat_id=ADMIN_ID,
        text=(
            f"📩 Täze habar:\n"
            f"👤 {user.first_name} (@{user.username or 'yok'})\n"
            f"🆔 ID: {user.id}\n\n"
            f"{text}"
        )
    )
    message_to_user[sent_msg.message_id] = user.id
    await update.message.reply_text("Jogaba garaşyň")

async def reply_from_admin(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        return
    if update.message.reply_to_message:
        reply_id = update.message.reply_to_message.message_id
        target_user_id = message_to_user.get(reply_id)
        if target_user_id:
            await context.bot.send_message(
                chat_id=target_user_id,
                text=f"*{update.message.text}*",
                parse_mode='Markdown'
            )
            await update.message.reply_text("✅ Iberildi.")
        else:
            await update.message.reply_text("❌ Bu habaryň eýesi tapylmady.")
    else:
        await update.message.reply_text("ℹ️ Jogap berýän habaryň ýok.")

if __name__ == "__main__":
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND & filters.User(ADMIN_ID), reply_from_admin))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, forward_to_admin))

    # Включаем вебхук
    app.run_webhook(
        listen="0.0.0.0",
        port=int(os.environ.get("PORT", 10000)),
        webhook_url=WEBHOOK_URL
    )
