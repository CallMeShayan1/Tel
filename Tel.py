import os
from flask import Flask, request
from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

# گرفتن توکن و آدرس وب‌هوک از متغیرهای محیطی
TOKEN = os.environ["BOT_TOKEN"]
WEBHOOK_URL = os.environ["WEBHOOK_URL"]

app = Flask(__name__)

# ساخت اپلیکیشن ربات
application = ApplicationBuilder().token(TOKEN).build()

# -----------------
# Handlerهای ربات
# -----------------

# /start : ارسال پیام خوشامدگویی
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("سلام من ماهان کونی هستم چه کمکی میتونم کنم؟")

# /help : نمایش منوی کمکی با کیبورد سفارشی
async def help_options(update: Update, context: ContextTypes.DEFAULT_TYPE):
    markup = ReplyKeyboardMarkup(
        [["درباره ما", "درخواست سکس", "برگشت"]],
        resize_keyboard=True
    )
    await update.message.reply_text("از بین موارد زیر انتخاب کنید", reply_markup=markup)

# /images : نمایش منوی مربوط به تصاویر با کیبورد سفارشی
async def images_options(update: Update, context: ContextTypes.DEFAULT_TYPE):
    markup = ReplyKeyboardMarkup(
        [["تجاوز به ماهان", "سکس چت با ماهان", "برگشت"]],
        resize_keyboard=True
    )
    await update.message.reply_text("از بین موارد زیر انتخاب کنید", reply_markup=markup)

# Handler برای سایر پیام‌های متنی
async def handle_other_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    if text == "درباره ما":
        await update.message.reply_text("یک خدا این ربات را ساخت")
    elif text == "درخواست سکس":
        await update.message.reply_text("درخواست شما تایید شد")
    elif text == "برگشت":
        await update.message.reply_text("شما به منوی اصلی برگشتید", reply_markup=ReplyKeyboardRemove())
    elif text == "تجاوز به ماهان":
        await update.message.reply_text("برای تجاوز به من پیام بدهید @mahan_j20")
    elif text == "سکس چت با ماهان":
        await update.message.reply_text("برای سکس چت با من پیام بدهید @mahan_j20")
    else:
        await update.message.reply_text("پیام ناشناخته")

# ثبت handlerها در اپلیکیشن
application.add_handler(CommandHandler("start", start))
application.add_handler(CommandHandler("help", help_options))
application.add_handler(CommandHandler("images", images_options))
application.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_other_message))

# ----------------------
# Endpoint وب‌هوک برای دریافت آپدیت‌ها از تلگرام
# ----------------------
@app.post(f"/{TOKEN}")
async def webhook():
    data = request.get_json(force=True)
    update = Update.de_json(data, application.bot)
    await application.process_update(update)
    return "ok"

# ----------------------
# اجرای برنامه Flask
# ----------------------
if __name__ == "__main__":
    app.run(port=8080)
