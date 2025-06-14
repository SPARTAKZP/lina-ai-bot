import os
import logging
import asyncio
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
BOT_TOKEN = os.getenv("BOT_TOKEN") or "8073520703:AAGVMWj0ayOSY85LfIgQWFEKnY9e6cALVWE"
BASE_URL = os.getenv("BASE_URL") or "https://lina-ai-bot.up.railway.app"
WEBHOOK_PATH = "/webhook/8073520703:AAGVMWj0ayOSY85LfIgQWFEKnY9e6cALVWE"

# === ЛОГИ ===
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)

# === TELEGRAM SETUP ===
bot = Bot(token=BOT_TOKEN)
app = FastAPI()
application = Application.builder().token(BOT_TOKEN).build()

# === ПРОСТОЙ РУТ ДЛЯ ПРОВЕРКИ ===
@app.get("/")
async def root():
    return {"status": "Lina is alive"}

# === КОМАНДЫ ===
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logging.info(f"[START] Message from {update.effective_user.id}")
    await update.message.reply_text("Привет, я Лина. Я слушаю тебя...")

async def voice_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logging.info(f"[VOICE] From {update.effective_user.id}")
    file = await update.message.voice.get_file()
    await update.message.reply_text("Ммм, люблю, когда ты говоришь голосом... (распознавание скоро будет)")

async def text_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text
    logging.info(f"[TEXT] {update.effective_user.id}: {user_text}")
    response = f"Ты сказал: «{user_text}». Хочешь, я скажу тебе кое-что неприличное?.."
    await update.message.reply_text(response)

# === ХЕНДЛЕРЫ ===
application.add_handler(CommandHandler("start", start))
application.add_handler(MessageHandler(filters.VOICE, voice_handler))
application.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), text_handler))

# === WEBHOOK ===
@app.post(WEBHOOK_PATH)
async def telegram_webhook(request: Request):
    data = await request.json()
    print("📩 Пришло обновление от Telegram!")
    logging.debug(f"[WEBHOOK] Данные: {data}")
    update = Update.de_json(data, bot)
    await application.process_update(update)
    return {"ok": True}

# === СТАРТ ===
@app.on_event("startup")
async def on_startup():
    await asyncio.sleep(3)
    webhook_url = f"{BASE_URL}{WEBHOOK_PATH}"
    await bot.set_webhook(webhook_url)
    print(f"✅ Webhook установлен: {webhook_url}")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
