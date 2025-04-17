from telegram.ext import Updater, MessageHandler, Filters

def get_chat_id(update, context):
    chat_id = update.effective_chat.id
    print(f"Chat ID: {chat_id}")

def main():
    updater = Updater("7239933938:AAEhm_lWwAr7JcGomW8-EJa_rg0_BbpczdQ", use_context=True)
    dp = updater.dispatcher
    dp.add_handler(MessageHandler(Filters.text, get_chat_id))
    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
