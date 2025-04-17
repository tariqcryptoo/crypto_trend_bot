import telegram
from telegram.ext import Updater, MessageHandler, Filters, CallbackContext
from telegram import Update

# بيانات البوت - جاهزة للاستخدام
BOT_TOKEN = "6195644071:AAEvGo-QGfDo9S3_rJCDNdPZJj9PldVf0j0"
GROUP_CHAT_ID = -4734806120

# دالة استقبال الرسائل
def handle_message(update: Update, context: CallbackContext):
    text = update.message.text
    print(f"Received message: {text}")
    context.bot.send_message(chat_id=GROUP_CHAT_ID, text="تم استلام رسالتك، وراح نرد عليك إذا كان ترند مهم!")

# بدء البوت
def main():
    updater = Updater(token=BOT_TOKEN, use_context=True)
    dispatcher = updater.dispatcher

    # إضافة المعالج للرسائل
    message_handler = MessageHandler(Filters.text & (~Filters.command), handle_message)
    dispatcher.add_handler(message_handler)

    # تشغيل البوت
    updater.start_polling()
    print("البوت شغال الآن...")
    updater.idle()

if __name__ == '__main__':
    main()
