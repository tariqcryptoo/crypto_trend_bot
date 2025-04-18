import requests
import time
from googletrans import Translator

# إعدادات التوكن ومعرف القروب
TELEGRAM_TOKEN = "7239933938:AAEhm_lWwAr7JcGomW8-EJa_rg0_BbpczdQ"
CHAT_ID = "-4734806120"
CRYPTO_API_KEY = "af664841cdcd4c27a050b06660d1b2f0"

translator = Translator()

def translate_text(text):
    result = translator.translate(text, src='en', dest='ar')
    return result.text

def fetch_crypto_news():
    url = "https://cryptopanic.com/api/v1/posts/"
    params = {
        "auth_token": CRYPTO_API_KEY,
        "public": "true"
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()
        return data.get("results", [])
    return []

def filter_and_translate(news_items):
    strong_trend = None
    important_news = None

    for item in news_items:
        if not item.get("title"):
            continue
        title = item["title"]
        domain = item.get("domain", "")
        importance = item.get("importance", 0)

        # نحدد الخبر الترند الأقوى
        if not strong_trend and ("binance" in title.lower() or "bitcoin" in title.lower()):
            strong_trend = f"خبر ترند: {translate_text(title)}\nالمصدر: {domain}"

        # نحدد خبر مهم حتى لو ما كان ترند
        if not important_news and importance == 1:
            important_news = f"خبر مهم: {translate_text(title)}\nالمصدر: {domain}"

    return strong_trend, important_news

def send_telegram_message(text):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": text,
        "parse_mode": "HTML"
    }
    requests.post(url, data=payload)

# حلقة التشغيل المستمرة كل 10 دقائق
while True:
    try:
        news = fetch_crypto_news()
        trend, important = filter_and_translate(news)

        if trend:
            send_telegram_message(trend)
        if important:
            send_telegram_message(important)
        if not trend and not important:
            send_telegram_message("تم الفحص ولا يوجد خبر يستاهل حالياً.")

    except Exception as e:
        send_telegram_message(f"حدث خطأ في البوت: {str(e)}")

    time.sleep(600)  # كل 10 دقائق
