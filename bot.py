from telegram import Update, Message
from telegram.ext import (
    ApplicationBuilder, CommandHandler,
    MessageHandler, ContextTypes, filters
)

TOKEN = os.getenv('BOT_TOKEN')
ADMIN_ID = 6612266126

# Хранилище соответствий сообщений и user_id
message_to_user = {}

# Приветствие
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Salam! Näme hyzmat?")

# Пользователь пишет боту
async def forward_to_admin(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    text = update.message.text

    # Отправляем админу с подписью и сохраняем сообщение
    sent_msg: Message = await context.bot.send_message(
        chat_id=ADMIN_ID,
        text=(
            f"📩 Täze habar:\n"
            f"👤 {user.first_name} (@{user.username or 'yok'})\n"
            f"🆔 ID: {user.id}\n\n"
            f"{text}"
        )
    )

    # Связываем ID пересланного сообщения с user_id
    message_to_user[sent_msg.message_id] = user.id

    await update.message.reply_text("Jogaba garaşyň")

# Админ отвечает на сообщение — бот отправляет пользователю
async def reply_from_admin(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        return

    if update.message.reply_to_message:
        reply_id = update.message.reply_to_message.message_id
        target_user_id = message_to_user.get(reply_id)

        if target_user_id:
            # Отправляем жирным
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

if __name__ == '__main__':
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler('start', start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND & filters.User(ADMIN_ID), reply_from_admin))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, forward_to_admin))

    print("🤖 Bot işläp başlady...")
    app.run_polling()
