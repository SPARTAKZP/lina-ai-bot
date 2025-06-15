import logging
from fastapi import FastAPI, Request
from telegram import Update, Bot
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters
import uvicorn

BOT_TOKEN = "7539472803:AAF3gWNZ2c6Y76NuFSp99WXBSwpnusfLVRs"
BASE_URL = "https://lina-ai-bot.up.railway.app"

logging.basicConfig(level=logging.INFO)

bot = Bot(token=BOT_TOKEN)
app = FastAPI()
application = Application.builder().token(BOT_TOKEN).build()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Привет, я Лина. Говори со мной...")

async def text_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(f"Ты сказал: «{update.message.text}». Я вся твоя...")

application.add_handler(CommandHandler("start", start))
application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, text_handler))

@app.post("/webhook")
async def telegram_webhook(request: Request):
    data = await request.json()
    update = Update.de_json(data, bot)

    if not application.running:
        await application.initialize()
    await application.process_update(update)
    return {"ok": True}

@app.on_event("startup")
async def on_startup():
    webhook_url = f"{BASE_URL}/webhook"
    await bot.set_webhook(webhook_url)
    print(f"✅ Webhook установлен: {webhook_url}")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080)
