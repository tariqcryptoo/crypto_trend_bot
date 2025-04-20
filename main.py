import requests
from deep_translator import GoogleTranslator
import html

# إعدادات البوت (مباشرة بدون تعديل منك)
TELEGRAM_TOKEN = "7239933938:AAEhm_lWwAr7JcGomW8-EJa_rg0_BbpczdQ"
CHAT_ID = "-4734806120"
CRYPTO_PANIC_API_KEY = "9889e4a8021167e15bc0d74858809a6e0195fa2e"

# جلب الأخبار من CryptoPanic
def fetch_crypto_news():
    url = f"https://cryptopanic.com/api/v1/posts/?auth_token={CRYPTO_PANIC_API_KEY}&public=true"
    try:
        response = requests.get(url)
        if response.status_code != 200:
            send_to_telegram(f"فشل جلب الأخبار {response.status_code}")
            return

        data = response.json()
        posts = data.get("results", [])

        for post in posts:
            title = post.get("title", "")
            description = post.get("body", "") or ""
            source = post.get("domain", "")
            url = post.get("url", "")

            full_text = f"{title}. {description}"
            summary = summarize_to_arabic(full_text)

            final_message = (
                f"عنوان مثير للاهتمام في سوق الكريبتو،\n"
                f"{summary}\n"
                f"المصدر: {source}\n"
                f"التفاصيل في الخبر:\n{url}"
            )
            send_to_telegram(final_message)

    except Exception as e:
        send_to_telegram(f"حدث خطأ أثناء تشغيل البوت: {e}")

# تلخيص الخبر وصياغته بالعربية البشرية
def summarize_to_arabic(text):
    try:
        translated = GoogleTranslator(source='auto', target='ar').translate(text)
        translated = html.unescape(translated)
        return translated.strip()
    except Exception as e:
        return "لم نتمكن من تلخيص الخبر حالياً."

# إرسال إلى تيليجرام
def send_to_telegram(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": message,
        "parse_mode": "HTML"
    }
    requests.post(url, data=payload)

# تشغيل البوت
fetch_crypto_news()
