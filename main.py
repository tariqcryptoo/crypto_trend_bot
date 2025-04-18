import requests
import time
from datetime import datetime
import os

# إعدادات التوكن ومعرف القروب
TELEGRAM_TOKEN = "7239933938:AAEhm_lWwAr7JcGomW8-EJa_rg0_BbpczdQ"
CHAT_ID = "-4734806120"
CRYPTO_API_KEY = "af664841cdcd4c27a050b06660d1b2f0"

# ملف لحفظ المعرفات المرسلة
SENT_FILE = "sent_ids.txt"

def load_sent_ids():
    if not os.path.exists(SENT_FILE):
        return set()
    with open(SENT_FILE, "r") as f:
        return set(line.strip() for line in f)

def save_sent_id(news_id):
    with open(SENT_FILE, "a") as f:
        f.write(f"{news_id}\n")

# ترجمة مبسطة
def simple_translate(text):
    replacements = {
        "Bitcoin": "بيتكوين",
        "Ethereum": "إيثيريوم",
        "Binance": "بينانس",
        "launch": "إطلاق",
        "announces": "يُعلن",
        "introduces": "يُطلق",
        "network": "شبكة",
        "partnership": "شراكة",
        "hack": "اختراق",
        "upgrade": "تحديث",
        "listing": "إدراج",
        "token": "توكن",
        "coin": "عملة",
        "exchange": "منصة",
        "price": "السعر",
        "wallet": "محفظة",
        "airdrop": "توزيع مجاني",
    }
    for en, ar in replacements.items():
        text = text.replace(en, ar)
    return text

# صياغة احترافية
def summarize_news(title):
    title_lower = title.lower()
    translated = simple_translate(title)

    if "hack" in title_lower or "exploit" in title_lower:
        return f"**تنبيه أمني:** تم تسجيل اختراق - {translated}"
    elif "listing" in title_lower or "listed" in title_lower:
        return f"**خبر إدراج:** تم إدراج عملة جديدة - {translated}"
    elif "partnership" in title_lower or "partners" in title_lower:
        return f"**شراكة جديدة:** {translated}"
    elif "airdrop" in title_lower:
        return f"**توزيع مجاني (Airdrop):** {translated}"
    elif "upgrade" in title_lower or "update" in title_lower:
        return f"**تحديث تقني:** {translated}"
    elif "launch" in title_lower or "introduce" in title_lower:
        return f"**إطلاق جديد:** {translated}"
    elif "regulation" in title_lower or "ban" in title_lower:
        return f"**تنظيمات وتشريعات:** {translated}"
    else:
        return f"**خبر ترند:** {translated}"

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

def filter_and_format(news_items, sent_ids):
    messages = []

    for item in news_items:
        news_id = str(item.get("id"))
        title = item.get("title", "")
        domain = item.get("domain", "")
        importance = item.get("importance")
        link = item.get("url", "")

        if not title or not news_id or news_id in sent_ids:
            continue

        summary = summarize_news(title)

        # شرط الترند أو المهم
        if any(word in title.lower() for word in ["bitcoin", "binance", "ethereum", "etf", "listing", "hack", "airdrop"]) or importance == "high":
            msg = f"{summary}\n\nالمصدر: {domain}\nالرابط: {link}"
            messages.append((news_id, msg))

    return messages

def send_telegram_message(text):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": text,
        "parse_mode": "Markdown"
    }
    response = requests.post(url, data=payload)
    if response.status_code == 200:
        print("[LOG] تم إرسال الرسالة لتليجرام")
    else:
        print(f"[ERROR] فشل إرسال الرسالة: {response.text}")

# الحلقة المستمرة
while True:
    try:
        sent_ids = load_sent_ids()
        news = fetch_crypto_news()
        messages = filter_and_format(news, sent_ids)

        if messages:
            for news_id, msg in messages:
                send_telegram_message(msg)
                save_sent_id(news_id)
        else:
            print("[LOG] لا يوجد خبر جديد مؤثر")
    except Exception as e:
        print(f"[ERROR] حدث خطأ أثناء التشغيل: {e}")
        send_telegram_message(f"حدث خطأ في البوت: {str(e)}")

    time.sleep(600)  # كل 10 دقائق
