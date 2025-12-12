from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

import os

BOT_TOKEN = os.getenv("BOT_TOKEN")
AFFILIATE_ID = os.getenv("AFFILIATE_ID")
ADMIN_ID = os.getenv("ADMIN_ID")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Hola! 👋\nEnvíame cualquier enlace de Amazon España y yo lo convertiré en un enlace afiliado automáticamente. 🇪🇸🔥"
    )

def convert_amazon_link(url):
    if "amazon.es" not in url:
        return None

    parts = url.split("/")
    asin = None
    for part in parts:
        if len(part) == 10 and part[0].isalnum():
            asin = part
            break

    if not asin:
        return None

    affiliate_link = f"https://www.amazon.es/dp/{asin}/?tag={AFFILIATE_ID}"
    return affiliate_link

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text
    affiliate = convert_amazon_link(url)

    if affiliate:
        await update.message.reply_text(f"✅ Tu enlace afiliado:\n{affiliate}")

        if ADMIN_ID:
            try:
                await context.bot.send_message(
                    chat_id=ADMIN_ID,
                    text=f"🔔 New link created by @{update.message.from_user.username}\n\n{affiliate}"
                )
            except:
                pass
    else:
        await update.message.reply_text("❌ Por favor, envíame un enlace válido de Amazon España.")

app = ApplicationBuilder().token(BOT_TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))

if __name__ == "__main__":
    print("Bot is running...")
    app.run_polling()
