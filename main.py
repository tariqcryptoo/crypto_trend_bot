import logging
import requests
from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext, MessageHandler, Filters
import feedparser
import html
from datetime import datetime

# إعدادات البوت
TOKEN = "7239933938:AAEhm_lWwAr7JcGomW8-EJa_rg0_BbpczdQ"
GROUP_CHAT_ID = -4734806120

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# روابط الأخبار
FEED_URLS = [
    "https://beincrypto.com/feed",
    "https://decrypt.co/feed",
    "https://cointelegraph.com/rss",
]

def clean_html(text):
    return html.unescape(text.replace("<![CDATA[", "").replace("]]>", "")).strip()

def fetch_top_news():
    for url in FEED_URLS:
        try:
            feed = feedparser.parse(url)
            for entry in feed.entries[:5]:
                title = clean_html(entry.title)
                link = entry.link
                summary = clean_html(entry.summary) if hasattr(entry, 'summary') else ""

                if any(keyword in title.lower() for keyword in ["bitcoin", "btc", "crypto", "binance", "ethereum", "eth", "sol", "airdrop", "crash", "pump", "hack", "lawsuit", "drop"]):
                    message = f"*عنوان:* {title}\n*الملخص:* {summary}\n[اقرأ التفاصيل]({link})"
                    return message
        except Exception as e:
            logging.error(f"خطأ أثناء قراءة الخلاصة: {e}")
    return None

def send_news(context: CallbackContext):
    news = fetch_top_news()
    if news:
        context.bot.send_message(chat_id=GROUP_CHAT_ID, text=news, parse_mode="Markdown", disable_web_page_preview=False)
    else:
        context.bot.send_message(chat_id=GROUP_CHAT_ID, text="✅ تم الفحص ومافي خبر يستاهل.")

def start(update: Update, context: CallbackContext):
    update.message.reply_text("أهلاً بك! البوت جاهز لفحص الأخبار.")

def main():
    updater = Updater(TOKEN)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, lambda update, context: update.message.reply_text("تم استلام رسالتك!")))

    job_queue = updater.job_queue
    job_queue.run_repeating(send_news, interval=600, first=10)

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
