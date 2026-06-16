from telegram import Update
from telegram.ext import (
    Application,
    MessageHandler,
    CommandHandler,
    ContextTypes,
    filters
)
from openai import OpenAI

import os
TOKEN = os.environ.get("TOKEN")
OPENROUTER_API_KEY = os.environ.get("OPENROUTER_API_KEY")

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=OPENROUTER_API_KEY,
)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Hola, soy tu bot de confianza creado para servirte."
    )

async def ayuda(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "/start - Iniciar\n"
        "/ayuda - Ver comandos\n"
        "/info - Información del bot"
    )

async def info(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🤖 Bot creado Por @Kalashnikov_ron"
    )	
async def responder(update: Update, context: ContextTypes.DEFAULT_TYPE):
    pregunta = update.message.text

    msg = await update.message.reply_text("⏳ Toy Pensando ctm...")

    try:
        respuesta = client.chat.completions.create(
            model="openai/gpt-oss-20b:free",
            messages=[
                {"role": "user", "content": pregunta}
            ]
        )

        texto = respuesta.choices[0].message.content

        await msg.delete()  # BORRA el mensaje de "pensando"

        await update.message.reply_text(texto)

    except Exception as e:
        await msg.delete()  # también lo borra si hay error
        await update.message.reply_text(f"Error: {e}")

app = Application.builder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("ayuda", ayuda))
app.add_handler(CommandHandler("info", info))

app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, responder))

app.run_polling()