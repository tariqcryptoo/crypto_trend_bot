import requests
import time
from datetime import datetime

# إعدادات التوكن ومعرف القروب
TELEGRAM_TOKEN = "7239933938:AAEhm_lWwAr7JcGomW8-EJa_rg0_BbpczdQ"
CHAT_ID = "-4734806120"
CRYPTO_API_KEY = "af664841cdcd4c27a050b06660d1b2f0"

# ترجمة مبسطة بدون الاعتماد على googletrans
def simple_translate(text):
    replacements = {
        "Bitcoin": "بيتكوين",
        "Ethereum": "إيثيريوم",
        "Binance": "بينانس",
        "launch": "إطلاق",
        "announces": "يُعلن",
        "network": "شبكة",
        "partnership": "شراكة",
        "hack": "اختراق",
        "upgrade": "تحديث",
        "listing": "إدراج",
        "token": "توكن",
        "coin": "عملة",
        "exchange": "منصة",
        "price": "السعر",
    }
    for en, ar in replacements.items():
        text = text.replace(en, ar)
    return text

def fetch_crypto_news():
    print(f"\n[LOG] بدء الفحص في: {datetime.now()}")
    url = "https://cryptopanic.com/api/v1/posts/"
    params = {
        "auth_token": CRYPTO_API_KEY,
        "public": "true"
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()
        results = data.get("results", [])
        print(f"[LOG] تم جلب {len(results)} خبر")
        return results
    print("[ERROR] فشل في جلب الأخبار من CryptoPanic")
    return []

def filter_and_translate(news_items):
    strong_trend = None
    important_news = None

    for item in news_items:
        title = item.get("title", "")
        domain = item.get("domain", "")
        importance = item.get("importance")
        published = item.get("published_at", "")
        link = item.get("url", "")

        if not title:
            continue

        translated = simple_translate(title)

        # فلترة خبر ترند
        if not strong_trend and any(word in title.lower() for word in ["bitcoin", "binance", "ethereum", "etf"]):
            strong_trend = f"خبر ترند:\n{translated}\nالمصدر: {domain}\nالرابط: {link}"

        # فلترة خبر مهم
        if not important_news and importance == "high":
            important_news = f"خبر مهم:\n{translated}\nالمصدر: {domain}\nالرابط: {link}"

    return strong_trend, important_news

def send_telegram_message(text):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": text,
        "parse_mode": "HTML"
    }
    response = requests.post(url, data=payload)
    if response.status_code == 200:
        print("[LOG] تم إرسال الرسالة لتليجرام")
    else:
        print(f"[ERROR] فشل إرسال الرسالة: {response.text}")

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
            send_telegram_message("تم الفحص ومافي خبر يستاهل")
            print("[LOG] لا يوجد خبر قوي حالياً")

    except Exception as e:
        print(f"[ERROR] حدث خطأ أثناء التشغيل: {e}")
        send_telegram_message(f"حدث خطأ في البوت: {str(e)}")

    time.sleep(600)  # كل 10 دقائق
