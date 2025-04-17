from telegram.ext import Updater, MessageHandler, Filters

BOT_TOKEN = "7239933938:AAEhm_lWwAr7JcGomW8-EJa_rg0_BbpczdQ"

def get_chat_id(update, context):
    chat_id = update.effective_chat.id
    print(f"Chat ID: {chat_id}")
    context.bot.send_message(chat_id=chat_id, text=f"تم استلام الرسالة! معرف القروب هو:\n{chat_id}")

def main():
    updater = Updater(BOT_TOKEN, use_context=True)
    dp = updater.dispatcher
    dp.add_handler(MessageHandler(Filters.text, get_chat_id))
    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
