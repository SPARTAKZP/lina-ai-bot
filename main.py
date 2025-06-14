import os
import logging
from fastapi import FastAPI, Request
from telegram import Update, Bot
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)
import uvicorn

# === CONFIG ===
BOT_TOKEN = "8073520703:AAGVMWj0ayOSY85LfIgQWFEKnY9e6cALVWE"
BASE_URL = "https://lina-ai-bot.up.railway.app"

# === LOGGING ===
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

# === SETUP ===
bot = Bot(token=BOT_TOKEN)
app = FastAPI()
application = Application.builder().token(BOT_TOKEN).build()


# === COMMANDS ===
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Привет, я Лина. Я слушаю тебя...")


async def voice_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    file = await update.message.voice.get_file()
    await update.message.reply_text("Ммм, люблю, когда ты говоришь голосом...")


async def text_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text
    response = f"Ты сказал: «{user_text}». Хочешь, я скажу тебе кое-что неприличное?.."
    await update.message.reply_text(response)


# === HANDLERS ===
application.add_handler(CommandHandler("start", start))
application.add_handler(MessageHandler(filters.VOICE, voice_handler))
application.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), text_handler))


# === WEBHOOK ===
@app.post(f"/webhook/{BOT_TOKEN}")
async def telegram_webhook(request: Request):
    data = await request.json()
    print("📥 Получено сообщение от Telegram:", data)  # 👈 добавим это
    update = Update.de_json(data, bot)
    await application.process_update(update)
    return {"ok": True}

@app.on_event("startup")
async def on_startup():
    webhook_url = f"{BASE_URL}/webhook/{BOT_TOKEN}"
    await bot.set_webhook(webhook_url)
    print(f"✅ Webhook установлен: {webhook_url}")


# === START ===
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080)
