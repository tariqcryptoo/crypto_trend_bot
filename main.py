from telegram import Bot

def main():
    print("Bot is starting...")

    bot = Bot(token="7239933938:AAEhm_lWwAr7JcGomW8-EJa_rg0_BbpczdQ")
    bot.send_message(chat_id="1273613018", text="البوت اشتغل بنجاح من Render!")

if __name__ == "__main__":
    main()
