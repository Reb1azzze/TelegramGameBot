import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo
from telegram.ext import Application, CommandHandler, ContextTypes
from dotenv import load_dotenv

# Загружаем токен из .env (или просто задай его прямо в коде)
load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")

# Короткое имя игры, заданное в BotFather при создании игры
WEB_APP_URL = "https://podrugematch3.netlify.app/"  # заменишь на свой

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("🎮 Играть в Match-3!", web_app=WebAppInfo(url=WEB_APP_URL))]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Готов к игре? Нажми кнопку ниже!", reply_markup=reply_markup)

def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.run_polling()

if __name__ == "__main__":
    main()