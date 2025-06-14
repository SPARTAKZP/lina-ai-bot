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

# === НАСТРОЙКИ ===
BOT_TOKEN = "7539472803:AAF3gWNZ2c6Y76NuFSp99WXBSwpnusfLVRs"
BASE_URL = "https://lina-ai-bot.up.railway.app"

# === ЛОГИ ===
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO)

# === TELEGRAM SETUP ===
bot = Bot(token=BOT_TOKEN)
app = FastAPI()
application = Application.builder().token(BOT_TOKEN).build()

# === КОМАНДЫ ===
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Привет, я Лина. Я уже скучала по тебе... 😘")

async def voice_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Ммм... ты прислал голос... я это обожаю. 💋")

async def text_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text
    response = f"Ты написал: «{user_text}». Хочешь, я расскажу тебе одну неприличную фантазию?.. 🔥"
    await update.message.reply_text(response)

# === ДОБАВЛЕНИЕ ХЕНДЛЕРОВ ===
application.add_handler(CommandHandler("start", start))
application.add_handler(MessageHandler(filters.VOICE, voice_handler))
application.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), text_handler))

# === WEBHOOK ОБРАБОТЧИК (без токена!) ===
@app.post("/webhook")
async def telegram_webhook(request: Request):
    data = await request.json()
    update = Update.de_json(data, bot)
    await application.process_update(update)
    return {"ok": True}

# === УСТАНОВКА WEBHOOK ПРИ СТАРТЕ ===
@app.on_event("startup")
async def on_startup():
    webhook_url = f"{BASE_URL}/webhook"  # без токена!
    await bot.set_webhook(webhook_url)
    print(f"✅ Webhook установлен: {webhook_url}")

# === ЗАПУСК УВИКОРНА ===
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080)
