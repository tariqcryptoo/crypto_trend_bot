import requests
import time
from deep_translator import GoogleTranslator

# إعدادات التوكن ومعرف القروب في تيليجرام
TELEGRAM_TOKEN = "7239933938:AAEhm_lWwAr7JcGomW8-EJa_rg0_BbpczdQ"
CHAT_ID = "-4734806120"

# رابط API الخاص بموقع CryptoPanic
CRYPTO_PANIC_API = "https://cryptopanic.com/api/v1/posts/?auth_token=9889e4a8021167e15bc0d74858809a6e0195fa2e&kind=news"

# حفظ آخر معرف خبر تم إرساله لتجنب التكرار
latest_news_id = None

def fetch_crypto_news():
    global latest_news_id
    try:
        response = requests.get(CRYPTO_PANIC_API)
        data = response.json()

        if "results" not in data or not data["results"]:
            send_message("ما فيه أخبار جديدة حالياً.")
            return

        for article in data["results"]:
            news_id = article.get("id")
            title = article.get("title", "")
            url = article.get("url", "")
            source = article.get("source", {}).get("domain", "غير معروف")

            if news_id == latest_news_id:
                continue  # تخطي الخبر إذا تم إرساله مسبقاً

            latest_news_id = news_id

            # إعادة صياغة الخبر للغة عربية مفهومة
            translated_title = GoogleTranslator(source='auto', target='ar').translate(title)

            message = (
                f"عنوان مثير للاهتمام في سوق الكريبتو،\n"
                f"{translated_title}\n"
                f"المصدر: {source}\n"
                f"التفاصيل في الخبر:\n{url}"
            )

            send_message(message)
            time.sleep(2)  # تأخير بسيط لتجنب سبام التيليجرام

    except Exception as e:
        send_message(f"فشل جلب الأخبار: {e}")

def send_message(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": message
    }
    requests.post(url, data=payload)

# تشغيل البوت
fetch_crypto_news()
