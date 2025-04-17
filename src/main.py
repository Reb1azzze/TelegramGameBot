import os
import json
from telegram import Update, KeyboardButton, ReplyKeyboardMarkup, WebAppInfo
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")
WEB_APP_URL = "https://podrugematch3.netlify.app/"

PRIZES = {
    1: "🎁 Сертификат на 500₽",
    2: "🎁 Сертификат на 1000₽",
    3: "🎁 Сертификат на 1500₽",
    4: "🎁 Сертификат на 2000₽",
    5: "🎁 Сертификат на 2500₽",
    6: "🎁 Сертификат на 3000₽",
    7: "🎁 Сертификат на 3500₽",
    8: "🎁 Сертификат на 4000₽",
    9: "🎁 Сертификат на 4500₽",
    10: "🏆 Сертификат на 5000₽ — ты чемпион!"
}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [[KeyboardButton("🎮 Играть в Match-3!", web_app=WebAppInfo(url=WEB_APP_URL))]]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    await update.message.reply_text("Привет, сыграй в игру '3 в ряд'!\n Чем больше сможешь набрать очков, тем лучше бонус сможешь забрать!\n\n"
                                    "10 очков: Сертификат 500р\n"
                                    "20 очков: Сертификат 1000р\n"
                                    "30 очков: Сертификат 1500р\n"
                                    "40 очков: Сертификат 2000р\n"
                                    "50 очков: Сертификат 2500р\n"
                                    "60 очков: Сертификат 3000р\n"
                                    "70 очков: Сертификат 3500р\n"
                                    "80 очков: Сертификат 4000р\n"
                                    "90 очков: Сертификат 4500р\n"
                                    "100 очков: Сертификат 5000р\n\n"
                                    "Готов к игре? Запускай её кнопкой ниже!",
                                    reply_markup=reply_markup)

async def handle_keyboard_press(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.text == "🎮 Играть в Match-3!":
        await update.message.reply_text(f"Запускай игру тут 👉 {WEB_APP_URL}")

async def handle_web_app_data(update: Update, context: ContextTypes.DEFAULT_TYPE):
    data = update.effective_message.web_app_data.data
    try:
        parsed = json.loads(data)
        score = int(parsed.get("score", 0))
        level = score // 10
        prize = PRIZES.get(level)
        if prize:
            await update.message.reply_text(
                f"Твои набранные очки💯:  {score}\n"
                f"Поздравляем! Ты получаешь: {prize}"
            )
        else:
            await update.message.reply_text(
                f"Твои набранные очки💯:  {score}\n"
                f"Продолжай играть, чтобы заработать приз! 💪"
            )
    except Exception as e:
        await update.message.reply_text("Произошла ошибка при получении данных из игры.")

def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & filters.Regex("🎮 Играть в Match-3!"), handle_keyboard_press))
    app.add_handler(MessageHandler(filters.StatusUpdate.WEB_APP_DATA, handle_web_app_data))
    app.run_polling()

if __name__ == "__main__":
    main()