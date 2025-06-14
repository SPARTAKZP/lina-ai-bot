import os
import logging
from fastapi import FastAPI, Request
from telegram import Update, Bot
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters
import uvicorn

# === CONFIG ===
BOT_TOKEN = os.getenv("BOT_TOKEN")
BASE_URL = os.getenv("BASE_URL")

# === LOGGING ===
logging.basicConfig(level=logging.INFO)

bot = Bot(BOT_TOKEN)
app = FastAPI()
application = Application.builder().token(BOT_TOKEN).build()

# === HANDLERS ===
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Привет, я Лина. Готова слушать тебя...")

async def echo_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text
    await update.message.reply_text(f"Ты сказал: «{user_text}». Хочешь, я скажу тебе кое-что неприличное?..")

async def echo_voice(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Ммм, ты прислал голосовое... (распознавание будет позже)")

application.add_handler(CommandHandler("start", start))
application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo_text))
application.add_handler(MessageHandler(filters.VOICE, echo_voice))

# === WEBHOOK ===
@app.post(f"/webhook/{BOT_TOKEN}")
async def telegram_webhook(req: Request):
    data = await req.json()
    update = Update.de_json(data, bot)
    await application.process_update(update)
    return {"ok": True}

@app.on_event("startup")
async def on_start():
    webhook_url = f"{BASE_URL}/webhook/{BOT_TOKEN}"
    await bot.set_webhook(webhook_url)
    print(f"✅ Webhook установлен: {webhook_url}")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080)
