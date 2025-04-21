import requests
import time
from deep_translator import GoogleTranslator
from telegram import Bot

# إعدادات البوت
TELEGRAM_TOKEN = "7239933938:AAEhm_lWwAr7JcGomW8-EJa_rg0_BbpczdQ"
CHAT_ID = "-4734806120"
CRYPTO_API_KEY = "9889e4a8021167e15bc0d74858809a6e0195fa2e"

bot = Bot(token=TELEGRAM_TOKEN)

# استخراج اسم المصدر من الرابط
def extract_source(url):
    try:
        return url.split("/")[2].replace("www.", "")
    except:
        return "crypto site"

# ترجمة نص إلى العربية
def human_translate(text):
    try:
        return GoogleTranslator(source='en', target='ar').translate(text)
    except:
        return "⚠️ فشل الترجمة"

# إرسال رسالة إلى تيليجرام
def send_to_telegram(title, url, content):
    source = extract_source(url)
    message = (
        f"عنوان مثير للاهتمام في سوق الكريبتو،\n"
        f"{human_translate(title)}:\n\n"
        f"المصدر: {source}\n"
        f"التفاصيل في الخبر:\n{url}"
    )
    bot.send_message(chat_id=CHAT_ID, text=message)

# جلب الأخبار
def fetch_crypto_news():
    url = f"https://cryptopanic.com/api/v1/posts/?auth_token={CRYPTO_API_KEY}&filter=important"
    response = requests.get(url)
    if response.status_code != 200:
        bot.send_message(chat_id=CHAT_ID, text="⚠️ فشل جلب الأخبار.")
        return

    data = response.json()
    posts = data.get("results", [])[:5]

    if not posts:
        bot.send_message(chat_id=CHAT_ID, text="✅ البوت شغال: لا توجد أخبار مهمة حالياً.")
        return

    for post in posts:
        title = post.get("title", "")
        link = post.get("url", "")
        content = post.get("body", "") or post.get("description", "")

        if not link or not title:
            continue

        send_to_telegram(title, link, content)
        time.sleep(2)

# تشغيل البوت
fetch_crypto_news()
