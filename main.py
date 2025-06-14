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

BOT_TOKEN = "8073520703:AAGVMWj0ayOSY85LfIgQWFEKnY9e6cALVWE"
BASE_URL = "https://lina-ai-bot.up.railway.app"
WEBHOOK_PATH = "/webhook/8073520703:AAGVMWj0ayOSY85LfIgQWFEKnY9e6cALVWE"

logging.basicConfig(level=logging.DEBUG)

bot = Bot(token=BOT_TOKEN)
app = FastAPI()
application = Application.builder().token(BOT_TOKEN).build()

@app.get("/")
async def root():
    return {"status": "Lina is alive"}

# === Команды ===
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logging.info(f"[START] {update.effective_user.id}")
    await update.message.reply_text("Привет, я Лина. Я слушаю тебя...")

async def voice_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logging.info(f"[VOICE] {update.effective_user.id}")
    await update.message.reply_text("Ммм... люблю твой голос. (распознавание скоро будет)")

async def text_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text
    logging.info(f"[TEXT] {update.effective_user.id}: {user_text}")
    await update.message.reply_text(f"Ты сказал: «{user_text}». Хочешь, я скажу тебе кое-что неприличное?..")

application.add_handler(CommandHandler("start", start))
application.add_handler(MessageHandler(filters.VOICE, voice_handler))
application.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), text_handler))

# === WEBHOOK ===
@app.post("/webhook/8073520703:AAGVMWj0ayOSY85LfIgQWFEKnY9e6cALVWE")
async def telegram_webhook(request: Request):
    data = await request.json()
    print("📩 Пришло обновление от Telegram!")
    update = Update.de_json(data, bot)
    await application.process_update(update)
    return {"ok": True}

# === Старт сервера и установка Webhook ===
@app.on_event("startup")
async def on_startup():
    await asyncio.sleep(2)
    await bot.set_webhook(f"{BASE_URL}{WEBHOOK_PATH}")
    print(f"✅ Webhook установлен: {BASE_URL}{WEBHOOK_PATH}")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
