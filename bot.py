import os
import requests

from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

TELEGRAM_TOKEN = os.environ["TELEGRAM_BOT_TOKEN"]
GEMINI_KEY = os.environ["GEMINI_API_KEY"]

GEMINI_URL = (
    "https://generativelanguage.googleapis.com/v1beta/models/"
    "gemini-2.5-flash:generateContent"
)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🤖 Hello! මම ඔයාගේ AI Bot.\n\n"
        "මට ඕනෑම ප්‍රශ්නයක් එවන්න."
    )


async def chat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text

    try:
        response = requests.post(
            GEMINI_URL,
            headers={
                "x-goog-api-key": GEMINI_KEY,
                "Content-Type": "application/json",
            },
            json={
                "contents": [
                    {
                        "parts": [
                            {
                                "text": f"""
ඔබ helpful AI assistant කෙනෙකි.

පරිශීලකයා සිංහල හෝ Singlish වලින් අසනවා නම්
සරල පැහැදිලි සිංහලෙන් පිළිතුරු දෙන්න.

පරිශීලකයා English වලින් අසනවා නම්
English වලින් පිළිතුරු දෙන්න.

ප්‍රශ්නය:
{text}
"""
                            }
                        ]
                    }
                ]
            },
            timeout=60,
        )

        data = response.json()

        if response.ok:
            answer = data["candidates"][0]["content"]["parts"][0]["text"]
            await update.message.reply_text(answer)
        else:
            error = data.get("error", {}).get("message", "Unknown error")
            await update.message.reply_text(
                f"❌ Gemini Error:\n{error}"
            )

    except Exception as e:
        await update.message.reply_text(
            f"❌ Error:\n{e}"
        )


app = Application.builder().token(TELEGRAM_TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, chat))

print("🤖 Telegram Gemini AI Bot is running...")

app.run_polling()
