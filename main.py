from telegram import Bot

def main():
    print("Bot is starting...")

    # إنشاء البوت
    bot = Bot(token="هنا_تحط_توكن_البوت")

    # إرسال رسالة إلى حسابك في تيليجرام
    bot.send_message(chat_id="1273613018", text="البوت اشتغل بنجاح من Render!")

if __name__ == "__main__":
    main()
